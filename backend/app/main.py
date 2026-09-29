from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .models import Incident
#from .hindsight_service import recall_incidents
from .analysis_service import analyze_incident
from .investigation_service import investigate_incident
from .hindsight_service import recall_incidents, retain_incident
app = FastAPI(title="IncidentMind")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {
        "message": "IncidentMind backend is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/incidents/recall")
def recall_for_incident(incident: Incident):
    query = f"""
    Find previous incidents relevant to this incident.

    Service: {incident.service}
    Severity: {incident.severity}
    Symptoms: {", ".join(incident.symptoms)}
    Deployment: {incident.deployment or "unknown"}

    Return previous incidents that could help diagnose the current incident.
    """

    results = recall_incidents(query)

    return {
        "incident_id": incident.incident_id,
        "results": results,
    }
@app.post("/incidents/analyze")
def analyze_for_incident(incident: Incident):
    return analyze_incident(
        incident_id=incident.incident_id,
        service=incident.service,
        severity=incident.severity,
        symptoms=incident.symptoms,
        deployment=incident.deployment,
    )
@app.post("/incidents/investigate")
def investigate_for_incident(incident: Incident):
    return investigate_incident(
        incident_id=incident.incident_id,
        service=incident.service,
        severity=incident.severity,
        symptoms=incident.symptoms,
        deployment=incident.deployment,
    )
@app.post("/incidents/postmortem")
def record_postmortem(data: dict):
    incident_id = data.get("incident_id")
    service = data.get("service")
    severity = data.get("severity")
    symptoms = data.get("symptoms", [])
    root_cause = data.get("root_cause")
    resolution = data.get("resolution")
    runbook = data.get("runbook")
    runbook_worked = data.get("runbook_worked")
    notes = data.get("notes")

    if not incident_id:
        return {"success": False, "error": "incident_id is required"}

    if not service:
        return {"success": False, "error": "service is required"}

    if not root_cause:
        return {"success": False, "error": "root_cause is required"}

    if not resolution:
        return {"success": False, "error": "resolution is required"}

    symptoms_text = ", ".join(symptoms) if symptoms else "not recorded"

    memory_content = f"""
IncidentMind Post-Mortem

Incident ID: {incident_id}
Service: {service}
Severity: {severity or "unknown"}

Symptoms:
{symptoms_text}

Root Cause:
{root_cause}

Resolution:
{resolution}

Runbook:
{runbook or "No runbook recorded"}

Runbook Worked:
{"Yes" if runbook_worked else "No"}

Additional Notes:
{notes or "None"}

This incident has been resolved and recorded as organizational incident
knowledge for future investigations.
""".strip()

    try:
        retain_response = retain_incident(memory_content)

        return {
            "success": True,
            "incident_id": incident_id,
            "message": (
                "Post-mortem recorded successfully. "
                "IncidentMind can use this resolution as historical evidence "
                "for future similar incidents."
            ),
            "memory": memory_content,
            "hindsight_response": str(retain_response),
        }

    except Exception as exc:
        return {
            "success": False,
            "incident_id": incident_id,
            "error": str(exc),
        }