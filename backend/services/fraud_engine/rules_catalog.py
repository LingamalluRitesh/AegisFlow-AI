"""
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
