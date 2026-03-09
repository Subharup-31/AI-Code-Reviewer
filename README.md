# VulnGuard AI 🛡️

AI-powered platform that scans GitHub repositories for security vulnerabilities, simulates cyber attacks, and generates secure code fixes.

![Tech Stack](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white)
![Next.js](https://img.shields.io/badge/Next.js-000000?style=flat&logo=next.js&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=flat&logo=typescript&logoColor=white)

## Features

- **GitHub Repository Scanning** — Clone and analyze any public GitHub repo
- **Vulnerability Detection** — Semgrep + Bandit static analysis
- **CVE Mapping** — Automatic mapping to known CVEs via NVD API
- **CVSS Scoring** — Severity classification (Critical/High/Medium/Low)
- **AI Attack Simulation** — Gemini 2.5-Flash simulates exploitation scenarios
- **AI Fix Recommendation** — Generates production-ready secure code fixes
- **Security Dashboard** — Charts, heatmaps, and detailed vulnerability reports

## Project Structure

```
├── backend/
│   ├── main.py                  # FastAPI app + /scan-repo endpoint
│   ├── github_service.py        # Clone GitHub repositories
│   ├── scanner.py               # Run Semgrep & Bandit
│   ├── vulnerability_parser.py  # Parse & normalize scan results
│   ├── cve_mapper.py            # NVD CVE API integration
│   ├── cvss_service.py          # CVSS severity scoring
│   ├── ai_engine.py             # Gemini 2.5-Flash AI analysis
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   └── src/
│       ├── app/
│       │   ├── page.tsx           # Landing page
│       │   ├── scan/page.tsx      # Scan input page
│       │   ├── dashboard/page.tsx # Results dashboard
│       │   ├── layout.tsx         # Root layout with nav
│       │   └── globals.css        # Design system
│       ├── components/
│       │   ├── RepoInput.tsx      # GitHub URL input
│       │   ├── VulnerabilityTable.tsx  # Sortable results table
│       │   ├── SeverityChart.tsx       # Chart.js charts
│       │   └── RiskHeatmap.tsx         # File risk heatmap
│       └── lib/
│           └── api.ts             # API client + types
```

## Prerequisites

- **Python 3.10+**
- **Node.js 18+**
- **Git**
- **Semgrep** — `pip install semgrep`
- **Bandit** — `pip install bandit`
- **Gemini API Key** — Get one at [Google AI Studio](https://aistudio.google.com/apikey)

## Setup & Run

### 1. Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY

# Run server
uvicorn main:app --reload --port 8000
```

### 2. Frontend

```bash
cd frontend

# Install dependencies
npm install

# Run dev server
npm run dev
```

### 3. Access

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## API Endpoint

### POST `/scan-repo`

```json
{
  "repo_url": "https://github.com/user/repo"
}
```

**Response:**

```json
{
  "repo_url": "https://github.com/user/repo",
  "total_vulnerabilities": 12,
  "severity_counts": { "Critical": 2, "High": 4, "Medium": 5, "Low": 1 },
  "vulnerabilities": [
    {
      "id": "B608",
      "file": "login.py",
      "line": 42,
      "issue": "SQL Injection",
      "severity": "Critical",
      "cvss_score": 9.8,
      "tool": "bandit",
      "code_snippet": "...",
      "cve": { "cve_id": "CVE-2023-32315", "description": "..." },
      "explanation": "AI explanation...",
      "attack_simulation": { "payload": "' OR '1'='1", "description": "..." },
      "secure_fix": { "description": "Use parameterized queries", "code": "..." }
    }
  ]
}
```

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | FastAPI, Python |
| Frontend | Next.js 15, TypeScript, TailwindCSS |
| Charts | Chart.js, react-chartjs-2 |
| Security | Semgrep, Bandit |
| AI | Google Gemini 2.5-Flash |
| CVE Data | NVD CVE API |

---

Built with 🛡️ for hackathon by VulnGuard AI team
