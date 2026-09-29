from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .models import Incident
from .hindsight_service import recall_incidents
from .analysis_service import analyze_incident
from .investigation_service import investigate_incident
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