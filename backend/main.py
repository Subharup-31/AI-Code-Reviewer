"""
VulnGuard AI — FastAPI Backend
Main application entry point with /scan-repo endpoint.
"""

import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
from dotenv import load_dotenv

from github_service import fetch_repo, cleanup_repo
from scanner import run_semgrep, run_bandit
from vulnerability_parser import parse_all
from cve_mapper import map_to_cve
from cvss_service import assign_cvss
from ai_engine import analyze_vulnerability

load_dotenv()


# ── Models ───────────────────────────────────────────────────────────────────

class ScanRequest(BaseModel):
    repo_url: str


class AttackSimulation(BaseModel):
    payload: str = ""
    description: str = ""


class SecureFix(BaseModel):
    description: str = ""
    code: str = ""


class CVEInfo(BaseModel):
    cve_id: str = "N/A"
    description: str = ""


class VulnerabilityResult(BaseModel):
    id: str = ""
    file: str = ""
    line: int = 0
    issue: str = ""
    severity: str = ""
    cvss_score: float = 0.0
    tool: str = ""
    code_snippet: str = ""
    cwe: list[str] = []
    cve: CVEInfo = CVEInfo()
    explanation: str = ""
    attack_simulation: AttackSimulation = AttackSimulation()
    secure_fix: SecureFix = SecureFix()


class ScanResponse(BaseModel):
    repo_url: str
    total_vulnerabilities: int
    severity_counts: dict[str, int]
    vulnerabilities: list[VulnerabilityResult]


class ApplyFixRequest(BaseModel):
    repo_url: str
    file_path: str
    line: int
    secure_code: str


class ApplyFixResponse(BaseModel):
    pr_url: str


# ── App ──────────────────────────────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("[+] VulnGuard AI backend starting...")
    yield
    print("[+] VulnGuard AI backend shutting down...")


app = FastAPI(
    title="VulnGuard AI",
    description="AI-powered GitHub repository vulnerability scanner",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Endpoints ────────────────────────────────────────────────────────────────

@app.get("/health")
async def health():
    return {"status": "ok", "service": "VulnGuard AI"}


@app.post("/scan-repo", response_model=ScanResponse)
async def scan_repo(request: ScanRequest):
    """
    Full pipeline:
    1. Clone repo
    2. Run Semgrep + Bandit
    3. Parse results
    4. CVE mapping
    5. CVSS scoring
    6. AI analysis
    7. Return enriched results
    """
    repo_path = None

    try:
        # Step 1: Fetch via GitHub API
        print(f"[1/6] Fetching repository via GitHub API: {request.repo_url}")
        repo_path = await fetch_repo(request.repo_url)

        # Step 2: Scan
        print("[2/6] Running security scanners...")
        semgrep_raw = run_semgrep(repo_path)
        bandit_raw = run_bandit(repo_path)

        # Step 3: Parse
        print("[3/6] Parsing scan results...")
        vulnerabilities = parse_all(semgrep_raw, bandit_raw, repo_path)
        print(f"     Found {len(vulnerabilities)} vulnerabilities")

        # Step 4 & 5: CVE Mapping + CVSS Scoring
        print("[4/6] Mapping CVEs and assigning CVSS scores...")
        enriched_vulns = []
        for vuln in vulnerabilities:
            cve_data = await map_to_cve(vuln.get("issue", ""))
            scored_vuln = assign_cvss(vuln, cve_data)
            enriched_vulns.append(scored_vuln)

        # Step 6: AI Analysis (process in batches to avoid rate limits)
        print("[5/6] Running AI analysis...")
        # Limit to first 20 vulnerabilities for speed
        vulns_to_analyze = enriched_vulns[:20]
        ai_tasks = [analyze_vulnerability(v) for v in vulns_to_analyze]
        ai_results = await asyncio.gather(*ai_tasks, return_exceptions=True)

        # Merge AI results
        print("[6/6] Assembling final results...")
        final_vulns = []
        for i, vuln in enumerate(enriched_vulns):
            if i < len(ai_results) and not isinstance(ai_results[i], Exception):
                ai_data = ai_results[i]
                if not ai_data.get("is_false_positive"):
                    vuln["explanation"] = ai_data.get("explanation", "")
                    vuln["attack_simulation"] = ai_data.get("attack_simulation", {})
                    vuln["secure_fix"] = ai_data.get("secure_fix", {})
                    final_vulns.append(VulnerabilityResult(**vuln))
                else:
                    print(f"     [!] Filtered out false positive: {vuln.get('id')} at {vuln.get('file')}:{vuln.get('line')}")
            else:
                final_vulns.append(VulnerabilityResult(**vuln))

        # Compute severity counts
        severity_counts = {"Critical": 0, "High": 0, "Medium": 0, "Low": 0}
        for v in final_vulns:
            if v.severity in severity_counts:
                severity_counts[v.severity] += 1

        return ScanResponse(
            repo_url=request.repo_url,
            total_vulnerabilities=len(final_vulns),
            severity_counts=severity_counts,
            vulnerabilities=final_vulns,
        )

    except Exception as e:
        print(f"[!] Scan failed: {e}")
        raise HTTPException(status_code=500, detail=f"Scan failed: {str(e)}")

    finally:
        if repo_path:
            cleanup_repo(repo_path)


@app.post("/apply-fix", response_model=ApplyFixResponse)
async def apply_fix(request: ApplyFixRequest):
    from github_service import create_pull_request_fix
    try:
        print(f"[+] Generating PR for {request.file_path} in {request.repo_url}")
        pr_url = await create_pull_request_fix(
            request.repo_url,
            request.file_path,
            request.line,
            request.secure_code
        )
        print(f"     [+] PR Created: {pr_url}")
        return ApplyFixResponse(pr_url=pr_url)
    except Exception as e:
        print(f"[!] Apply fix failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ── Run ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
