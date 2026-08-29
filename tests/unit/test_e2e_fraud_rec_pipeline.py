"""
End-to-End Fraud Graph & Recommender Pipeline Integration Suite.
Validates Graph Ring Analyzers, HNSW Semantic Retrievers, Rate Limiters, and Ensemble Scoring.
"""

import pytest
from backend.services.fraud_engine.circular_ring_detector import CircularFraudRingDetector
from backend.services.rec_engine.hnsw_retriever import HNSWVectorIndex
from backend.core.token_bucket_guard import TokenBucketSecurityGuard
from backend.services.fraud_engine.ensemble_scorer import EnsembleRiskScorer


def test_full_fraud_and_recommendation_flow():
    # 1. Graph Ring Detection
    ring_detector = CircularFraudRingDetector(max_ring_depth=4)
    ring_detector.add_transaction("u_alice", "u_bob", 1200.0)
    ring_detector.add_transaction("u_bob", "u_charlie", 1150.0)
    ring_detector.add_transaction("u_charlie", "u_alice", 1100.0)

    rings = ring_detector.find_circular_rings()
    assert len(rings) == 1
    assert rings[0]["ring_length"] == 3

    # 2. Recommender ANN Search
    vector_index = HNSWVectorIndex(dimension=4)
    vector_index.insert_vector("rec_item_1", [0.8, 0.2, 0.0, 0.1], {"title": "Cybersecurity Suite"})
    vector_index.insert_vector("rec_item_2", [0.0, 0.1, 0.9, 0.1], {"title": "Travel Backpack"})

    retrieved = vector_index.search_knn([0.85, 0.15, 0.0, 0.05], top_k=1)
    assert len(retrieved) == 1
    assert retrieved[0]["item_id"] == "rec_item_1"

    # 3. Token Bucket Security Check
    guard = TokenBucketSecurityGuard(capacity=10.0, refill_rate_per_sec=5.0)
    res = guard.allow_request("tenant_fintech_corp", tokens_required=2.0)
    assert res["allowed"] is True

    # 4. Ensemble Scorer Check
    scorer = EnsembleRiskScorer()
    combined = scorer.compute_ensemble_score(
        rule_boost=0.85,
        ml_model_prob=0.90,
        anomaly_score=0.95,
        graph_multiplier=1.2,
    )
    assert combined >= 0.80
