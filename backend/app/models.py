from pydantic import BaseModel


class Incident(BaseModel):
    incident_id: str
    service: str
    severity: str
    symptoms: list[str]
    deployment: str | None = None


class IncidentFeedback(BaseModel):
    incident_id: str
    feedback: str