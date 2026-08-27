"""
AegisFlow Python Client SDK
High-performance async client for event ingestion, online feature lookup, and fraud/recommendation inference.
"""

from typing import Dict, Any, Optional
import httpx


class AegisFlowClient:
    def __init__(self, endpoint: str = "http://localhost:8000/api/v1", api_key: Optional[str] = None):
        self.endpoint = endpoint.rstrip("/")
        self.headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}

    async def evaluate_fraud(self, transaction_payload: Dict[str, Any]) -> Dict[str, Any]:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.post(f"{self.endpoint}/fraud/evaluate", json=transaction_payload, headers=self.headers)
            resp.raise_for_status()
            return resp.json()

    async def get_recommendations(self, user_id: str, candidate_count: int = 10) -> Dict[str, Any]:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.post(
                f"{self.endpoint}/recommendations/serve",
                json={"user_id": user_id, "candidate_count": candidate_count},
                headers=self.headers,
            )
            resp.raise_for_status()
            return resp.json()
