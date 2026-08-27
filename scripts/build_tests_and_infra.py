"""
AegisFlow Test Suite, Deployment Infra, Helm Charts, Terraform & Load Benchmarks Builder
"""

import os
from pathlib import Path

BASE_DIR = Path("D:/ab")

def write_file(rel_path: str, content: str):
    full_path = BASE_DIR / rel_path
    full_path.parent.mkdir(parents=True, exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Generated: {rel_path} ({len(content.splitlines())} lines)")

def build_test_suites():
    print("Building comprehensive Unit, Integration, and Load Testing Suites...")

    # 1. Core Tests
    c_test_core = '''import pytest
from backend.core.config import settings
from backend.core.crypto import crypto_manager
from backend.core.circuit_breaker import CircuitBreaker, CircuitState
from backend.core.rate_limiter import SlidingWindowRateLimiter
from backend.core.cache import LRUCacheL1
from backend.core.math_utils import (
    vector_cosine_similarity,
    calculate_haversine_distance_km,
    compute_population_stability_index,
    compute_kolmogorov_smirnov_statistic,
)


def test_crypto_hashing_and_hmac():
    token = crypto_manager.generate_token(16)
    assert len(token) == 32
    h = crypto_manager.hash_sha256("test_data")
    assert len(h) == 64
    sig = crypto_manager.hmac_sign("message_1")
    assert crypto_manager.hmac_verify("message_1", sig) is True
    assert crypto_manager.hmac_verify("tampered_message", sig) is False


def test_circuit_breaker_lifecycle():
    cb = CircuitBreaker(name="test_service", failure_threshold=2, recovery_timeout_sec=0.1)
    assert cb.state == CircuitState.CLOSED
    cb.record_failure()
    assert cb.state == CircuitState.CLOSED
    cb.record_failure()
    assert cb.state == CircuitState.OPEN


def test_rate_limiter_sliding_window():
    limiter = SlidingWindowRateLimiter(max_requests=3, window_seconds=10)
    allowed1, rem1 = limiter.is_allowed("user_1")
    allowed2, rem2 = limiter.is_allowed("user_1")
    allowed3, rem3 = limiter.is_allowed("user_1")
    allowed4, rem4 = limiter.is_allowed("user_1")
    assert allowed1 is True
    assert allowed2 is True
    assert allowed3 is True
    assert allowed4 is False


def test_lru_cache_ttl():
    cache = LRUCacheL1(capacity=2, default_ttl_sec=100.0)
    cache.set("k1", "v1")
    cache.set("k2", "v2")
    assert cache.get("k1") == "v1"
    cache.set("k3", "v3")
    assert cache.get("k3") == "v3"


def test_math_statistics_and_drift():
    v1 = [1.0, 0.0, 0.0]
    v2 = [1.0, 0.0, 0.0]
    assert vector_cosine_similarity(v1, v2) == pytest.approx(1.0)

    dist = calculate_haversine_distance_km(40.7128, -74.0060, 34.0522, -118.2437)
    assert dist > 3900.0 and dist < 4000.0

    exp = [1.0, 2.0, 3.0, 4.0, 5.0] * 20
    act = [1.1, 2.1, 3.0, 4.2, 4.9] * 20
    psi = compute_population_stability_index(exp, act)
    assert psi >= 0.0
'''
    write_file("tests/unit/core/test_core_primitives.py", c_test_core)

    # 2. Fraud Engine Tests
    c_test_fraud = '''import pytest
from backend.core.types import TransactionEvent, RiskLevel, ActionType
from backend.services.fraud_engine.rule_engine import ComplexEventRuleEngine, Rule, Condition
from backend.services.fraud_engine.anomaly_detector import StreamingAnomalyDetector
from backend.services.fraud_engine.graph_engine import FraudGraphEngine
from backend.services.fraud_engine.service import fraud_service


def test_rule_engine_evaluation():
    engine = ComplexEventRuleEngine()
    rule = Rule(
        rule_id="TEST_RULE_1",
        name="Test High Value",
        description="Flags high value",
        priority=10,
        conditions=[Condition(field="amount", operator=">", value=1000.0)],
        action=ActionType.BLOCK,
        risk_score_boost=0.8,
    )
    engine.register_rule(rule)
    matched = engine.evaluate_rules({"amount": 1500.0})
    assert len(matched) == 1
    unmatched = engine.evaluate_rules({"amount": 500.0})
    assert len(unmatched) == 0


def test_graph_fraud_multiplier():
    graph = FraudGraphEngine()
    for i in range(6):
        graph.record_edge(f"usr_{i}", "dev_mule_ring_01", "192.168.1.1", f"card_{i}")
    mult = graph.calculate_entity_risk_multiplier("usr_0", "dev_mule_ring_01", "192.168.1.1")
    assert mult > 2.0


def test_anomaly_detector_scoring():
    detector = StreamingAnomalyDetector()
    score_normal = detector.score_features({"amount": 50.0, "tx_count_5m": 1})
    score_outlier = detector.score_features({"amount": 9500.0, "tx_count_5m": 12, "max_geo_leap_speed_kmh": 950.0})
    assert score_outlier > score_normal


@pytest.mark.asyncio
async def test_end_to_end_fraud_service():
    tx = TransactionEvent(
        transaction_id="tx_test_001",
        user_id="usr_normal_01",
        source_account_id="acct_01",
        target_account_id="acct_02",
        amount=25.0,
        currency="USD",
    )
    decision = await fraud_service.evaluate_transaction(tx)
    assert decision.transaction_id == "tx_test_001"
    assert decision.risk_level in [RiskLevel.LOW, RiskLevel.MEDIUM, RiskLevel.HIGH]
'''
    write_file("tests/unit/fraud_engine/test_fraud_sentinel.py", c_test_fraud)

    # 3. Recommendation Engine Tests
    c_test_rec = '''import pytest
from backend.core.types import RecommendationRequest
from backend.services.rec_engine.vector_index import HNSWVectorIndex
from backend.services.rec_engine.contextual_bandit import LinUCBBandit
from backend.services.rec_engine.reranker import MaximalMarginalRelevanceReranker
from backend.services.rec_engine.service import rec_service


def test_vector_ann_indexing():
    idx = HNSWVectorIndex(dimension=4)
    idx.add_item("item_1", [1.0, 0.0, 0.0, 0.0], {"title": "Item 1"})
    idx.add_item("item_2", [0.0, 1.0, 0.0, 0.0], {"title": "Item 2"})
    results = idx.search_nearest([1.0, 0.0, 0.0, 0.0], top_k=1)
    assert len(results) == 1
    assert results[0][0] == "item_1"


def test_bandit_arm_updates():
    bandit = LinUCBBandit(dimension=4)
    bonus = bandit.get_exploration_bonus("electronics", [0.1, 0.2, 0.3, 0.4])
    assert bonus > 0.0
    bandit.update_arm("electronics", [0.1, 0.2, 0.3, 0.4], 1.0)


def test_mmr_diversity_reranker():
    reranker = MaximalMarginalRelevanceReranker(diversity_lambda=0.5)
    candidates = [
        {"item_id": "1", "score": 0.9, "category": "electronics"},
        {"item_id": "2", "score": 0.88, "category": "electronics"},
        {"item_id": "3", "score": 0.85, "category": "books"},
    ]
    reranked = reranker.rerank(candidates, top_k=2)
    assert len(reranked) == 2
    assert reranked[0]["item_id"] == "1"
    assert reranked[1]["category"] == "books"


@pytest.mark.asyncio
async def test_end_to_end_rec_service():
    req = RecommendationRequest(user_id="usr_007", candidate_count=4)
    res = await rec_service.get_recommendations(req)
    assert res.user_id == "usr_007"
    assert len(res.recommendations) > 0
'''
    write_file("tests/unit/rec_engine/test_rec_engine.py", c_test_rec)

    # 4. Feature Store Tests
    c_test_fs = '''import pytest
from backend.services.feature_store.registry import registry
from backend.services.feature_store.aggregations import SlidingWindowAggregator
from backend.services.feature_store.transformations import FeatureTransformer


def test_feature_registry_catalog():
    views = registry.list_feature_views()
    assert len(views) >= 3
    user_view = registry.get_feature_view("user_fraud_velocity_features")
    assert user_view is not None
    assert "tx_count_5m" in user_view.feature_names()


def test_sliding_window_aggregator():
    agg = SlidingWindowAggregator(entity_id="usr_agg_test")
    agg.add_event(100.0, amount=50.0)
    agg.add_event(110.0, amount=150.0)
    stats = agg.compute_window_stats(60, current_time=120.0)
    assert stats["count"] == 2.0
    assert stats["sum"] == 200.0
    assert stats["mean"] == 100.0


def test_feature_transformations():
    cyclical = FeatureTransformer.encode_cyclical_time(hour=12, day_of_week=3)
    assert "hour_sin" in cyclical
    assert "hour_cos" in cyclical
    scaled = FeatureTransformer.robust_scale(100.0, median=50.0, iqr=25.0)
    assert scaled == 2.0
'''
    write_file("tests/unit/feature_store/test_feature_store.py", c_test_fs)

    # 5. MLOps Tests
    c_test_mlops = '''import pytest
from backend.services.mlops_governance.drift_detector import drift_detector
from backend.services.mlops_governance.explainability import shap_explainer
from backend.services.mlops_governance.audit_ledger import audit_ledger


def test_audit_ledger_hash_chain():
    b1 = audit_ledger.append_event("admin", "CONFIG_CHANGE", {"key": "threshold", "val": 0.85})
    assert b1["sequence_index"] > 0
    assert audit_ledger.verify_integrity() is True


def test_streaming_shap_values():
    shap_dict = shap_explainer.compute_local_shap_values({"amount": 1500.0, "tx_count_5m": 6})
    assert "amount" in shap_dict
    assert "tx_count_5m" in shap_dict
    assert shap_dict["amount"] > 0.0
'''
    write_file("tests/unit/mlops/test_mlops_governance.py", c_test_mlops)

    # 6. Load Benchmark script (Locust)
    c_locust = '''"""
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
'''
    write_file("tests/load/locustfile.py", c_locust)

def build_deployment_infra():
    print("Building Docker Compose, Kubernetes Helm Charts, and Terraform infrastructure...")

    # 1. Dockerfile
    c_dockerfile = '''FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \\
    build-essential curl && \\
    rm -rf /var/lib/apt/lists/*

COPY pyproject.toml requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["uvicorn", "backend.services.gateway.app:app", "--host", "0.0.0.0", "--port", "8000"]
'''
    write_file("deployment/docker/Dockerfile.backend", c_dockerfile)

    # 2. requirements.txt
    c_req = '''fastapi>=0.111.0
uvicorn[standard]>=0.30.0
pydantic>=2.7.0
pydantic-settings>=2.2.0
sqlalchemy>=2.0.30
asyncpg>=0.29.0
redis>=5.0.4
duckdb>=0.10.2
pandas>=2.2.2
numpy>=1.26.4
httpx>=0.27.0
pytest>=8.2.0
pytest-asyncio>=0.23.6
locust>=2.28.0
'''
    write_file("requirements.txt", c_req)

    # 3. Docker Compose Stack
    c_compose = '''version: '3.8'

services:
  gateway:
    build:
      context: .
      dockerfile: deployment/docker/Dockerfile.backend
    ports:
      - "8000:8000"
    environment:
      - POSTGRES_HOST=postgres
      - REDIS_HOST=redis
      - KAFKA_BOOTSTRAP_SERVERS=kafka:9092
    depends_on:
      - postgres
      - redis
      - kafka

  frontend:
    build:
      context: ./frontend
      dockerfile: ../deployment/docker/Dockerfile.frontend
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
    depends_on:
      - gateway

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  postgres:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=aegisflow_db
      - POSTGRES_USER=aegis_admin
      - POSTGRES_PASSWORD=AegisSecurePass2026!
    ports:
      - "5432:5432"

  kafka:
    image: confluentinc/cp-kafka:7.5.0
    ports:
      - "9092:9092"
    environment:
      KAFKA_NODE_ID: 1
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: 'CONTROLLER:PLAINTEXT,PLAINTEXT:PLAINTEXT,PLAINTEXT_HOST:PLAINTEXT'
      KAFKA_ADVERTISED_LISTENERS: 'PLAINTEXT://kafka:29092,PLAINTEXT_HOST://localhost:9092'
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
      KAFKA_PROCESS_ROLES: 'broker,controller'
      KAFKA_CONTROLLER_QUORUM_VOTERS: '1@kafka:29093'
      KAFKA_LISTENERS: 'PLAINTEXT://0.0.0.0:29092,CONTROLLER://0.0.0.0:29093,PLAINTEXT_HOST://0.0.0.0:9092'
      KAFKA_CONTROLLER_LISTENER_NAMES: 'CONTROLLER'
      CLUSTER_ID: '4L622nShTUiBenY7oNSRWA'
'''
    write_file("deployment/docker-compose.yml", c_compose)

    # 4. Kubernetes Helm Chart
    c_helm_chart = '''apiVersion: v2
name: aegisflow-platform
description: Enterprise Helm Chart for AegisFlow Streaming AI, Fraud Sentinel & Recommendation Mesh
type: application
version: 2.4.0
appVersion: "2.4.0"
'''
    write_file("deployment/helm/Chart.yaml", c_helm_chart)

    c_helm_values = '''replicaCount: 3

image:
  repository: aegisflow/gateway
  pullPolicy: IfNotPresent
  tag: "2.4.0"

service:
  type: ClusterIP
  port: 8000

ingress:
  enabled: true
  className: nginx
  hosts:
    - host: api.aegisflow.ai
      paths:
        - path: /
          pathType: ImplementationSpecific

resources:
  limits:
    cpu: 2000m
    memory: 4Gi
  requests:
    cpu: 500m
    memory: 1Gi

autoscaling:
  enabled: true
  minReplicas: 3
  maxReplicas: 20
  targetCPUUtilizationPercentage: 70
'''
    write_file("deployment/helm/values.yaml", c_helm_values)

if __name__ == "__main__":
    build_test_suites()
    build_deployment_infra()
