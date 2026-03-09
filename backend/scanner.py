"""
Scanner — Run Semgrep and Bandit static analysis tools.
Supports all popular programming languages through comprehensive Semgrep rulesets.
"""

import json
import subprocess
import sys


# Comprehensive Semgrep rulesets for multi-language coverage
SEMGREP_CONFIGS = [
    "p/security-audit",      # Broad security rules (all languages)
    "p/secrets",             # Hardcoded secrets, API keys, passwords
    "p/owasp-top-ten",       # OWASP Top 10 (injection, XSS, etc.)
    "p/cwe-top-25",          # CWE Top 25 Most Dangerous Software Errors
    "p/jwt",                 # JSON Web Token specific rules
    "p/ci",                  # CI/CD pipeline rules
    "p/dockerfile",          # Dockerfile best practices and security
    "p/terraform",           # Infrastructure as Code: Terraform
    "p/kubernetes",          # Kubernetes configurations
    "p/javascript",          # JavaScript-specific rules
    "p/typescript",          # TypeScript-specific rules
    "p/python",              # Python-specific rules
    "p/java",                # Java-specific rules
    "p/go",                  # Go-specific rules
    "p/ruby",                # Ruby-specific rules
    "p/php",                 # PHP-specific rules
    "p/csharp",              # C#-specific rules
    "p/rust",                # Rust-specific rules
    "p/scala",               # Scala-specific rules
    "p/kotlin",              # Kotlin-specific rules
    "p/swift",               # Swift-specific rules
    "p/c",                   # C/C++-specific rules
]


def run_semgrep(repo_path: str) -> dict:
    """
    Run Semgrep with multiple security rulesets for broad language coverage.
    Deduplicates findings across rulesets.
    """
    all_results = []
    seen_ids = set()

    for config in SEMGREP_CONFIGS:
        try:
            print(f"[semgrep] Running config: {config}")
            cmd = [
                sys.executable, "-m", "semgrep",
                "--config", config,
                "--json",
                "--no-git-ignore",
                "--timeout", "30",
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
            else:
                # Config may not apply to this language — skip silently
                pass

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
    """
    try:
        print(f"[bandit] Running on: {repo_path}")
        result = subprocess.run(
            [
                sys.executable, "-m", "bandit",
                "-r", repo_path,
                "-f", "json",
                "-ll",  # Report medium severity and above
            ],
            capture_output=True,
            text=True,
            timeout=300,
        )

        # Bandit outputs to stdout even on findings (exit code 1)
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
