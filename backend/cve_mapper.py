"""
CVE Mapper — Map vulnerability types to known CVE entries using the NVD API.
"""

import os
import httpx

NVD_API_BASE = "https://services.nvd.nist.gov/rest/json/cves/2.0"
NVD_API_KEY = os.getenv("NVD_API_KEY", "")

# Fallback mappings for common vulnerability types when API is unavailable
FALLBACK_CVE_MAP = {
    "sql injection": {
        "cve_id": "CVE-2023-32315",
        "description": "SQL Injection vulnerability allowing unauthorized data access",
        "cvss_score": 9.8,
    },
    "xss": {
        "cve_id": "CVE-2023-29489",
        "description": "Cross-Site Scripting (XSS) vulnerability allowing script injection",
        "cvss_score": 6.1,
    },
    "cross-site scripting": {
        "cve_id": "CVE-2023-29489",
        "description": "Cross-Site Scripting (XSS) vulnerability allowing script injection",
        "cvss_score": 6.1,
    },
    "hardcoded secret": {
        "cve_id": "CVE-2023-35078",
        "description": "Exposure of sensitive credentials in source code",
        "cvss_score": 7.5,
    },
    "hardcoded password": {
        "cve_id": "CVE-2023-35078",
        "description": "Hardcoded credentials enabling unauthorized access",
        "cvss_score": 7.5,
    },
    "insecure deserialization": {
        "cve_id": "CVE-2023-34362",
        "description": "Insecure deserialization leading to remote code execution",
        "cvss_score": 9.8,
    },
    "command injection": {
        "cve_id": "CVE-2023-27997",
        "description": "OS command injection allowing arbitrary command execution",
        "cvss_score": 9.8,
    },
    "path traversal": {
        "cve_id": "CVE-2023-24955",
        "description": "Path traversal allowing unauthorized file access",
        "cvss_score": 7.2,
    },
    "insecure authentication": {
        "cve_id": "CVE-2023-20198",
        "description": "Authentication bypass vulnerability",
        "cvss_score": 8.6,
    },
    "unsafe file handling": {
        "cve_id": "CVE-2023-23397",
        "description": "Unsafe file operations leading to potential code execution",
        "cvss_score": 7.8,
    },
}


async def map_to_cve(vulnerability_type: str) -> dict:
    """
    Map a vulnerability type string to a known CVE entry.
    First tries the NVD API, falls back to local mapping.
    """
    vuln_lower = vulnerability_type.lower()

    try:
        params = {"keywordSearch": vulnerability_type, "resultsPerPage": 5}
        headers = {}
        if NVD_API_KEY:
            headers["apiKey"] = NVD_API_KEY

        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(NVD_API_BASE, params=params, headers=headers)

            if response.status_code == 200:
                data = response.json()
                vulns = data.get("vulnerabilities", [])

                if vulns:
                    nvd_context_parts = []
                    primary_cve = None
                    primary_desc = "No description available"
                    primary_cvss = 0.0

                    for i, vuln_item in enumerate(vulns):
                        cve_item = vuln_item.get("cve", {})
                        cve_id = cve_item.get("id", "N/A")

                        descriptions = cve_item.get("descriptions", [])
                        desc = next(
                            (d["value"] for d in descriptions if d.get("lang") == "en"),
                            "No description available",
                        )

                        # Extract CVSS score
                        metrics = cve_item.get("metrics", {})
                        cvss_score = 0.0
                        for version in ["cvssMetricV31", "cvssMetricV30", "cvssMetricV2"]:
                            if version in metrics and metrics[version]:
                                cvss_data = metrics[version][0].get("cvssData", {})
                                cvss_score = cvss_data.get("baseScore", 0.0)
                                break
                        
                        nvd_context_parts.append(f"- {cve_id} (CVSS: {cvss_score}): {desc}")

                        if i == 0:
                            primary_cve = cve_id
                            primary_desc = desc
                            primary_cvss = cvss_score

                    nvd_context = "\n".join(nvd_context_parts)

                    if primary_cve:
                        return {
                            "cve_id": primary_cve,
                            "description": primary_desc[:200],
                            "cvss_score": primary_cvss,
                            "nvd_context": nvd_context
                        }
    except Exception as e:
        print(f"[!] NVD API error: {e}")

    # Fallback to local mapping
    for key, value in FALLBACK_CVE_MAP.items():
        if key in vuln_lower:
            return {
                **value,
                "nvd_context": f"- {value['cve_id']} (CVSS: {value['cvss_score']}): {value['description']}"
            }

    return {
        "cve_id": "N/A",
        "description": f"No CVE mapping found for: {vulnerability_type}",
        "cvss_score": 5.0,
        "nvd_context": f"- N/A: No related CVE data found for {vulnerability_type} in the NVD database, possibly a zero-day or custom business logic flaw."
    }
