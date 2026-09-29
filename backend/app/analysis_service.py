from .hindsight_service import recall_incidents


def analyze_incident(
    incident_id: str,
    service: str,
    severity: str,
    symptoms: list[str],
    deployment: str | None,
):
    query = f"""
    Find previous production incidents relevant to this incident.

    Current incident:
    Incident ID: {incident_id}
    Service: {service}
    Severity: {severity}
    Symptoms: {", ".join(symptoms)}
    Deployment: {deployment or "unknown"}

    Look especially for:
    - similar symptoms
    - the same service
    - database connection problems
    - high latency
    - high error rates
    - deployment-related failures
    - previous root causes
    - previous resolutions

    Return historical incidents that could help investigate the current incident.
    """

    results = recall_incidents(query)

    return {
        "incident_id": incident_id,
        "service": service,
        "severity": severity,
        "historical_matches": results,
    }