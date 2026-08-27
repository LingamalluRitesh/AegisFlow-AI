import pytest
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
