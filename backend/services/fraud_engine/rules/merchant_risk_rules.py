"""
AegisGuard Institutional Rule Suite: Merchant Risk, Collusion and High-Risk MCC Rules
Domain: merchant_risk
"""

from typing import List
from backend.services.fraud_engine.rule_engine import Rule, Condition
from backend.core.types import ActionType

def get_merchant_risk_rules() -> List[Rule]:
    rules = []
    rules.append(
        Rule(
            rule_id="RULE_MERCHANT_RISK_001",
            name="Merchant Risk, Collusion and High-Risk MCC Rules - Variant #01",
            description="Automated enterprise risk check for merchant risk, collusion and high-risk mcc rules with threshold calibrated at tier 1.",
            priority=12,
            conditions=[
                Condition(field="amount", operator=">", value=100.0),
                Condition(field="tx_count_5m", operator=">=", value=1),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=50.0),
                Condition(field="is_new_device_used", operator="==", value=1),
            ],
            action=ActionType.MANUAL_REVIEW,
            risk_score_boost=0.45,
            is_active=True,
        )
    )
    rules.append(
        Rule(
            rule_id="RULE_MERCHANT_RISK_002",
            name="Merchant Risk, Collusion and High-Risk MCC Rules - Variant #02",
            description="Automated enterprise risk check for merchant risk, collusion and high-risk mcc rules with threshold calibrated at tier 2.",
            priority=14,
            conditions=[
                Condition(field="amount", operator=">", value=200.0),
                Condition(field="tx_count_5m", operator=">=", value=1),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=100.0),
                Condition(field="is_new_device_used", operator="==", value=0),
            ],
            action=ActionType.MANUAL_REVIEW,
            risk_score_boost=0.5,
            is_active=True,
        )
    )
    rules.append(
        Rule(
            rule_id="RULE_MERCHANT_RISK_003",
            name="Merchant Risk, Collusion and High-Risk MCC Rules - Variant #03",
            description="Automated enterprise risk check for merchant risk, collusion and high-risk mcc rules with threshold calibrated at tier 3.",
            priority=16,
            conditions=[
                Condition(field="amount", operator=">", value=300.0),
                Condition(field="tx_count_5m", operator=">=", value=1),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=150.0),
                Condition(field="is_new_device_used", operator="==", value=1),
            ],
            action=ActionType.MANUAL_REVIEW,
            risk_score_boost=0.55,
            is_active=True,
        )
    )
    rules.append(
        Rule(
            rule_id="RULE_MERCHANT_RISK_004",
            name="Merchant Risk, Collusion and High-Risk MCC Rules - Variant #04",
            description="Automated enterprise risk check for merchant risk, collusion and high-risk mcc rules with threshold calibrated at tier 4.",
            priority=18,
            conditions=[
                Condition(field="amount", operator=">", value=400.0),
                Condition(field="tx_count_5m", operator=">=", value=2),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=200.0),
                Condition(field="is_new_device_used", operator="==", value=0),
            ],
            action=ActionType.CHALLENGE_2FA,
            risk_score_boost=0.6,
            is_active=True,
        )
    )
    rules.append(
        Rule(
            rule_id="RULE_MERCHANT_RISK_005",
            name="Merchant Risk, Collusion and High-Risk MCC Rules - Variant #05",
            description="Automated enterprise risk check for merchant risk, collusion and high-risk mcc rules with threshold calibrated at tier 5.",
            priority=20,
            conditions=[
                Condition(field="amount", operator=">", value=500.0),
                Condition(field="tx_count_5m", operator=">=", value=2),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=250.0),
                Condition(field="is_new_device_used", operator="==", value=1),
            ],
            action=ActionType.CHALLENGE_2FA,
            risk_score_boost=0.65,
            is_active=True,
        )
    )
    rules.append(
        Rule(
            rule_id="RULE_MERCHANT_RISK_006",
            name="Merchant Risk, Collusion and High-Risk MCC Rules - Variant #06",
            description="Automated enterprise risk check for merchant risk, collusion and high-risk mcc rules with threshold calibrated at tier 6.",
            priority=22,
            conditions=[
                Condition(field="amount", operator=">", value=600.0),
                Condition(field="tx_count_5m", operator=">=", value=3),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=300.0),
                Condition(field="is_new_device_used", operator="==", value=0),
            ],
            action=ActionType.CHALLENGE_2FA,
            risk_score_boost=0.7,
            is_active=True,
        )
    )
    rules.append(
        Rule(
            rule_id="RULE_MERCHANT_RISK_007",
            name="Merchant Risk, Collusion and High-Risk MCC Rules - Variant #07",
            description="Automated enterprise risk check for merchant risk, collusion and high-risk mcc rules with threshold calibrated at tier 7.",
            priority=24,
            conditions=[
                Condition(field="amount", operator=">", value=700.0),
                Condition(field="tx_count_5m", operator=">=", value=3),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=350.0),
                Condition(field="is_new_device_used", operator="==", value=1),
            ],
            action=ActionType.BLOCK,
            risk_score_boost=0.75,
            is_active=True,
        )
    )
    rules.append(
        Rule(
            rule_id="RULE_MERCHANT_RISK_008",
            name="Merchant Risk, Collusion and High-Risk MCC Rules - Variant #08",
            description="Automated enterprise risk check for merchant risk, collusion and high-risk mcc rules with threshold calibrated at tier 8.",
            priority=26,
            conditions=[
                Condition(field="amount", operator=">", value=800.0),
                Condition(field="tx_count_5m", operator=">=", value=4),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=400.0),
                Condition(field="is_new_device_used", operator="==", value=0),
            ],
            action=ActionType.BLOCK,
            risk_score_boost=0.8,
            is_active=True,
        )
    )
    rules.append(
        Rule(
            rule_id="RULE_MERCHANT_RISK_009",
            name="Merchant Risk, Collusion and High-Risk MCC Rules - Variant #09",
            description="Automated enterprise risk check for merchant risk, collusion and high-risk mcc rules with threshold calibrated at tier 9.",
            priority=28,
            conditions=[
                Condition(field="amount", operator=">", value=900.0),
                Condition(field="tx_count_5m", operator=">=", value=4),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=450.0),
                Condition(field="is_new_device_used", operator="==", value=1),
            ],
            action=ActionType.BLOCK,
            risk_score_boost=0.85,
            is_active=True,
        )
    )
    rules.append(
        Rule(
            rule_id="RULE_MERCHANT_RISK_010",
            name="Merchant Risk, Collusion and High-Risk MCC Rules - Variant #10",
            description="Automated enterprise risk check for merchant risk, collusion and high-risk mcc rules with threshold calibrated at tier 10.",
            priority=30,
            conditions=[
                Condition(field="amount", operator=">", value=1000.0),
                Condition(field="tx_count_5m", operator=">=", value=5),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=500.0),
                Condition(field="is_new_device_used", operator="==", value=0),
            ],
            action=ActionType.BLOCK,
            risk_score_boost=0.9,
            is_active=True,
        )
    )
    return rules
