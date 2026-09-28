import os

from dotenv import load_dotenv
from hindsight_client import Hindsight

load_dotenv()

client = Hindsight(
    base_url=os.environ["HINDSIGHT_BASE_URL"],
    api_key=os.environ["HINDSIGHT_API_KEY"],
)

BANK_ID = os.environ["HINDSIGHT_BANK_ID"]

query = """
Find previous incidents related to:
- payment API latency
- high error rates
- database connection exhaustion
- deployment-related failures
- database connection leaks

Return incidents that could help diagnose a new incident with similar symptoms.
"""

results = client.recall(
    bank_id=BANK_ID,
    query=query,
)

print("RECALL RESULTS:")
print(results)