"""
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
