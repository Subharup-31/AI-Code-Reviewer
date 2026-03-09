// ── Types ────────────────────────────────────────────────────────────────────

export interface AttackSimulation {
  payload: string;
  description: string;
}

export interface SecureFix {
  description: string;
  code: string;
}

export interface CVEInfo {
  cve_id: string;
  description: string;
}

export interface Vulnerability {
  id: string;
  file: string;
  line: number;
  issue: string;
  severity: "Critical" | "High" | "Medium" | "Low";
  cvss_score: number;
  tool: string;
  code_snippet: string;
  cwe: string[];
  cve: CVEInfo;
  explanation: string;
  attack_simulation: AttackSimulation;
  secure_fix: SecureFix;
}

export interface ScanResult {
  repo_url: string;
  total_vulnerabilities: number;
  severity_counts: Record<string, number>;
  vulnerabilities: Vulnerability[];
}

// ── API ──────────────────────────────────────────────────────────────────────

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

export async function scanRepo(repoUrl: string): Promise<ScanResult> {
  const response = await fetch(`${API_BASE}/scan-repo`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ repo_url: repoUrl }),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: "Scan failed" }));
    throw new Error(error.detail || "Failed to scan repository");
  }

  return response.json();
}

export async function healthCheck(): Promise<boolean> {
  try {
    const response = await fetch(`${API_BASE}/health`);
    return response.ok;
  } catch {
    return false;
  }
}
