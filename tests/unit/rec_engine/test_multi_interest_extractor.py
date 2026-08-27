"""
Unit tests for PulseRec Dynamic Capsule Multi-Interest Extractor.
"""

from backend.services.rec_engine.multi_interest_extractor import MultiInterestCapsuleExtractor
import numpy as np


def test_capsule_interest_extraction():
    extractor = MultiInterestCapsuleExtractor(embedding_dim=16, max_interests_k=3, routing_iterations=3)

    # 10 item embeddings
    items = [np.random.normal(0, 1, 16).tolist() for _ in range(10)]
    interests = extractor.extract_user_interests(items)

    assert len(interests) == 3
    assert len(interests[0]) == 16
    assert len(interests[1]) == 16
    assert len(interests[2]) == 16


def test_empty_sequence_fallback():
    extractor = MultiInterestCapsuleExtractor(embedding_dim=8, max_interests_k=2)
    interests = extractor.extract_user_interests([])
    assert len(interests) == 1
    assert len(interests[0]) == 8
