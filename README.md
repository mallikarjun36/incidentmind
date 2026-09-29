# IncidentMind

An AI-powered incident response agent that uses Hindsight as persistent organizational memory to help engineers investigate production incidents using knowledge from previous incidents.

## Problem

Production incidents often involve recurring symptoms and failure patterns. Previous incidents may contain useful information about the affected service, symptoms, root causes, deployments, and resolutions.

When this information is not available during a new investigation, engineers may have to repeat parts of the investigation process.

IncidentMind explores how persistent agent memory can make relevant knowledge from previous incidents available during future incident investigations.

## Solution

IncidentMind uses Hindsight as its persistent memory layer.

When a new incident is submitted, IncidentMind uses information about the incident to retrieve relevant historical memories. After an incident is resolved, incident-related knowledge can be retained so that it can be recalled during future investigations.

The core memory loop is:

```text
New Incident
     |
     v
Hindsight RECALL
     |
     v
Relevant Historical Knowledge
     |
     v
Investigation
     |
     v
Resolution
     |
     v
Hindsight RETAIN
     |
     v
Persistent Organizational Memory
     |
     +------> Future Incidents
```

## Hindsight Integration

Hindsight is the central memory component of IncidentMind.

### RETAIN

Incident-related knowledge is retained in the IncidentMind Hindsight memory bank.

The prototype has successfully retained incident information including:

* Incident ID
* Service
* Symptoms
* Deployment
* Root cause
* Resolution

### RECALL

When investigating a new incident, IncidentMind constructs a Hindsight recall query from incident information including:

* Service
* Severity
* Symptoms
* Deployment

Hindsight then returns relevant historical memories.

During testing, the prototype successfully recalled information related to a previous `payment-api` incident, including database connection exhaustion, a database connection leak, and the associated resolution.

## Current Architecture

```text
                         INCIDENTMIND

                    +-------------------+
                    |   Incident Input  |
                    +---------+---------+
                              |
                              v
                    +-------------------+
                    |      FastAPI      |
                    |      Backend      |
                    +---------+---------+
                              |
                              v
                    +-------------------+
                    |  Investigation    |
                    |     Service       |
                    +---------+---------+
                              |
                              v
                    +-------------------+
                    | Hindsight RECALL  |
                    +---------+---------+
                              |
                              v
                    +-------------------+
                    | Historical Memory |
                    +---------+---------+
                              |
                              v
                    +-------------------+
                    |   Investigation   |
                    +---------+---------+
                              |
                              v
                    +-------------------+
                    | Hindsight RETAIN  |
                    +---------+---------+
                              |
                              v
                    +-------------------+
                    | Persistent Memory |
                    +-------------------+
```

## Example Incident

An incident can contain information such as:

```json
{
  "incident_id": "INC-1024",
  "service": "payment-api",
  "severity": "SEV-1",
  "symptoms": [
    "high latency",
    "18% error rate",
    "database connection exhaustion"
  ],
  "deployment": "v2.4.3"
}
```

IncidentMind uses these details to construct a query for historical incident knowledge.

## Example Retained Knowledge

The prototype has retained an incident with information similar to:

```text
Incident: INC-0971
Service: payment-api

Symptoms:
- high latency
- high error rate
- database connection exhaustion

Deployment:
v2.4.3

Root cause:
database connection leak

Resolution:
correct connection lifecycle and apply the required deployment fix
```

Hindsight recall successfully returned related memories from this incident during prototype testing.

## Technology Stack

* Python 3.13.7
* FastAPI
* Uvicorn
* Hindsight
* `hindsight_client`
* `python-dotenv`
* Swagger / OpenAPI
* GitHub

## Project Structure

```text
incidentmind/
└── backend/
    ├── .venv/
    ├── app/
    │   ├── __init__.py
    │   ├── main.py
    │   ├── models.py
    │   ├── hindsight_service.py
    │   ├── analysis_service.py
    │   └── investigation_service.py
    ├── .env
    ├── test_hindsight.py
    ├── .gitignore
    └── README.md
```

> Do not commit `.venv/` or `.env` to the repository.

## Current API

### Health Check

```http
GET /health
```

Returns the backend health status.

### Root Endpoint

```http
GET /
```

Returns a basic message confirming that the IncidentMind backend is running.

### Incident Recall

```http
POST /incidents/recall
```

Accepts incident information and constructs a Hindsight recall query.

The current incident model includes:

* `incident_id`
* `service`
* `severity`
* `symptoms`
* `deployment`

## Running the Backend

Create a Python virtual environment, install the project dependencies, configure the required environment variables, and start the FastAPI application using Uvicorn.

Once the server is running, the FastAPI Swagger/OpenAPI interface is available at:

```text
http://127.0.0.1:8001/docs
```

## Environment Variables

Sensitive configuration such as Hindsight credentials must be supplied through environment variables.

Do not commit API keys or other secrets to the repository.

Provide an `.env.example` file containing the required variable names without actual credentials.

## Current Status

The current prototype has verified:

* FastAPI backend
* Hindsight Cloud connection
* IncidentMind Hindsight memory bank
* Hindsight RETAIN
* Hindsight RECALL
* Incident recall API
* Initial investigation service
* GitHub repository

The LLM-powered investigation workflow and final user-facing dashboard are still being developed.

## Limitations

The current prototype is backend-focused.

The final LLM-powered investigation flow and user-facing dashboard should only be described as completed after they have been implemented and tested.

## Future Work

Planned improvements include:

* LLM integration for investigation generation
* More structured investigation reasoning
* Root-cause analysis
* Resolution/runbook recommendations
* A user-facing incident investigation dashboard
* An end-to-end demonstration showing how retained knowledge influences future investigations

## Why Hindsight Matters

The purpose of using Hindsight is not simply to store incident records.

The intended workflow is for IncidentMind to accumulate knowledge from previous incidents and make relevant knowledge available during future investigations.

This creates a persistent memory loop:

```text
Incident
   ↓
Retain knowledge
   ↓
Historical memory
   ↓
Recall relevant knowledge
   ↓
Investigate a new incident
   ↓
Retain new knowledge
```

The project therefore uses Hindsight as a central part of the incident investigation workflow rather than as a separate storage component.
