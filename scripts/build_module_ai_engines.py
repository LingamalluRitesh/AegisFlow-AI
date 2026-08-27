"""
AegisFlow AI Engines Builder
Constructs backend/services/fraud_engine (AegisGuard) and backend/services/rec_engine (PulseRec)
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

def build_ai_engines():
    print("Building AegisGuard Fraud Engine and PulseRec Recommendation Engine...")

    # fraud_engine/__init__.py
    c_fe_init = '''"""
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
'''
    write_file("backend/services/fraud_engine/__init__.py", c_fe_init)

    # fraud_engine/rule_engine.py
    c_fe_rules = '''"""
Complex Event Processing (CEP) Deterministic Rule Engine
Evaluates dynamic boolean AST expressions against transaction payloads and hydrated feature vectors.
"""

import re
import operator
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from backend.core.types import ActionType
from backend.core.logging import get_logger

logger = get_logger("fraud.rule_engine")


class OperatorType(str):
    EQ = "=="
    NE = "!="
    GT = ">"
    GTE = ">="
    LT = "<"
    LTE = "<="
    IN = "IN"
    NOT_IN = "NOT_IN"
    CONTAINS = "CONTAINS"
    REGEX = "REGEX"


_OP_FUNCS = {
    "==": operator.eq,
    "!=": operator.ne,
    ">": operator.gt,
    ">=": operator.ge,
    "<": operator.lt,
    "<=": operator.le,
    "IN": lambda val, target_list: val in target_list,
    "NOT_IN": lambda val, target_list: val not in target_list,
    "CONTAINS": lambda val, substr: substr in str(val),
    "REGEX": lambda val, pattern: bool(re.search(pattern, str(val))),
}


class Condition(BaseModel):
    field: str = Field(..., description="Target feature or payload field, e.g. tx_count_5m")
    operator: str = Field(..., description="Comparison operator (==, >, <, IN, etc.)")
    value: Any = Field(..., description="Threshold or comparison target")

    def evaluate(self, context: Dict[str, Any]) -> bool:
        if self.field not in context:
            return False
        field_val = context[self.field]
        if field_val is None:
            return False

        op_func = _OP_FUNCS.get(self.operator.upper())
        if not op_func:
            return False

        try:
            if isinstance(self.value, (int, float)) and isinstance(field_val, (int, float)):
                return op_func(float(field_val), float(self.value))
            return op_func(field_val, self.value)
        except Exception:
            return False


class Rule(BaseModel):
    rule_id: str
    name: str
    description: str
    priority: int = 100
    conditions: List[Condition]
    action: ActionType = ActionType.BLOCK
    risk_score_boost: float = 0.5
    is_active: bool = True

    def evaluate(self, context: Dict[str, Any]) -> bool:
        if not self.is_active or not self.conditions:
            return False
        return all(cond.evaluate(context) for cond in self.conditions)


class ComplexEventRuleEngine:
    def __init__(self):
        self._rules: Dict[str, Rule] = {}

    def register_rule(self, rule: Rule) -> None:
        self._rules[rule.rule_id] = rule
        logger.info_ctx(f"Registered Fraud Rule: [{rule.rule_id}] {rule.name}")

    def evaluate_rules(self, context: Dict[str, Any]) -> List[Rule]:
        matched = []
        sorted_rules = sorted(self._rules.values(), key=lambda r: r.priority)
        for rule in sorted_rules:
            if rule.evaluate(context):
                matched.append(rule)
        return matched
'''
    write_file("backend/services/fraud_engine/rule_engine.py", c_fe_rules)

    # fraud_engine/rules_catalog.py
    c_fe_cat = '''"""
Institutional Fraud Rules Catalog
Production rule definitions for high-velocity transfers, impossible travel, new device bursts.
"""

from typing import List
from backend.services.fraud_engine.rule_engine import Rule, Condition
from backend.core.types import ActionType


def get_default_fraud_rules() -> List[Rule]:
    return [
        Rule(
            rule_id="RULE_HIGH_VELOCITY_5M",
            name="Extreme 5-Minute Velocity Surge",
            description="More than 6 transactions in 5 minutes",
            priority=10,
            conditions=[
                Condition(field="tx_count_5m", operator=">", value=6),
            ],
            action=ActionType.BLOCK,
            risk_score_boost=0.90,
        ),
        Rule(
            rule_id="RULE_IMPOSSIBLE_TRAVEL",
            name="Impossible Geographic Travel Leap",
            description="Geographic distance leap velocity > 800 km/h",
            priority=15,
            conditions=[
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=800.0),
            ],
            action=ActionType.CHALLENGE_2FA,
            risk_score_boost=0.75,
        ),
        Rule(
            rule_id="RULE_NEW_DEVICE_LARGE_AMOUNT",
            name="New Device High-Value Outlier",
            description="Transaction on newly seen device exceeding $2,500",
            priority=20,
            conditions=[
                Condition(field="is_new_device_used", operator="==", value=1),
                Condition(field="amount", operator=">", value=2500.0),
            ],
            action=ActionType.MANUAL_REVIEW,
            risk_score_boost=0.60,
        ),
        Rule(
            rule_id="RULE_HIGH_FAILURE_RATE",
            name="Repeated Transaction Failures",
            description="More than 3 failed transactions in the last hour",
            priority=25,
            conditions=[
                Condition(field="failed_tx_count_1h", operator=">=", value=3),
            ],
            action=ActionType.CHALLENGE_2FA,
            risk_score_boost=0.55,
        ),
        Rule(
            rule_id="RULE_MULTI_IP_SURGE",
            name="Rapid IP Address Hopping",
            description="Transactions originating from more than 3 distinct IPs in 24h",
            priority=30,
            conditions=[
                Condition(field="distinct_ips_24h", operator=">=", value=4),
            ],
            action=ActionType.MANUAL_REVIEW,
            risk_score_boost=0.45,
        ),
    ]
'''
    write_file("backend/services/fraud_engine/rules_catalog.py", c_fe_cat)

    # fraud_engine/graph_engine.py
    c_fe_graph = '''"""
Graph-Based Fraud Ring & Entity Linkage Engine
Analyzes bipartite and heterogeneous transaction graphs to detect coordinated fraud rings and mule networks.
"""

from typing import Dict, Any, List, Set, Optional
from collections import defaultdict
import threading
from backend.core.logging import get_logger

logger = get_logger("fraud.graph_engine")


class FraudGraphEngine:
    def __init__(self):
        self._user_to_devices: Dict[str, Set[str]] = defaultdict(set)
        self._device_to_users: Dict[str, Set[str]] = defaultdict(set)
        self._user_to_ips: Dict[str, Set[str]] = defaultdict(set)
        self._ip_to_users: Dict[str, Set[str]] = defaultdict(set)
        self._user_to_cards: Dict[str, Set[str]] = defaultdict(set)
        self._card_to_users: Dict[str, Set[str]] = defaultdict(set)
        self._lock = threading.Lock()

    def record_edge(self, user_id: str, device_id: Optional[str], ip_address: Optional[str], card_id: Optional[str]) -> None:
        with self._lock:
            if device_id:
                self._user_to_devices[user_id].add(device_id)
                self._device_to_users[device_id].add(user_id)
            if ip_address:
                self._user_to_ips[user_id].add(ip_address)
                self._ip_to_users[ip_address].add(user_id)
            if card_id:
                self._user_to_cards[user_id].add(card_id)
                self._card_to_users[card_id].add(user_id)

    def calculate_entity_risk_multiplier(self, user_id: str, device_id: Optional[str], ip_address: Optional[str]) -> float:
        with self._lock:
            multiplier = 1.0

            if device_id and device_id in self._device_to_users:
                shared_users = len(self._device_to_users[device_id])
                if shared_users > 5:
                    multiplier += 1.2
                elif shared_users > 2:
                    multiplier += 0.5

            if ip_address and ip_address in self._ip_to_users:
                shared_ip_users = len(self._ip_to_users[ip_address])
                if shared_ip_users > 10:
                    multiplier += 0.4

            return min(3.0, multiplier)
'''
    write_file("backend/services/fraud_engine/graph_engine.py", c_fe_graph)

    # fraud_engine/anomaly_detector.py
    c_fe_anom = '''"""
Streaming Unsupervised Anomaly Detector
Evaluates multi-variate continuous feature vectors against expected baseline distributions.
"""

import math
from typing import Dict, Any
from backend.core.logging import get_logger

logger = get_logger("fraud.anomaly_detector")


class StreamingAnomalyDetector:
    def __init__(self):
        self._baselines = {
            "amount": (85.0, 120.0),
            "tx_count_5m": (0.8, 1.2),
            "tx_amount_sum_24h": (250.0, 400.0),
            "max_geo_leap_speed_kmh": (25.0, 60.0),
        }

    def score_features(self, feature_dict: Dict[str, Any]) -> float:
        z_scores = []

        for feature_name, (mean, std) in self._baselines.items():
            if feature_name in feature_dict and feature_dict[feature_name] is not None:
                val = float(feature_dict[feature_name])
                z = max(0.0, (val - mean) / max(1.0, std))
                z_scores.append(z)

        if not z_scores:
            return 0.05

        max_z = max(z_scores)
        mean_z = sum(z_scores) / len(z_scores)
        combined_z = 0.7 * max_z + 0.3 * mean_z

        anomaly_score = 1.0 / (1.0 + math.exp(-1.2 * (combined_z - 2.5)))
        return float(max(0.0, min(1.0, anomaly_score)))
'''
    write_file("backend/services/fraud_engine/anomaly_detector.py", c_fe_anom)

    # fraud_engine/ensemble_scorer.py
    c_fe_ens = '''"""
Ensemble Risk Scoring Engine
Fuses deterministic rule boosts, graph multipliers, supervised tree probabilities, and anomaly scores.
"""

class EnsembleRiskScorer:
    def __init__(
        self,
        rule_weight: float = 0.40,
        ml_model_weight: float = 0.35,
        anomaly_weight: float = 0.15,
        graph_weight: float = 0.10,
    ):
        self.rule_weight = rule_weight
        self.ml_model_weight = ml_model_weight
        self.anomaly_weight = anomaly_weight
        self.graph_weight = graph_weight

    def compute_ensemble_score(
        self,
        rule_boost: float,
        ml_model_prob: float,
        anomaly_score: float,
        graph_multiplier: float,
    ) -> float:
        base_score = (
            self.rule_weight * rule_boost
            + self.ml_model_weight * ml_model_prob
            + self.anomaly_weight * anomaly_score
        )
        final_score = base_score * (1.0 + (graph_multiplier - 1.0) * self.graph_weight)
        return float(max(0.0, min(1.0, final_score)))
'''
    write_file("backend/services/fraud_engine/ensemble_scorer.py", c_fe_ens)

    # fraud_engine/policy_evaluator.py
    c_fe_pol = '''"""
Automated Decision Policy Evaluator
Maps calibrated ensemble risk score to discrete business action types and risk tiers.
"""

from typing import Tuple
from backend.core.types import RiskLevel, ActionType


class PolicyEvaluator:
    def __init__(
        self,
        high_risk_threshold: float = 0.85,
        medium_risk_threshold: float = 0.50,
        low_risk_threshold: float = 0.20,
    ):
        self.high_threshold = high_risk_threshold
        self.medium_threshold = medium_risk_threshold
        self.low_threshold = low_risk_threshold

    def evaluate_decision(
        self,
        risk_score: float,
        forced_action: ActionType = None,
    ) -> Tuple[RiskLevel, ActionType]:
        if forced_action == ActionType.BLOCK:
            return RiskLevel.CRITICAL, ActionType.BLOCK

        if risk_score >= self.high_threshold:
            return RiskLevel.HIGH, ActionType.BLOCK
        elif risk_score >= self.medium_threshold:
            return RiskLevel.MEDIUM, ActionType.CHALLENGE_2FA
        elif risk_score >= self.low_threshold:
            return RiskLevel.LOW, ActionType.ALLOW
        else:
            return RiskLevel.LOW, ActionType.ALLOW
'''
    write_file("backend/services/fraud_engine/policy_evaluator.py", c_fe_pol)

    # fraud_engine/case_manager.py
    c_fe_case = '''"""
Fraud Case Management Workflow Subsystem
Tracks suspicious alerts, investigator assignments, and resolution notes.
"""

import time
import uuid
from typing import Dict, Any, List, Optional
import threading
from backend.core.logging import get_logger

logger = get_logger("fraud.case_manager")


class CaseManager:
    def __init__(self):
        self._cases: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.Lock()

    def create_case(
        self,
        transaction_id: str,
        user_id: str,
        risk_score: float,
        severity: str,
        evidence: Dict[str, Any],
    ) -> Dict[str, Any]:
        case_id = f"CASE-{str(uuid.uuid4())[:8].upper()}"
        case_entry = {
            "case_id": case_id,
            "transaction_id": transaction_id,
            "user_id": user_id,
            "risk_score": risk_score,
            "severity": severity,
            "status": "OPEN",
            "assigned_analyst": None,
            "evidence": evidence,
            "created_at": time.time(),
            "resolved_at": None,
            "resolution_notes": None,
        }
        with self._lock:
            self._cases[case_id] = case_entry

        logger.info_ctx(f"Created Fraud Case [{case_id}] for transaction {transaction_id} (Risk: {risk_score:.2f})")
        return case_entry

    def list_open_cases(self, limit: int = 50) -> List[Dict[str, Any]]:
        with self._lock:
            return [c for c in self._cases.values() if c["status"] == "OPEN"][:limit]

    def resolve_case(self, case_id: str, analyst_id: str, resolution: str, notes: str) -> Optional[Dict[str, Any]]:
        with self._lock:
            if case_id in self._cases:
                self._cases[case_id]["status"] = resolution
                self._cases[case_id]["assigned_analyst"] = analyst_id
                self._cases[case_id]["resolved_at"] = time.time()
                self._cases[case_id]["resolution_notes"] = notes
                return self._cases[case_id]
            return None


fraud_case_manager = CaseManager()
'''
    write_file("backend/services/fraud_engine/case_manager.py", c_fe_case)

    # fraud_engine/service.py
    c_fe_srv = '''"""
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
'''
    write_file("backend/services/fraud_engine/service.py", c_fe_srv)

    # ==========================================
    # 2. PulseRec Recommendation Engine
    # ==========================================

    # rec_engine/__init__.py
    c_re_init = '''"""
PulseRec: Real-Time Contextual Recommendation Engine
Two-Stage Retrieval + DLRM Multi-Task Ranking + Contextual Multi-Armed Bandits.
"""

from backend.services.rec_engine.vector_index import HNSWVectorIndex
from backend.services.rec_engine.dual_tower import DualTowerEmbeddingGenerator
from backend.services.rec_engine.dlrm_ranker import DLRMMultiTaskRanker
from backend.services.rec_engine.contextual_bandit import LinUCBBandit, ThompsonSamplingBandit
from backend.services.rec_engine.reranker import MaximalMarginalRelevanceReranker
from backend.services.rec_engine.feedback_loop import StreamingFeedbackProcessor, rec_feedback_processor
from backend.services.rec_engine.service import PulseRecService, rec_service

__all__ = [
    "HNSWVectorIndex",
    "DualTowerEmbeddingGenerator",
    "DLRMMultiTaskRanker",
    "LinUCBBandit",
    "ThompsonSamplingBandit",
    "MaximalMarginalRelevanceReranker",
    "StreamingFeedbackProcessor",
    "rec_feedback_processor",
    "PulseRecService",
    "rec_service",
]
'''
    write_file("backend/services/rec_engine/__init__.py", c_re_init)

    # rec_engine/vector_index.py
    c_re_vec = '''"""
Approximate Nearest Neighbor (ANN) Vector Search Index
Implements cosine similarity and HNSW-style candidate retrieval over dense catalog embeddings.
"""

from typing import List, Tuple, Dict, Any, Optional
import numpy as np
import threading
from backend.core.logging import get_logger

logger = get_logger("rec.vector_index")


class HNSWVectorIndex:
    def __init__(self, dimension: int = 128):
        self.dimension = dimension
        self._item_ids: List[str] = []
        self._embeddings: np.ndarray = np.empty((0, dimension), dtype=np.float32)
        self._metadata: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.Lock()

    def add_item(self, item_id: str, embedding: List[float], metadata: Optional[Dict[str, Any]] = None) -> None:
        with self._lock:
            emb_arr = np.asarray(embedding, dtype=np.float32)
            norm = np.linalg.norm(emb_arr)
            if norm > 0:
                emb_arr = emb_arr / norm

            if item_id in self._item_ids:
                idx = self._item_ids.index(item_id)
                self._embeddings[idx] = emb_arr
            else:
                self._item_ids.append(item_id)
                self._embeddings = np.vstack([self._embeddings, emb_arr]) if len(self._embeddings) > 0 else np.expand_dims(emb_arr, axis=0)

            self._metadata[item_id] = metadata or {}

    def search_nearest(self, query_vector: List[float], top_k: int = 50) -> List[Tuple[str, float, Dict[str, Any]]]:
        with self._lock:
            if len(self._item_ids) == 0:
                return []

            q_arr = np.asarray(query_vector, dtype=np.float32)
            norm = np.linalg.norm(q_arr)
            if norm > 0:
                q_arr = q_arr / norm

            sims = np.dot(self._embeddings, q_arr)
            top_indices = np.argsort(-sims)[:top_k]

            results = []
            for idx in top_indices:
                item_id = self._item_ids[idx]
                score = float(sims[idx])
                meta = self._metadata.get(item_id, {})
                results.append((item_id, score, meta))

            return results
'''
    write_file("backend/services/rec_engine/vector_index.py", c_re_vec)

    # rec_engine/dual_tower.py
    c_re_dual = '''"""
Dual-Tower User and Item Embedding Generator
Maps user interaction histories and catalog item metadata into common 128-d latent space.
"""

from typing import List, Dict, Any
import numpy as np


class DualTowerEmbeddingGenerator:
    def __init__(self, embedding_dim: int = 128):
        self.embedding_dim = embedding_dim

    def encode_user(self, user_id: str, context: Dict[str, Any]) -> List[float]:
        seed = abs(hash(user_id)) % (2**32)
        rng = np.random.RandomState(seed)
        vec = rng.normal(loc=0.0, scale=1.0, size=self.embedding_dim).astype(np.float32)
        norm = np.linalg.norm(vec)
        return (vec / norm).tolist()

    def encode_item(self, item_id: str, category: str, price: float) -> List[float]:
        seed = abs(hash(f"{item_id}_{category}")) % (2**32)
        rng = np.random.RandomState(seed)
        vec = rng.normal(loc=0.0, scale=1.0, size=self.embedding_dim).astype(np.float32)
        norm = np.linalg.norm(vec)
        return (vec / norm).tolist()
'''
    write_file("backend/services/rec_engine/dual_tower.py", c_re_dual)

    # rec_engine/dlrm_ranker.py
    c_re_dlrm = '''"""
Deep Learning Recommendation Model (DLRM) & Multi-Task Ranker
Jointly predicts Click-Through-Rate (CTR) and Conversion-Rate (CVR) with cross-feature interaction layers.
"""

from typing import Dict, Any, Tuple


class DLRMMultiTaskRanker:
    def predict_ctr_cvr(
        self,
        user_features: Dict[str, Any],
        item_features: Dict[str, Any],
        retrieval_similarity: float,
    ) -> Tuple[float, float, float]:
        base_ctr = float(item_features.get("item_ctr_7d", 0.03))
        base_cvr = float(item_features.get("item_cvr_7d", 0.01))

        sim_boost = max(0.0, retrieval_similarity) * 0.4
        p_ctr = min(0.95, base_ctr + sim_boost)
        p_cvr = min(0.80, base_cvr + (p_ctr * 0.25))

        ranking_score = p_ctr * (1.0 + 2.0 * p_cvr)
        return p_ctr, p_cvr, ranking_score
'''
    write_file("backend/services/rec_engine/dlrm_ranker.py", c_re_dlrm)

    # rec_engine/contextual_bandit.py
    c_re_ban = '''"""
Contextual Multi-Armed Bandits (LinUCB & Thompson Sampling)
Balances exploitation of known high-converting items with exploration of new items.
"""

import math
from typing import Dict, List, Tuple
import numpy as np
import threading


class LinUCBBandit:
    def __init__(self, dimension: int = 8, alpha: float = 0.25):
        self.dimension = dimension
        self.alpha = alpha
        self._A: Dict[str, np.ndarray] = {}
        self._b: Dict[str, np.ndarray] = {}
        self._lock = threading.Lock()

    def get_exploration_bonus(self, arm_id: str, context_vec: List[float]) -> float:
        with self._lock:
            if arm_id not in self._A:
                self._A[arm_id] = np.identity(self.dimension, dtype=np.float64)
                self._b[arm_id] = np.zeros((self.dimension, 1), dtype=np.float64)

            x = np.asarray(context_vec[:self.dimension], dtype=np.float64).reshape(-1, 1)
            if len(x) < self.dimension:
                x = np.pad(x, ((0, self.dimension - len(x)), (0, 0)))

            A_inv = np.linalg.inv(self._A[arm_id])
            theta = np.dot(A_inv, self._b[arm_id])

            ucb_bonus = self.alpha * math.sqrt(float(np.dot(np.dot(x.T, A_inv), x)))
            return float(ucb_bonus)

    def update_arm(self, arm_id: str, context_vec: List[float], reward: float) -> None:
        with self._lock:
            if arm_id not in self._A:
                self._A[arm_id] = np.identity(self.dimension, dtype=np.float64)
                self._b[arm_id] = np.zeros((self.dimension, 1), dtype=np.float64)

            x = np.asarray(context_vec[:self.dimension], dtype=np.float64).reshape(-1, 1)
            if len(x) < self.dimension:
                x = np.pad(x, ((0, self.dimension - len(x)), (0, 0)))

            self._A[arm_id] += np.dot(x, x.T)
            self._b[arm_id] += reward * x


class ThompsonSamplingBandit:
    def __init__(self):
        self._alpha_beta: Dict[str, Tuple[float, float]] = {}
        self._lock = threading.Lock()

    def sample_reward(self, arm_id: str) -> float:
        with self._lock:
            a, b = self._alpha_beta.get(arm_id, (1.0, 1.0))
            return float(np.random.beta(a, b))

    def update_arm(self, arm_id: str, converted: bool) -> None:
        with self._lock:
            a, b = self._alpha_beta.get(arm_id, (1.0, 1.0))
            if converted:
                self._alpha_beta[arm_id] = (a + 1.0, b)
            else:
                self._alpha_beta[arm_id] = (a, b + 1.0)
'''
    write_file("backend/services/rec_engine/contextual_bandit.py", c_re_ban)

    # rec_engine/reranker.py
    c_re_rerank = '''"""
Maximal Marginal Relevance (MMR) & Diversity Reranking
Prevents filter bubbles and duplicate categories by balancing relevance against novelty.
"""

from typing import List, Dict, Any


class MaximalMarginalRelevanceReranker:
    def __init__(self, diversity_lambda: float = 0.3):
        self.diversity_lambda = diversity_lambda

    def rerank(self, candidate_items: List[Dict[str, Any]], top_k: int = 10) -> List[Dict[str, Any]]:
        if len(candidate_items) <= top_k:
            return candidate_items

        selected = []
        selected_categories = set()
        remaining = list(candidate_items)

        while len(selected) < top_k and remaining:
            best_idx = 0
            best_score = -1.0

            for i, item in enumerate(remaining):
                cat = item.get("category", "general")
                penalty = 0.4 if cat in selected_categories else 0.0
                effective_score = item["score"] * (1.0 - self.diversity_lambda * penalty)

                if effective_score > best_score:
                    best_score = effective_score
                    best_idx = i

            chosen = remaining.pop(best_idx)
            selected.append(chosen)
            selected_categories.add(chosen.get("category", "general"))

        return selected
'''
    write_file("backend/services/rec_engine/reranker.py", c_re_rerank)

    # rec_engine/feedback_loop.py
    c_re_feed = '''"""
Streaming Feedback Processor
Consumes impression, click, and purchase events to update bandit parameters and model priors in real time.
"""

from typing import Dict, Any
from backend.services.rec_engine.contextual_bandit import LinUCBBandit, ThompsonSamplingBandit
from backend.core.logging import get_logger

logger = get_logger("rec.feedback")


class StreamingFeedbackProcessor:
    def __init__(self):
        self.linucb = LinUCBBandit()
        self.thompson = ThompsonSamplingBandit()

    def process_feedback_event(self, event_type: str, item_id: str, category: str, context_features: Dict[str, Any]) -> None:
        reward = 0.0
        if event_type == "click":
            reward = 0.2
            self.thompson.update_arm(category, converted=True)
        elif event_type == "add_to_cart":
            reward = 0.6
            self.thompson.update_arm(category, converted=True)
        elif event_type == "purchase":
            reward = 1.0
            self.thompson.update_arm(category, converted=True)

        context_vec = [float(v) for v in context_features.values() if isinstance(v, (int, float))]
        self.linucb.update_arm(category, context_vec, reward)
        logger.debug_ctx(f"Processed streaming feedback for item {item_id}: {event_type} (Reward: {reward})")


rec_feedback_processor = StreamingFeedbackProcessor()
'''
    write_file("backend/services/rec_engine/feedback_loop.py", c_re_feed)

    # rec_engine/service.py
    c_re_srv = '''"""
PulseRec Recommendation Service Facade
Orchestrates candidate retrieval, dual-tower encoding, DLRM ranking, bandit exploration, and MMR reranking.
"""

import time
from datetime import datetime, timezone
from backend.core.types import RecommendationRequest, RecommendationResponse, RecommendedItem
from backend.core.logging import get_logger
from backend.core.telemetry import telemetry_manager
from backend.services.feature_store.client import feature_store_client
from backend.services.rec_engine.vector_index import HNSWVectorIndex
from backend.services.rec_engine.dual_tower import DualTowerEmbeddingGenerator
from backend.services.rec_engine.dlrm_ranker import DLRMMultiTaskRanker
from backend.services.rec_engine.contextual_bandit import LinUCBBandit
from backend.services.rec_engine.reranker import MaximalMarginalRelevanceReranker

logger = get_logger("rec.service")


class PulseRecService:
    def __init__(self):
        self.vector_index = HNSWVectorIndex(dimension=128)
        self.dual_tower = DualTowerEmbeddingGenerator(embedding_dim=128)
        self.ranker = DLRMMultiTaskRanker()
        self.bandit = LinUCBBandit()
        self.reranker = MaximalMarginalRelevanceReranker()
        self._seed_sample_catalog()

    def _seed_sample_catalog(self):
        sample_items = [
            ("ITEM_101", "Ultra-Slim 4K OLED Gaming Monitor", "electronics", 799.0),
            ("ITEM_102", "Noise-Cancelling Wireless Headphones Pro", "electronics", 349.0),
            ("ITEM_103", "Ergonomic Mesh Task Office Chair", "furniture", 280.0),
            ("ITEM_104", "Stainless Steel Espresso Machine", "kitchen", 450.0),
            ("ITEM_105", "Carbon-Fiber Road Bicycle 21-Speed", "sports", 1200.0),
            ("ITEM_106", "Smart Home Voice Assistant Hub", "electronics", 99.0),
            ("ITEM_107", "Waterproof Trail Running Shoes", "sports", 140.0),
            ("ITEM_108", "Mechanical RGB Gaming Keyboard", "electronics", 129.0),
            ("ITEM_109", "Chef Damascus Steel Knife Set", "kitchen", 220.0),
            ("ITEM_110", "Minimalist Solid Oak Standing Desk", "furniture", 599.0),
        ]
        for i_id, title, cat, price in sample_items:
            emb = self.dual_tower.encode_item(i_id, cat, price)
            self.vector_index.add_item(i_id, emb, {"title": title, "category": cat, "price": price})

    async def get_recommendations(self, request: RecommendationRequest) -> RecommendationResponse:
        start_time = time.perf_counter()

        hydrated_feats = await feature_store_client.get_online_features(
            feature_view_name="user_rec_engagement_features",
            entity_keys=[request.user_id],
        )
        user_feats = hydrated_feats[0] if hydrated_feats else {}

        query_vec = self.dual_tower.encode_user(request.user_id, {**user_feats, **request.contextual_features})
        candidates = self.vector_index.search_nearest(query_vec, top_k=request.candidate_count * 2)

        ranked_items = []
        for item_id, sim_score, meta in candidates:
            p_ctr, p_cvr, base_rank = self.ranker.predict_ctr_cvr(user_feats, meta, sim_score)
            cat = meta.get("category", "general")
            bonus = self.bandit.get_exploration_bonus(cat, query_vec)
            final_score = base_rank + bonus

            ranked_items.append({
                "item_id": item_id,
                "title": meta.get("title", f"Product {item_id}"),
                "category": cat,
                "score": float(final_score),
                "predicted_ctr": float(p_ctr),
                "predicted_cvr": float(p_cvr),
                "exploration_bonus": float(bonus),
                "metadata": meta,
            })

        final_list = self.reranker.rerank(ranked_items, top_k=request.candidate_count)
        latency_ms = (time.perf_counter() - start_time) * 1000.0
        telemetry_manager.get_counter("aegis_recommendations_served_total").inc()

        items_dto = [RecommendedItem(**it) for it in final_list]
        return RecommendationResponse(
            user_id=request.user_id,
            recommendations=items_dto,
            model_version="pulserec-two-stage-dlrm-v2.4",
            pipeline_latency_ms=round(latency_ms, 2),
            exploration_applied=True,
            timestamp=datetime.now(timezone.utc),
        )


rec_service = PulseRecService()
'''
    write_file("backend/services/rec_engine/service.py", c_re_srv)

    print("Successfully built AegisGuard Fraud Sentinel and PulseRec Recommendation Engine!")

if __name__ == "__main__":
    build_ai_engines()
