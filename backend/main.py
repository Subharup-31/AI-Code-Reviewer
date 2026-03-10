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

from github_service import fetch_repo, fetch_pr_files, cleanup_repo
from scanner import run_semgrep, run_bandit, run_pip_audit, run_npm_audit
from vulnerability_parser import parse_all, parse_pylint
from cve_mapper import map_to_cve
from cvss_service import assign_cvss
from ai_engine import analyze_vulnerability
from bug_detector import run_pylint, scan_for_bugs

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
    confidence_score: int = 50
    exploitability: str = "Medium"
    mitigations_present: str = "None detected"
    corroborated: bool = False        # True when ≥2 tools flagged same location
    finding_type: str = "security"    # "security" | "bug"
    explanation: str = ""
    attack_simulation: AttackSimulation = AttackSimulation()
    secure_fix: SecureFix = SecureFix()


class ScanResponse(BaseModel):
    repo_url: str
    total_vulnerabilities: int        # security + bugs combined
    security_count: int = 0           # security findings only
    bug_count: int = 0                # code bug findings only
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

        # Step 2: Scan — SAST + dependency + bug scanners
        print("[2/6] Running security + bug scanners...")
        semgrep_raw = run_semgrep(repo_path)
        bandit_raw = run_bandit(repo_path)
        # Dependency + Pylint scanners run via threadpool (subprocess, non-blocking)
        loop = asyncio.get_event_loop()
        pip_audit_raw, npm_audit_raw, pylint_raw = await asyncio.gather(
            loop.run_in_executor(None, run_pip_audit, repo_path),
            loop.run_in_executor(None, run_npm_audit, repo_path),
            loop.run_in_executor(None, run_pylint, repo_path),
        )

        # Step 3: Parse static findings (security + dependencies + Pylint bugs)
        print("[3/6] Parsing scan results...")
        vulnerabilities = parse_all(
            semgrep_raw, bandit_raw, repo_path,
            pip_audit_raw=pip_audit_raw,
            npm_audit_raw=npm_audit_raw,
        )
        # Add Pylint bug findings
        pylint_bugs = parse_pylint(pylint_raw, repo_path)
        vulnerabilities = vulnerabilities + pylint_bugs
        print(f"     Found {len(vulnerabilities)} total findings "
              f"({len(pylint_bugs)} Pylint bugs)")

        # Step 4 & 5: CVE Mapping + CVSS Scoring
        # Pass CWE IDs from scanner metadata — enables precise NVD lookup by weakness class
        print("[4/6] Mapping CVEs and assigning CVSS scores...")
        enriched_vulns = []
        for vuln in vulnerabilities:
            cve_data = await map_to_cve(vuln.get("issue", ""), cwe_ids=vuln.get("cwe", []))
            scored_vuln = assign_cvss(vuln, cve_data)
            enriched_vulns.append(scored_vuln)

        # Separate deterministic dependency findings from SAST findings
        dep_vulns = [v for v in enriched_vulns if v.get("source") == "dependency"]
        sast_vulns = [v for v in enriched_vulns if v.get("source") != "dependency"]

        # Step 6: AI Analysis — SAST findings only (dep findings are already 100% accurate)
        print(f"[5/6] Running AI analysis on {len(sast_vulns)} SAST findings "
              f"({len(dep_vulns)} dependency findings bypass AI — deterministic)...")
        semaphore = asyncio.Semaphore(10)

        async def _analyze_with_limit(v: dict) -> dict:
            async with semaphore:
                return await analyze_vulnerability(v)

        ai_tasks = [_analyze_with_limit(v) for v in sast_vulns]
        ai_results = await asyncio.gather(*ai_tasks, return_exceptions=True)

        # Merge AI results — filter false positives and low-confidence noise
        print("[6/6] Assembling final results...")
        CONFIDENCE_THRESHOLD = 35
        final_vulns = []
        fp_count = 0
        low_conf_count = 0

        for i, vuln in enumerate(sast_vulns):
            if i < len(ai_results) and not isinstance(ai_results[i], Exception):
                ai_data = ai_results[i]
                confidence = int(ai_data.get("confidence_score", 50))

                if ai_data.get("is_false_positive"):
                    fp_count += 1
                    print(f"     [FP] {vuln.get('id')} at {vuln.get('file')}:{vuln.get('line')} — filtered by AI")
                    continue
                if confidence < CONFIDENCE_THRESHOLD:
                    low_conf_count += 1
                    print(f"     [LOW-CONF {confidence}] {vuln.get('id')} at {vuln.get('file')}:{vuln.get('line')} — filtered")
                    continue

                vuln["confidence_score"] = confidence
                vuln["exploitability"] = ai_data.get("exploitability", "Medium")
                vuln["mitigations_present"] = ai_data.get("mitigations_present", "None detected")
                vuln["explanation"] = ai_data.get("explanation", "")
                vuln["attack_simulation"] = ai_data.get("attack_simulation", {})
                vuln["secure_fix"] = ai_data.get("secure_fix", {})
                final_vulns.append(VulnerabilityResult(**vuln))
            else:
                vuln.setdefault("confidence_score", 50)
                vuln.setdefault("exploitability", "Medium")
                vuln.setdefault("mitigations_present", "Unknown — AI unavailable")
                final_vulns.append(VulnerabilityResult(**vuln))

        # Dependency findings: add directly — no AI filtering needed
        for v in dep_vulns:
            v.setdefault("finding_type", "security")
            final_vulns.append(VulnerabilityResult(**v))

        print(f"     Filtered: {fp_count} false positives, {low_conf_count} low-confidence findings")
        print(f"     Remaining: {len(final_vulns)} confirmed security findings")

        # ── AI Bug Sweep ────────────────────────────────────────────────────────
        # Run per-file AI bug detection on source files already flagged by SAST
        # (plus any small remaining source files up to the file cap).
        print("[+] Running AI bug detection sweep...")
        sast_files = {v.get("file", "") for v in sast_vulns}
        ai_bugs = await scan_for_bugs(repo_path, sast_files)
        for bug in ai_bugs:
            bug.setdefault("finding_type", "bug")
            final_vulns.append(VulnerabilityResult(**bug))
        print(f"     AI bug sweep: {len(ai_bugs)} bugs detected")

        # ── Final assembly ──────────────────────────────────────────────────────
        # Sort: security findings by CVSS + confidence; bugs by severity + confidence
        def _sort_key(v: VulnerabilityResult) -> tuple:
            sev_order = {"Critical": 4, "High": 3, "Medium": 2, "Low": 1}
            if v.finding_type == "security":
                return (1, v.cvss_score, v.confidence_score)
            return (0, sev_order.get(v.severity, 0), v.confidence_score)

        final_vulns.sort(key=_sort_key, reverse=True)

        severity_counts = {"Critical": 0, "High": 0, "Medium": 0, "Low": 0}
        security_count = 0
        bug_count = 0
        for v in final_vulns:
            if v.severity in severity_counts:
                severity_counts[v.severity] += 1
            if v.finding_type == "bug":
                bug_count += 1
            else:
                security_count += 1

        return ScanResponse(
            repo_url=request.repo_url,
            total_vulnerabilities=len(final_vulns),
            security_count=security_count,
            bug_count=bug_count,
            severity_counts=severity_counts,
            vulnerabilities=final_vulns,
        )

    except Exception as e:
        print(f"[!] Scan failed: {e}")
        raise HTTPException(status_code=500, detail=f"Scan failed: {str(e)}")

    finally:
        if repo_path:
            cleanup_repo(repo_path)


class ScanPRRequest(BaseModel):
    pr_url: str  # e.g. https://github.com/owner/repo/pull/123


@app.post("/scan-pr", response_model=ScanResponse)
async def scan_pr(request: ScanPRRequest):
    """
    PR-targeted scan — mirrors how CodeRabbit works.

    Instead of scanning the entire repository, this endpoint:
    1. Fetches only the files changed in the PR (via GitHub API)
    2. Runs full Semgrep + Bandit analysis on those files only
    3. Filters findings to lines touched by the PR diff ± 10 lines
    4. Runs the same two-pass AI validation pipeline

    Benefits vs full-repo scan:
    - Much smaller surface area → faster and more focused
    - Full file content available → AI sees complete function context
    - Findings are directly actionable (developer just wrote that code)
    - False positive rate drops because test files and unrelated legacy
      code are naturally excluded
    """
    repo_path = None
    try:
        print(f"[PR-SCAN] Fetching changed files from: {request.pr_url}")
        repo_path, changed_files = await fetch_pr_files(request.pr_url)

        # Build a set of (file, line_range) touched by the PR diff
        # so we can filter findings to only PR-relevant lines
        pr_touched: dict[str, set[int]] = {}
        for f in changed_files:
            filename = f.get("filename", "")
            patch = f.get("patch", "")
            touched_lines: set[int] = set()
            if patch:
                # Parse unified diff @@ -old +new,count @@ headers
                import re
                for match in re.finditer(r"@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@", patch):
                    start = int(match.group(1))
                    count = int(match.group(2)) if match.group(2) else 1
                    for line in range(start, start + count + 10):  # ± 10 line window
                        touched_lines.add(line)
            pr_touched[filename] = touched_lines

        print(f"[PR-SCAN] Running scanners on {len(changed_files)} changed files...")
        semgrep_raw = run_semgrep(repo_path)
        bandit_raw = run_bandit(repo_path)

        vulnerabilities = parse_all(semgrep_raw, bandit_raw, repo_path)
        print(f"[PR-SCAN] {len(vulnerabilities)} raw findings before PR filtering")

        # Filter to only findings in PR-touched lines
        pr_vulns = []
        for v in vulnerabilities:
            fname = v.get("file", "")
            line = v.get("line", 0)
            touched = pr_touched.get(fname, set())
            # If we have diff data, restrict to touched lines; otherwise keep all
            if not touched or line in touched:
                pr_vulns.append(v)

        print(f"[PR-SCAN] {len(pr_vulns)} findings in PR-changed lines")

        # CVE mapping + CVSS scoring
        enriched_vulns = []
        for vuln in pr_vulns:
            cve_data = await map_to_cve(vuln.get("issue", ""), cwe_ids=vuln.get("cwe", []))
            enriched_vulns.append(assign_cvss(vuln, cve_data))

        # Two-pass AI validation on all PR findings
        semaphore = asyncio.Semaphore(10)

        async def _analyze_limited(v: dict) -> dict:
            async with semaphore:
                return await analyze_vulnerability(v)

        ai_results = await asyncio.gather(
            *[_analyze_limited(v) for v in enriched_vulns],
            return_exceptions=True,
        )

        CONFIDENCE_THRESHOLD = 35
        final_vulns = []
        fp_count = low_conf_count = 0

        for i, vuln in enumerate(enriched_vulns):
            if i < len(ai_results) and not isinstance(ai_results[i], Exception):
                ai_data = ai_results[i]
                confidence = int(ai_data.get("confidence_score", 50))
                if ai_data.get("is_false_positive"):
                    fp_count += 1
                    continue
                if confidence < CONFIDENCE_THRESHOLD:
                    low_conf_count += 1
                    continue
                vuln.update({
                    "confidence_score": confidence,
                    "exploitability": ai_data.get("exploitability", "Medium"),
                    "mitigations_present": ai_data.get("mitigations_present", "None detected"),
                    "explanation": ai_data.get("explanation", ""),
                    "attack_simulation": ai_data.get("attack_simulation", {}),
                    "secure_fix": ai_data.get("secure_fix", {}),
                })
                final_vulns.append(VulnerabilityResult(**vuln))
            else:
                vuln.setdefault("confidence_score", 50)
                vuln.setdefault("exploitability", "Medium")
                vuln.setdefault("mitigations_present", "Unknown — AI unavailable")
                final_vulns.append(VulnerabilityResult(**vuln))

        print(f"[PR-SCAN] Filtered {fp_count} FP + {low_conf_count} low-conf → {len(final_vulns)} confirmed")
        final_vulns.sort(key=lambda v: (v.cvss_score, v.confidence_score), reverse=True)

        severity_counts = {"Critical": 0, "High": 0, "Medium": 0, "Low": 0}
        for v in final_vulns:
            if v.severity in severity_counts:
                severity_counts[v.severity] += 1

        return ScanResponse(
            repo_url=request.pr_url,
            total_vulnerabilities=len(final_vulns),
            severity_counts=severity_counts,
            vulnerabilities=final_vulns,
        )

    except Exception as e:
        print(f"[!] PR scan failed: {e}")
        raise HTTPException(status_code=500, detail=f"PR scan failed: {str(e)}")

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
