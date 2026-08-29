import pytest
from backend.services.fraud_engine.circular_ring_detector import CircularFraudRingDetector


def test_circular_fraud_ring_detection():
    detector = CircularFraudRingDetector(max_ring_depth=4)

    # Create circular ring: A -> B -> C -> A
    detector.add_transaction("acc_A", "acc_B", 5000.0)
    detector.add_transaction("acc_B", "acc_C", 4800.0)
    detector.add_transaction("acc_C", "acc_A", 4600.0)

    # Legitimate non-cyclic branch: D -> E
    detector.add_transaction("acc_D", "acc_E", 200.0)

    rings = detector.find_circular_rings()
    assert len(rings) == 1
    assert rings[0]["ring_length"] == 3
    assert rings[0]["risk_category"] == "CRITICAL_CIRCULAR_MONEY_LAUNDERING_RING"
    assert "acc_A" in rings[0]["ring_members"]
    assert "acc_B" in rings[0]["ring_members"]
    assert "acc_C" in rings[0]["ring_members"]


def test_degree_centrality_risk():
    detector = CircularFraudRingDetector()
    for i in range(6):
        detector.add_transaction(f"sender_{i}", "hub_account", 1000.0)
        detector.add_transaction("hub_account", f"receiver_{i}", 950.0)

    centrality = detector.calculate_centrality_risk("hub_account")
    assert centrality["in_degree"] == 6
    assert centrality["out_degree"] == 6
    assert centrality["is_suspicious_mule_hub"] is True
