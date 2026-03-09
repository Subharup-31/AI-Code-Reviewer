"""
AI Engine — LLM-powered vulnerability analysis using Google Gemini 2.5-flash.
"""

import os
import json
import httpx
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
MODEL_NAME = "gemini-2.5-flash"
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent?key={GEMINI_API_KEY}"


ANALYSIS_PROMPT = """You are a senior cybersecurity expert. Analyze the following vulnerability found in a codebase.

**Vulnerability Type:** {issue}
**File:** {file}
**Line:** {line}
**Code Snippet:**
```
{code_snippet}
```

**Context from NVD (National Vulnerability Database):**
{nvd_context}

Provide your analysis in the following JSON format (return ONLY valid JSON, no markdown):
{{
  "is_false_positive": <boolean>, // Set to true ONLY if you are absolutely certain, based on the code snippet context provided, that this is a false positive (e.g., test code, securely sanitized input, or a misidentification by the static analyzer). Otherwise, set to false.
  "explanation": "A highly accurate explanation of the security issue. You MUST explicitly state the most applicable **OWASP Top 10** category (e.g., A01:2021-Broken Access Control). Cross-reference the vulnerability with the provided **NVD Context** and mention relevant CVEs to explain why it is dangerous. Use Markdown bolding (**text**) to highlight the OWASP category and CVE references.",
  "attack_simulation": {{
    "payload": "Provide a concrete, actionable attack payload. If an exact payload cannot be determined, provide a conceptual but highly specific representation (e.g., `' OR 1=1 --` or `<script>alert('XSS')</script>`). Do NOT leave this blank.",
    "description": "Provide a detailed, step-by-step technical explanation of how an attacker would deploy this payload to exploit the vulnerability."
  }},
  "secure_fix": {{
    "description": "Explanation of the recommended fix, adhering to secure coding guidelines.",
    "code": "The corrected code snippet with the vulnerability fixed"
  }}
}}
"""

async def analyze_vulnerability(vuln: dict) -> dict:
    """
    Send vulnerability data to Gemini and return AI analysis.
    Returns explanation, attack simulation, and secure fix.
    """
    if not GEMINI_API_KEY:
        return _fallback_analysis(vuln)

    try:
        prompt = ANALYSIS_PROMPT.format(
            issue=vuln.get("issue", "Unknown"),
            file=vuln.get("file", "unknown"),
            line=vuln.get("line", 0),
            code_snippet=vuln.get("code_snippet", "No code available"),
            nvd_context=vuln.get("cve", {}).get("nvd_context", "No NVD context available."),
        )

        payload = {
            "contents": [{"parts": [{"text": prompt}]}]
        }
        async with httpx.AsyncClient(timeout=60.0) as client:
            resp = await client.post(GEMINI_API_URL, json=payload)
            resp.raise_for_status()
            data = resp.json()
            text = data["candidates"][0]["content"]["parts"][0]["text"].strip()

        # Strip markdown code fences if present (handles ``` and ```json)
        if text.startswith("```"):
            # Remove the opening fence + optional language tag (e.g. ```json)
            lines = text.split("\n")
            text = "\n".join(lines[1:])  # drop first line (```json or ```)
            if text.endswith("```"):
                text = text[:-3]
            text = text.strip()

        analysis = json.loads(text)

        return {
            "is_false_positive": analysis.get("is_false_positive", False),
            "explanation": analysis.get("explanation", "Analysis unavailable"),
            "attack_simulation": analysis.get("attack_simulation", {}),
            "secure_fix": analysis.get("secure_fix", {}),
        }
    except json.JSONDecodeError:
        # If JSON parsing fails, use the raw text
        return {
            "is_false_positive": False,
            "explanation": text if 'text' in locals() else "Analysis unavailable",
            "attack_simulation": {"payload": "N/A", "description": "Could not parse AI response"},
            "secure_fix": {"description": "Could not parse AI response", "code": ""},
        }
    except Exception as e:
        print(f"[!] AI Engine error: {e}")
        return _fallback_analysis(vuln)


def _fallback_analysis(vuln: dict) -> dict:
    """Provide a basic analysis when AI is unavailable."""
    issue = vuln.get("issue", "Security vulnerability")
    return {
        "explanation": f"A {issue} vulnerability was detected. This type of issue "
                       f"can lead to unauthorized access, data exposure, or system compromise. "
                       f"Please refer to the applicable **OWASP Top 10** category for more context.",
        "attack_simulation": {
            "payload": "Example payload depends on vulnerability type",
            "description": f"An attacker could exploit this {issue} vulnerability to "
                          f"compromise the application's security posture.",
        },
        "secure_fix": {
            "description": f"Review and remediate the {issue} issue by following "
                          f"OWASP secure coding guidelines.",
            "code": "# Refer to OWASP guidelines for secure implementation",
        },
    }
