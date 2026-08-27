"""
AegisGuard: Real-Time Streaming Fraud Sentinel & Risk Scoring Subsystem
Sub-10ms financial fraud interception, CEP rule engine, GNN risk topologies, and explainability.
"""

from backend.services.fraud_engine.rule_engine import ComplexEventRuleEngine, Rule, Condition
from backend.services.fraud_engine.rules_catalog import get_default_fraud_rules
from backend.services.fraud_engine.graph_engine import FraudGraphEngine
from backend.services.fraud_engine.anomaly_detector import StreamingAnomalyDetector
from backend.services.fraud_engine.ensemble_scorer import EnsembleRiskScorer
from backend.services.fraud_engine.policy_evaluator import PolicyEvaluator
from backend.services.fraud_engine.case_manager import CaseManager, fraud_case_manager
from backend.services.fraud_engine.service import AegisGuardFraudService, fraud_service

__all__ = [
    "ComplexEventRuleEngine",
    "Rule",
    "Condition",
    "get_default_fraud_rules",
    "FraudGraphEngine",
    "StreamingAnomalyDetector",
    "EnsembleRiskScorer",
    "PolicyEvaluator",
    "CaseManager",
    "fraud_case_manager",
    "AegisGuardFraudService",
    "fraud_service",
]
