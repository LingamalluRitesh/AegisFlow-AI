"""
High-Concurrency Performance & Stress Benchmark (Locust)
Tests sustained high throughput and sub-10ms latency percentiles.
"""

from locust import HttpUser, task, between
import random
import uuid


class AegisFlowBenchmarkUser(HttpUser):
    wait_time = between(0.01, 0.05)

    @task(4)
    def evaluate_fraud_transaction(self):
        tx_payload = {
            "transaction_id": f"tx_load_{str(uuid.uuid4())[:8]}",
            "user_id": f"usr_{random.randint(1, 1000)}",
            "source_account_id": "acct_source_load",
            "target_account_id": f"acct_target_{random.randint(1, 50)}",
            "amount": round(random.uniform(10.0, 2500.0), 2),
            "currency": "USD",
            "channel": "mobile_app",
        }
        self.client.post("/api/v1/fraud/evaluate", json=tx_payload)

    @task(3)
    def request_recommendations(self):
        self.client.post(
            "/api/v1/recommendations/serve",
            json={"user_id": f"usr_{random.randint(1, 1000)}", "candidate_count": 8},
        )

    @task(1)
    def lookup_features(self):
        self.client.post(
            "/api/v1/feature-store/online-lookup?view_name=user_fraud_velocity_features",
            json=[f"usr_{random.randint(1, 1000)}"],
        )
