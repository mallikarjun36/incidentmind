import os

from dotenv import load_dotenv
from hindsight_client import Hindsight

load_dotenv()

client = Hindsight(
    base_url=os.environ["HINDSIGHT_BASE_URL"],
    api_key=os.environ["HINDSIGHT_API_KEY"],
)

BANK_ID = os.environ["HINDSIGHT_BANK_ID"]


def retain_incident(content: str):
    return client.retain(
        bank_id=BANK_ID,
        content=content,
    )


def recall_incidents(query: str):
    return client.recall(
        bank_id=BANK_ID,
        query=query,
    )