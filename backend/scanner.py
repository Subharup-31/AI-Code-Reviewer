"""
Scanner — Run Semgrep and Bandit static analysis tools.
Supports all popular programming languages through comprehensive Semgrep rulesets.
"""

import glob as glob_module
import json
import os
import subprocess
import sys


# ── Semgrep rule packs ────────────────────────────────────────────────────────
#
# Ordering matters: high-precision packs first, broad packs last.
# Removed: p/ci (CI pipeline linting, not security vulnerabilities in code)
#          p/scala, p/kotlin, p/swift (very small packs, low signal-to-noise)
# Added:   p/trailofbits — Trail of Bits professional security rules (highest precision)
#          p/r2c-security-audit — Curated security audit rules by Semgrep's own team
#
SEMGREP_CONFIGS = [
    # ── Tier 1: Professional, high-precision packs ────────────────────────────
    "p/trailofbits",         # Trail of Bits curated rules — very low false-positive rate
    "p/r2c-security-audit",  # Semgrep's own curated security audit rules
    # ── Tier 2: Standard security frameworks ──────────────────────────────────
    "p/owasp-top-ten",       # OWASP Top 10 (injection, XSS, broken auth, etc.)
    "p/cwe-top-25",          # CWE Top 25 Most Dangerous Software Weaknesses
    "p/secrets",             # Hardcoded secrets, API keys, tokens, passwords
    "p/jwt",                 # JSON Web Token vulnerabilities
    # ── Tier 3: Infrastructure as Code ───────────────────────────────────────
    "p/dockerfile",          # Dockerfile security misconfigurations
    "p/terraform",           # Terraform IaC security issues
    "p/kubernetes",          # Kubernetes manifest security issues
    # ── Tier 4: Language-specific packs (cover popular languages only) ────────
    "p/javascript",          # JavaScript
    "p/typescript",          # TypeScript
    "p/python",              # Python
    "p/java",                # Java
    "p/go",                  # Go
    "p/ruby",                # Ruby
    "p/php",                 # PHP
    "p/csharp",              # C#
    "p/rust",                # Rust
    "p/c",                   # C / C++
    # ── Tier 5: Correctness / bug-class rules ─────────────────────────────────
    "p/default",             # Semgrep default pack — includes correctness + bug rules
    # ── Tier 6: Broad catch-all (run last to avoid duplicating Tier 1–5) ──────
    "p/security-audit",      # Broad multi-language security rules
]

# Directories that are almost entirely false-positive sources:
# - test / spec directories contain deliberately insecure code for testing
# - vendor / node_modules are third-party code not owned by the developer
# - build / dist are generated artefacts
# - migrations contain raw SQL that tools often misread as injection
EXCLUDE_DIRS = [
    "test", "tests", "__tests__", "spec", "specs",
    "mocks", "mock", "fixtures", "fixture",
    "node_modules", "vendor", "venv", ".venv", "env",
    "dist", "build", "target", "out", ".next", ".nuxt",
    "migrations", "migration",
    ".git", ".github",
]

# File name patterns to exclude (glob-style, matched against basename)
EXCLUDE_FILE_PATTERNS = [
    "*_test.go", "*_test.py", "*_spec.rb",
    "*.test.js", "*.test.ts", "*.test.jsx", "*.test.tsx",
    "*.spec.js", "*.spec.ts", "*.spec.jsx", "*.spec.tsx",
    "test_*.py", "conftest.py",
]


def run_semgrep(repo_path: str) -> dict:
    """
    Run Semgrep with high-precision security rulesets.

    Key accuracy improvements:
    - Test/mock/vendor directories are excluded — they are the #1 source of
      false positives in static analysis (deliberately insecure code, fixtures, etc.)
    - Trail of Bits + r2c-security-audit packs run first — much higher precision
      than the broad p/security-audit pack.
    - Deduplicates findings across all rule packs.
    """
    all_results = []
    seen_ids = set()

    # Build exclude-dir flags
    exclude_flags = []
    for d in EXCLUDE_DIRS:
        exclude_flags += ["--exclude-dir", d]
    for pattern in EXCLUDE_FILE_PATTERNS:
        exclude_flags += ["--exclude", pattern]

    for config in SEMGREP_CONFIGS:
        try:
            print(f"[semgrep] Running config: {config}")
            cmd = [
                sys.executable, "-m", "semgrep",
                "--config", config,
                "--json",
                "--no-git-ignore",
                "--timeout", "30",
                *exclude_flags,
                repo_path,
            ]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=120,
            )

            if result.stdout.strip():
                try:
                    data = json.loads(result.stdout)
                except json.JSONDecodeError:
                    print(f"[semgrep] {config}: failed to parse output")
                    continue

                results = data.get("results", [])
                # Deduplicate across configs
                for r in results:
                    key = f"{r.get('path', '')}:{r.get('start', {}).get('line', 0)}:{r.get('check_id', '')}"
                    if key not in seen_ids:
                        seen_ids.add(key)
                        all_results.append(r)

                new_count = len(results)
                if new_count > 0:
                    print(f"[semgrep] {config}: +{new_count} findings ({len(all_results)} total unique)")

        except subprocess.TimeoutExpired:
            print(f"[semgrep] {config}: timed out, skipping")
        except FileNotFoundError:
            print("[!] Semgrep not found. Install with: pip install semgrep")
            return {"results": [], "error": "semgrep not installed"}

    print(f"[semgrep] Total unique findings: {len(all_results)}")
    return {"results": all_results}


def run_bandit(repo_path: str) -> dict:
    """
    Run Bandit on the repository and return JSON results.
    Bandit only scans Python files — returns empty for non-Python repos.
    Test files are excluded to match Semgrep's exclusion policy.
    """
    # Build exclude paths for bandit (comma-separated directory names)
    exclude_paths = ",".join(EXCLUDE_DIRS)

    try:
        print(f"[bandit] Running on: {repo_path}")
        result = subprocess.run(
            [
                sys.executable, "-m", "bandit",
                "-r", repo_path,
                "-f", "json",
                "-ll",                      # Medium severity and above only
                "--exclude", exclude_paths, # Skip test/vendor dirs
            ],
            capture_output=True,
            text=True,
            timeout=300,
        )

        output = result.stdout.strip()
        if output:
            try:
                data = json.loads(output)
                count = len(data.get("results", []))
                print(f"[bandit] Found {count} results")
                return data
            except json.JSONDecodeError:
                print("[bandit] Failed to parse output")
                return {"results": []}

        print("[bandit] No findings (repo may have no Python files)")
        return {"results": []}
    except FileNotFoundError:
        print("[!] Bandit not found. Install with: pip install bandit")
        return {"results": [], "error": "bandit not installed"}
    except subprocess.TimeoutExpired:
        print("[!] Bandit scan timed out after 300s")
        return {"results": [], "error": "timeout"}


def run_pip_audit(repo_path: str) -> dict:
    """
    Run pip-audit against every requirements*.txt found in the repo.

    pip-audit queries the OSV (Open Source Vulnerabilities) database — findings
    are 100% deterministic: a package at a given version either has a published
    CVE/GHSA or it doesn't.  Zero false positives possible.
    """
    req_files = []
    for pattern in ["requirements*.txt", "**/requirements*.txt"]:
        req_files.extend(glob_module.glob(os.path.join(repo_path, pattern), recursive=True))

    if not req_files:
        print("[pip-audit] No requirements*.txt found — skipping")
        return {"results": []}

    all_vulns = []
    for req_file in req_files:
        try:
            print(f"[pip-audit] Scanning: {req_file}")
            result = subprocess.run(
                [
                    sys.executable, "-m", "pip_audit",
                    "--requirement", req_file,
                    "--format", "json",
                    "--no-deps",          # Direct deps only — transitive noise
                    "--skip-editable",    # Skip local editable installs
                ],
                capture_output=True,
                text=True,
                timeout=120,
            )
            output = result.stdout.strip()
            if output:
                data = json.loads(output)
                for dep in data.get("dependencies", []):
                    for v in dep.get("vulns", []):
                        all_vulns.append({
                            "package": dep.get("name", "unknown"),
                            "version": dep.get("version", "unknown"),
                            "vuln_id": v.get("id", "N/A"),
                            "description": v.get("description", ""),
                            "fix_versions": v.get("fix_versions", []),
                            "req_file": os.path.relpath(req_file, repo_path),
                        })
        except subprocess.TimeoutExpired:
            print(f"[pip-audit] {req_file}: timed out, skipping")
        except (FileNotFoundError, ModuleNotFoundError):
            print("[!] pip-audit not found — install with: pip install pip-audit")
            return {"results": [], "error": "pip-audit not installed"}
        except Exception as e:
            print(f"[pip-audit] Error scanning {req_file}: {e}")

    print(f"[pip-audit] Found {len(all_vulns)} dependency vulnerabilities")
    return {"results": all_vulns}


def run_npm_audit(repo_path: str) -> dict:
    """
    Run npm audit --json against every package-lock.json found in the repo.
    Reports moderate+ severity advisories only.

    Like pip-audit, these are CVE database lookups — 100% deterministic.
    """
    lockfiles = [
        f for f in glob_module.glob(os.path.join(repo_path, "**/package-lock.json"), recursive=True)
        if "node_modules" not in f
    ]

    if not lockfiles:
        print("[npm-audit] No package-lock.json found — skipping")
        return {"results": []}

    all_vulns = []
    for lockfile in lockfiles:
        lockdir = os.path.dirname(lockfile)
        try:
            print(f"[npm-audit] Scanning: {lockfile}")
            result = subprocess.run(
                ["npm", "audit", "--json"],
                capture_output=True,
                text=True,
                timeout=120,
                cwd=lockdir,
            )
            output = result.stdout.strip()
            if output:
                data = json.loads(output)
                for pkg_name, vuln_data in data.get("vulnerabilities", {}).items():
                    if vuln_data.get("severity", "low") == "low":
                        continue
                    for via in vuln_data.get("via", []):
                        if not isinstance(via, dict):
                            continue
                        fix_info = vuln_data.get("fixAvailable")
                        fix_ver = fix_info.get("version", "") if isinstance(fix_info, dict) else ""
                        all_vulns.append({
                            "package": pkg_name,
                            "version": vuln_data.get("range", "unknown"),
                            "vuln_id": str(via.get("source", "N/A")),
                            "description": via.get("title", ""),
                            "severity": vuln_data.get("severity", "high"),
                            "fix_versions": [fix_ver] if fix_ver else [],
                            "lockfile": os.path.relpath(lockfile, repo_path),
                        })
        except subprocess.TimeoutExpired:
            print(f"[npm-audit] {lockfile}: timed out, skipping")
        except FileNotFoundError:
            print("[!] npm not found — skipping npm audit")
            return {"results": [], "error": "npm not installed"}
        except Exception as e:
            print(f"[npm-audit] Error: {e}")

    print(f"[npm-audit] Found {len(all_vulns)} npm dependency vulnerabilities")
    return {"results": all_vulns}
