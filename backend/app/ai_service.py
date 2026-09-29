import os

from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()

client = AzureOpenAI(
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    api_version="2024-10-21",
)

DEPLOYMENT = os.environ["AZURE_OPENAI_DEPLOYMENT"]


def generate_investigation(
    incident_id: str,
    service: str,
    severity: str,
    symptoms: list[str],
    deployment: str | None,
    historical_evidence: list[dict],
):
    evidence_text = "\n\n".join(
        f"Historical evidence {i + 1}:\n{item.get('evidence', '')}"
        for i, item in enumerate(historical_evidence)
    )

    prompt = f"""
You are IncidentMind, an incident-response assistant for production engineers.

Analyze the current production incident using the historical evidence
provided below.

CURRENT INCIDENT

Incident ID: {incident_id}
Service: {service}
Severity: {severity}
Symptoms: {", ".join(symptoms)}
Deployment: {deployment or "unknown"}

HISTORICAL EVIDENCE

{evidence_text}

Produce a concise investigation report containing:

1. Incident summary
2. Root-cause hypotheses
3. Evidence supporting each hypothesis
4. Recommended investigation steps
5. Recommended remediation actions
6. Important uncertainty or missing evidence

Rules:
- Use the historical evidence provided.
- Do not invent facts.
- Clearly distinguish evidence from hypotheses.
- If evidence is insufficient, say so.
- Prioritize concrete technical reasoning.
"""

    response = client.chat.completions.create(
        model=DEPLOYMENT,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a careful production incident-response "
                    "assistant. Ground your reasoning in supplied evidence."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content