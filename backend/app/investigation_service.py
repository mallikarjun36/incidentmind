from difflib import SequenceMatcher

from .hindsight_service import recall_incidents


def investigate_incident(
    incident_id: str,
    service: str,
    severity: str,
    symptoms: list[str],
    deployment: str | None,
):
    query = f"""
    Find historical production incidents relevant to this incident.

    Current incident:
    Incident ID: {incident_id}
    Service: {service}
    Severity: {severity}
    Symptoms: {", ".join(symptoms)}
    Deployment: {deployment or "unknown"}

    Focus on:
    - same service
    - similar symptoms
    - database connection exhaustion
    - connection leaks
    - latency
    - error rates
    - deployment-related failures
    - root causes
    - resolutions
    """

    recall_response = recall_incidents(query)

    historical_results = getattr(recall_response, "results", [])

    # Convert Hindsight results into a simple internal structure.
    incidents = []

    for result in historical_results:
        evidence = getattr(result, "text", None)

        if not evidence:
            evidence = str(result)

        incidents.append(
            {
                "memory_id": getattr(result, "id", None),
                "type": getattr(result, "type", None),
                "evidence": evidence.strip(),
            }
        )

    # ---------------------------------------------------------
    # Deduplicate Hindsight memories.
    # Hindsight may return multiple records containing the
    # same incident fact with slightly different wording.
    # ---------------------------------------------------------

    unique_incidents = []

    for incident in incidents:
        evidence = incident["evidence"]

        if not evidence:
            continue

        is_duplicate = False

        for existing in unique_incidents:
            similarity = SequenceMatcher(
                None,
                evidence.lower(),
                existing["evidence"].lower(),
            ).ratio()

            if similarity >= 0.90:
                is_duplicate = True
                break

        if not is_duplicate:
            unique_incidents.append(incident)

    # Keep the investigation report manageable.
    incidents = unique_incidents[:5]

    combined_text = " ".join(
        item["evidence"].lower()
        for item in incidents
    )

    hypotheses = []

    # ---------------------------------------------------------
    # Hypothesis 1: Connection exhaustion
    # ---------------------------------------------------------

    connection_evidence = [
        item["evidence"]
        for item in incidents
        if (
            "connection" in item["evidence"].lower()
            or "pool" in item["evidence"].lower()
        )
    ]

    if connection_evidence:
        hypotheses.append(
            {
                "hypothesis": (
                    "Database connection exhaustion or "
                    "connection lifecycle issue"
                ),
                "evidence": connection_evidence[:2],
            }
        )

    # ---------------------------------------------------------
    # Hypothesis 2: Connection/resource leak
    # ---------------------------------------------------------

    leak_evidence = [
        item["evidence"]
        for item in incidents
        if "leak" in item["evidence"].lower()
    ]

    if leak_evidence:
        hypotheses.append(
            {
                "hypothesis": "Database connection/resource leak",
                "evidence": leak_evidence[:2],
            }
        )

    # ---------------------------------------------------------
    # Hypothesis 3: Deployment regression
    # ---------------------------------------------------------

    deployment_evidence = [
        item["evidence"]
        for item in incidents
        if "deployment" in item["evidence"].lower()
    ]

    if deployment_evidence:
        hypotheses.append(
            {
                "hypothesis": "Deployment-related regression",
                "evidence": deployment_evidence[:2],
            }
        )

    # ---------------------------------------------------------
    # Hypothesis 4: Latency
    # ---------------------------------------------------------

    latency_evidence = [
        item["evidence"]
        for item in incidents
        if "latency" in item["evidence"].lower()
    ]

    if latency_evidence:
        hypotheses.append(
            {
                "hypothesis": "Database or downstream dependency latency",
                "evidence": latency_evidence[:2],
            }
        )

    # ---------------------------------------------------------
    # Investigation steps
    # ---------------------------------------------------------

    investigation_steps = [
        "Check database connection pool utilization and active connections.",
        "Inspect recent deployment changes affecting database connection lifecycle.",
        "Compare current symptoms with the retrieved historical incidents.",
        "Check application logs for connection timeout and pool exhaustion errors.",
    ]

    # ---------------------------------------------------------
    # Recommended remediation
    # ---------------------------------------------------------

    remediation_actions = [
        "Correct connection lifecycle handling if a connection leak is confirmed.",
        "Roll back the latest deployment if evidence links the regression to that release.",
        "Restore database connection pool capacity after confirming the underlying cause.",
    ]

    # ---------------------------------------------------------
    # Final investigation report
    # ---------------------------------------------------------

    return {
        "incident_id": incident_id,
        "service": service,
        "severity": severity,
        "current_symptoms": symptoms,
        "deployment": deployment,

        "summary": (
            f"Incident investigation for {service}. "
            f"Historical evidence was retrieved from IncidentMind memory."
        ),

        "root_cause_hypotheses": hypotheses,

        "investigation_steps": investigation_steps,

        "recommended_actions": remediation_actions,

        "historical_evidence": incidents,

       "ai_status": "Investigation powered by organizational incident memory",
    }