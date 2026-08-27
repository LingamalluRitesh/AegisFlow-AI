"""
AegisGuard Fraud Sentinel Service Facade
Orchestrates feature hydration, rule evaluation, graph multiplier, ML scoring, and decision emission in < 10ms.
"""

import time
from datetime import datetime, timezone
from backend.core.types import TransactionEvent, FraudEvaluationResponse, RiskLevel, ActionType
from backend.core.logging import get_logger
from backend.core.telemetry import telemetry_manager
from backend.services.feature_store.client import feature_store_client
from backend.services.fraud_engine.rule_engine import ComplexEventRuleEngine
from backend.services.fraud_engine.rules_catalog import get_default_fraud_rules
from backend.services.fraud_engine.graph_engine import FraudGraphEngine
from backend.services.fraud_engine.anomaly_detector import StreamingAnomalyDetector
from backend.services.fraud_engine.ensemble_scorer import EnsembleRiskScorer
from backend.services.fraud_engine.policy_evaluator import PolicyEvaluator
from backend.services.fraud_engine.case_manager import fraud_case_manager

logger = get_logger("fraud.service")


class AegisGuardFraudService:
    def __init__(self):
        self.rule_engine = ComplexEventRuleEngine()
        for r in get_default_fraud_rules():
            self.rule_engine.register_rule(r)

        self.graph_engine = FraudGraphEngine()
        self.anomaly_detector = StreamingAnomalyDetector()
        self.ensemble_scorer = EnsembleRiskScorer()
        self.policy_evaluator = PolicyEvaluator()

    async def evaluate_transaction(self, tx: TransactionEvent) -> FraudEvaluationResponse:
        start_time = time.perf_counter()

        self.graph_engine.record_edge(
            user_id=tx.user_id,
            device_id=tx.device_id,
            ip_address=tx.ip_address,
            card_id=tx.source_account_id,
        )

        hydrated_feats_list = await feature_store_client.get_online_features(
            feature_view_name="user_fraud_velocity_features",
            entity_keys=[tx.user_id],
        )
        online_feats = hydrated_feats_list[0] if hydrated_feats_list else {}

        context = {**online_feats, **tx.model_dump(), "amount": tx.amount}

        matched_rules = self.rule_engine.evaluate_rules(context)
        triggered_rule_names = [r.name for r in matched_rules]
        rule_boost = max([r.risk_score_boost for r in matched_rules], default=0.0)
        forced_action = matched_rules[0].action if matched_rules else None

        graph_mult = self.graph_engine.calculate_entity_risk_multiplier(tx.user_id, tx.device_id, tx.ip_address)
        anomaly_score = self.anomaly_detector.score_features(context)

        simulated_ml_prob = min(0.99, (context.get("tx_count_5m", 0) * 0.12) + (tx.amount / 10000.0))

        final_risk_score = self.ensemble_scorer.compute_ensemble_score(
            rule_boost=rule_boost,
            ml_model_prob=simulated_ml_prob,
            anomaly_score=anomaly_score,
            graph_multiplier=graph_mult,
        )

        risk_level, action = self.policy_evaluator.evaluate_decision(final_risk_score, forced_action)

        shap_contributions = {
            "tx_count_5m": float(context.get("tx_count_5m", 0) * 0.15),
            "amount": float(min(0.40, tx.amount / 5000.0)),
            "graph_multiplier": float((graph_mult - 1.0) * 0.25),
            "anomaly_score": float(anomaly_score * 0.20),
        }

        reasons = []
        if triggered_rule_names:
            reasons.extend([f"Rule Triggered: {r}" for r in triggered_rule_names])
        if risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]:
            reasons.append(f"High risk anomaly probability ({final_risk_score:.2f})")

        latency_ms = (time.perf_counter() - start_time) * 1000.0

        if risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]:
            fraud_case_manager.create_case(
                transaction_id=tx.transaction_id,
                user_id=tx.user_id,
                risk_score=final_risk_score,
                severity=risk_level.value,
                evidence={"reasons": reasons, "features": context},
            )

        telemetry_manager.get_counter("aegis_fraud_evaluations_total").inc()
        if action == ActionType.BLOCK:
            telemetry_manager.get_counter("aegis_fraud_blocked_total").inc()
        telemetry_manager.get_histogram("aegis_end_to_end_decision_latency_seconds").observe(latency_ms / 1000.0)

        return FraudEvaluationResponse(
            transaction_id=tx.transaction_id,
            risk_score=round(final_risk_score, 4),
            risk_level=risk_level,
            recommended_action=action,
            reasons=reasons,
            triggered_rules=triggered_rule_names,
            shap_contributions=shap_contributions,
            feature_snapshot=context,
            evaluation_latency_ms=round(latency_ms, 2),
            model_version="aegisguard-ensemble-v2.4",
            timestamp=datetime.now(timezone.utc),
        )


fraud_service = AegisGuardFraudService()
