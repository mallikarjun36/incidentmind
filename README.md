# IncidentMind

## AI-Assisted Production Incident Investigation with Organizational Memory

IncidentMind is an AI-assisted production incident investigation system that gives engineering teams **organizational memory**.

When a production incident occurs, engineers often investigate the same types of failures repeatedly. IncidentMind helps solve this problem by retrieving relevant historical incidents, their root causes, resolutions, and runbooks from organizational memory.

The system uses **Hindsight** to remember previous incidents and learn from post-mortems. When a new incident occurs, IncidentMind searches that memory, presents relevant historical evidence, generates root-cause hypotheses, suggests investigation steps and recommended actions, and allows engineers to record the final resolution.

The result is a continuous learning loop:

```text
New Incident
     ↓
Historical Incident Recall
     ↓
Evidence-Based Investigation
     ↓
Root Cause Hypotheses
     ↓
Investigation Steps
     ↓
Recommended Actions
     ↓
Incident Resolution
     ↓
Post-Mortem
     ↓
Organizational Memory
     ↓
Future Incidents
```

---

# Features

## 1. Incident Intake

Engineers can provide the details of a production incident:

- Incident ID
- Service
- Severity
- Deployment
- Symptoms

Example:

```text
Incident ID: INC-2001
Service: payment-api
Severity: SEV-1
Deployment: v2.5.0

Symptoms:
- High latency
- High error rate
- Database connection exhaustion
```

---

## 2. Historical Incident Recall

IncidentMind searches organizational memory using Hindsight to find incidents that are relevant to the current incident.

For example, a new `payment-api` incident involving database connection exhaustion may retrieve historical incidents involving:

- Database connection leaks
- Connection pool exhaustion
- Similar deployments
- Similar service symptoms

This allows engineers to reuse knowledge from previous incidents instead of starting every investigation from scratch.

---

## 3. Historical Match

When relevant historical evidence is found, IncidentMind displays a historical match.

Example:

```text
Historical Match

Incident INC-1042 occurred in the payment-api service,
causing high latency, high error rates, and database
connection exhaustion.
```

The engineer can immediately see that the organization has experienced a similar problem before.

---

## 4. Root-Cause Hypotheses

IncidentMind uses the current incident together with retrieved historical evidence to generate possible root-cause hypotheses.

Example:

```text
1. Database connection exhaustion or connection lifecycle issue

2. Database connection/resource leak

3. Deployment-related regression

4. Database or downstream dependency latency
```

Each hypothesis is supported by historical evidence.

IncidentMind presents these as hypotheses rather than automatically claiming that one cause is definitely correct.

---

## 5. Supporting Evidence

For every investigation, IncidentMind displays historical evidence retrieved from organizational memory.

Example:

```text
The root cause of incident INC-1042 was a database
connection leak introduced by deployment v2.5.0.
```

This makes the investigation more transparent because engineers can see why a particular hypothesis was suggested.

---

## 6. Investigation Steps

IncidentMind provides practical investigation steps based on the current incident and historical evidence.

Example:

```text
- Check database connection pool utilization and active connections.
- Inspect recent deployment changes affecting database connection lifecycle.
- Compare current symptoms with retrieved historical incidents.
- Check application logs for connection timeout and pool exhaustion errors.
```

---

## 7. Recommended Actions

IncidentMind can provide remediation-oriented actions based on the investigation.

Example:

```text
- Correct connection lifecycle handling if a connection leak is confirmed.
- Roll back the latest deployment if evidence links the regression to that release.
- Restore database connection pool capacity after confirming the underlying cause.
```

These recommendations are intended to assist engineers during investigation and response.

---

## 8. Post-Mortem Recording

After the incident is resolved, engineers can record what actually happened.

The post-mortem includes:

- Root Cause
- Resolution
- Runbook Used
- Additional Notes

Example:

```text
Root Cause:
Database connection leak introduced by deployment v2.5.0.

Resolution:
Rolled back v2.5.0 and corrected connection lifecycle handling.

Runbook Used:
Database connection pool exhaustion recovery runbook.

Additional Notes:
Database connection utilization returned to normal after remediation.
```

---

## 9. Organizational Memory

The post-mortem information is stored in Hindsight.

This means the resolution of today's incident can become useful evidence for tomorrow's incident.

The learning loop is:

```text
Incident
   ↓
Investigation
   ↓
Resolution
   ↓
Post-Mortem
   ↓
Hindsight Memory
   ↓
Future Incident
   ↓
Historical Recall
```

This is the central concept behind IncidentMind.

---

# Architecture

```text
┌─────────────────────────────────────┐
│          React Frontend             │
│                                     │
│  Incident Input                     │
│  Investigation Report               │
│  Historical Evidence                │
│  Root Cause Hypotheses              │
│  Recommended Actions                │
│  Post-Mortem Recording              │
└──────────────────┬──────────────────┘
                   │
                   │ HTTP REST API
                   ▼
┌─────────────────────────────────────┐
│          FastAPI Backend             │
│                                     │
│  /incidents/recall                  │
│  /incidents/analyze                 │
│  /incidents/investigate             │
│                                     │
│  Investigation Service              │
│  Analysis Service                   │
│  AI Service                         │
│  Hindsight Service                  │
└──────────────────┬──────────────────┘
                   │
                   │
                   ▼
┌─────────────────────────────────────┐
│             Hindsight               │
│                                     │
│      Organizational Memory           │
│                                     │
│  Historical Incidents               │
│  Root Causes                        │
│  Resolutions                        │
│  Runbooks                           │
│  Post-Mortems                       │
└─────────────────────────────────────┘
```

---

# Project Structure

```text
incidentmind/
│
├── backend/
│   │
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── ai_service.py
│   │   ├── analysis_service.py
│   │   ├── hindsight_service.py
│   │   └── investigation_service.py
│   │
│   ├── test_hindsight.py
│   ├── requirements.txt
│   └── .env
│
├── frontend/
│   │
│   ├── public/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── main.jsx
│   │   └── assets/
│   │
│   ├── package.json
│   ├── package-lock.json
│   └── vite.config.js
│
└── README.md
```

---

# Technology Stack

## Frontend

- React
- Vite
- JavaScript
- CSS

## Backend

- Python
- FastAPI
- REST APIs
- Uvicorn

## Organizational Memory

- Hindsight
- Hindsight Recall
- Hindsight Retain

## Application Services

- Incident investigation service
- Analysis service
- AI service
- Hindsight service

---

# Requirements

Before running IncidentMind, install:

- Python 3.10 or newer
- Node.js 18 or newer
- npm
- Hindsight
- Hindsight API credentials

---

# Environment Configuration

The backend requires Hindsight configuration.

Create a `.env` file inside the `backend` directory:

```env
HINDSIGHT_BASE_URL=<your-hindsight-url>
HINDSIGHT_API_KEY=<your-hindsight-api-key>
HINDSIGHT_BANK_ID=<your-hindsight-bank-id>
```

Replace the values with your Hindsight configuration.

Do not commit API keys or other secrets to GitHub.

---

# Backend Setup

Open PowerShell in the project directory.

```powershell
cd C:\Users\<YOUR_USERNAME>\Desktop\incidentmind\backend
```

Create a Python virtual environment:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

Then activate again:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the backend dependencies:

```powershell
pip install -r requirements.txt
```

---

# Start the Backend

From the `backend` directory:

```powershell
python -m uvicorn app.main:app --reload --port 8001
```

The backend should start at:

```text
http://127.0.0.1:8001
```

You can verify the backend with:

```text
http://127.0.0.1:8001/
```

Health check:

```text
http://127.0.0.1:8001/health
```

FastAPI interactive API documentation:

```text
http://127.0.0.1:8001/docs
```

---

# Frontend Setup

Open a second PowerShell terminal.

Navigate to the frontend:

```powershell
cd C:\Users\<YOUR_USERNAME>\Desktop\incidentmind\frontend
```

Install the frontend dependencies:

```powershell
npm install
```

Start the Vite development server:

```powershell
npm run dev
```

The frontend should normally start at:

```text
http://localhost:5173
```

Open this address in Chrome.

---

# Running the Complete Application

IncidentMind requires two running processes.

## Terminal 1 — Backend

```powershell
cd C:\Users\<YOUR_USERNAME>\Desktop\incidentmind\backend
.\.venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --reload --port 8001
```

Backend:

```text
http://127.0.0.1:8001
```

API documentation:

```text
http://127.0.0.1:8001/docs
```

---

## Terminal 2 — Frontend

```powershell
cd C:\Users\<YOUR_USERNAME>\Desktop\incidentmind\frontend
npm run dev
```

Frontend:

```text
http://localhost:5173
```

Open the frontend URL in Chrome.

---

# API Endpoints

The FastAPI backend provides the following endpoints:

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Backend status |
| GET | `/health` | Health check |
| POST | `/incidents/recall` | Retrieve relevant historical incidents |
| POST | `/incidents/analyze` | Analyze an incident |
| POST | `/incidents/investigate` | Run the investigation workflow |

Interactive API documentation:

```text
http://127.0.0.1:8001/docs
```

---

# Example Incident

A useful demonstration incident is:

```text
Incident ID:
INC-2001

Service:
payment-api

Severity:
SEV-1

Deployment:
v2.5.0
```

Symptoms:

```text
High latency
High error rate
Database connection exhaustion
```

Click:

```text
Investigate Incident
```

IncidentMind sends the incident to the backend.

The backend searches Hindsight for relevant historical organizational memory.

---

# Example Historical Match

A historical incident may contain:

```text
Incident: INC-1042

Service: payment-api

Symptoms:
High latency
High error rates
Database connection exhaustion

Deployment:
v2.5.0
```

Another historical incident may contain:

```text
Incident: INC-0971

Service: payment-api

Root Cause:
Database connection leak

Impact:
Connection pool exhaustion

Deployment:
v2.4.3
```

IncidentMind uses these memories as evidence during the current investigation.

---

# Example Investigation Output

The investigation may produce:

## Historical Match

```text
Relevant organizational memory was found.
```

## Root Cause Hypotheses

```text
1. Database connection exhaustion or connection lifecycle issue

2. Database connection/resource leak

3. Deployment-related regression

4. Database or downstream dependency latency
```

## Investigation Steps

```text
1. Check database connection pool utilization.
2. Inspect recent deployment changes.
3. Compare current symptoms with historical incidents.
4. Check application logs for connection timeout errors.
```

## Recommended Actions

```text
1. Correct connection lifecycle handling if a leak is confirmed.
2. Roll back the latest deployment if evidence links the regression to it.
3. Restore database connection capacity after confirming the cause.
```

---

# Post-Mortem Learning

After resolving an incident, the engineer records the post-mortem.

Example:

```text
Root Cause:
Database connection leak introduced by deployment v2.5.0.

Resolution:
Rolled back deployment and fixed connection lifecycle handling.

Runbook Used:
Database connection pool exhaustion recovery runbook.

Additional Notes:
Connection utilization returned to normal after remediation.
```

This information is retained in Hindsight.

The next time a similar incident occurs, IncidentMind can retrieve the previous incident and its resolution.

---

# Why Hindsight?

Traditional incident investigation often depends on engineers remembering previous incidents or searching through scattered documentation.

IncidentMind uses Hindsight as organizational memory.

Instead of only asking:

```text
"What does the AI know about this problem?"
```

IncidentMind asks:

```text
"What has our organization experienced before?"
```

This allows the system to use organization-specific knowledge such as:

- Previous incidents
- Previous root causes
- Previous resolutions
- Previous runbooks
- Post-mortem information

---

# Learning Loop

The key differentiator of IncidentMind is the learning loop:

```text
┌─────────────────────┐
│   Production        │
│   Incident          │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Historical Recall   │
│ using Hindsight     │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Investigation       │
│ + Evidence          │
│ + Hypotheses        │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Incident Resolution │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Post-Mortem         │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Hindsight Memory    │
│ Updated             │
└──────────┬──────────┘
           │
           └───────────────┐
                           ↓
                    Future Incident
```

---

# Security

Do not commit secrets to the repository.

Keep credentials inside the local `.env` file:

```text
HINDSIGHT_API_KEY
HINDSIGHT_BASE_URL
HINDSIGHT_BANK_ID
```

The `.env` file should remain excluded from Git.

---

# Troubleshooting

## Backend does not start

Make sure the virtual environment is activated:

```powershell
.\.venv\Scripts\Activate.ps1
```

Then run:

```powershell
python -m uvicorn app.main:app --reload --port 8001
```

If port `8001` is already being used, stop the existing backend process or use another port.

---

## Frontend does not start

From the `frontend` directory:

```powershell
npm install
npm run dev
```

Then open:

```text
http://localhost:5173
```

---

## Backend is running but frontend cannot communicate with it

Verify the backend:

```text
http://127.0.0.1:8001/health
```

Expected response:

```json
{
  "status": "healthy"
}
```

Also verify that the frontend is running on:

```text
http://localhost:5173
```

---

# Demo Checklist

Before demonstrating IncidentMind:

```text
[ ] Hindsight credentials configured
[ ] Backend running
[ ] Frontend running
[ ] Hindsight memory contains historical incidents
[ ] Test incident ready
[ ] Historical match can be demonstrated
[ ] Investigation report displays correctly
[ ] Post-mortem can be recorded
```

Recommended demo incident:

```text
Service: payment-api
Severity: SEV-1
Deployment: v2.5.0

Symptoms:
- High latency
- High error rate
- Database connection exhaustion
```

---

# Project Goal

IncidentMind is designed to help engineering teams respond to production incidents faster by turning previous incident experience into reusable organizational knowledge.

The system connects:

```text
Past Experience
      +
Current Incident
      +
AI-Assisted Investigation
      +
Organizational Memory
```

into a continuous learning system for incident response.

---

# Summary

IncidentMind provides an end-to-end incident investigation workflow:

```text
Incident Intake
      ↓
Historical Incident Recall
      ↓
Historical Match
      ↓
Evidence Retrieval
      ↓
Root Cause Hypotheses
      ↓
Investigation Steps
      ↓
Recommended Actions
      ↓
Incident Resolution
      ↓
Post-Mortem
      ↓
Hindsight Organizational Memory
      ↓
Future Incident Investigation
```

**IncidentMind — Remember every incident. Learn from every resolution. Respond smarter next time.**