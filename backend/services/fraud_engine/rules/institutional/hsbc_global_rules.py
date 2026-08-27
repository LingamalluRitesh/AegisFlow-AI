"""
Institutional Defense Matrix: HSBC Cross-Border AML & Trade Finance Fraud Defense
Institution Identifier: hsbc_global
"""

from typing import List
from backend.services.fraud_engine.rule_engine import Rule, Condition
from backend.core.types import ActionType

def get_hsbc_global_rules() -> List[Rule]:
    """Returns compliance rule definitions calibrated for HSBC Cross-Border AML & Trade Finance Fraud Defense."""
    rules = []
    rules.append(
        Rule(
            rule_id="INST_HSBC_GLOBAL_001",
            name="HSBC Cross-Border AML & Trade Finance Fraud Defense - Rule Variant #01",
            description="Institutional rule protecting against financial fraud patterns at tier level 1.",
            priority=12,
            conditions=[
                Condition(field="amount", operator=">", value=300.0),
                Condition(field="tx_count_5m", operator=">=", value=1),
                Condition(field="tx_amount_sum_1h", operator=">", value=600.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=45.0),
                Condition(field="is_new_device_used", operator="==", value=1),
            ],
            action=ActionType.MANUAL_REVIEW,
            risk_score_boost=0.428,
            is_active=True,
        )
    )
    rules.append(
        Rule(
            rule_id="INST_HSBC_GLOBAL_002",
            name="HSBC Cross-Border AML & Trade Finance Fraud Defense - Rule Variant #02",
            description="Institutional rule protecting against financial fraud patterns at tier level 2.",
            priority=14,
            conditions=[
                Condition(field="amount", operator=">", value=600.0),
                Condition(field="tx_count_5m", operator=">=", value=1),
                Condition(field="tx_amount_sum_1h", operator=">", value=1200.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=90.0),
                Condition(field="is_new_device_used", operator="==", value=0),
            ],
            action=ActionType.MANUAL_REVIEW,
            risk_score_boost=0.456,
            is_active=True,
        )
    )
    rules.append(
        Rule(
            rule_id="INST_HSBC_GLOBAL_003",
            name="HSBC Cross-Border AML & Trade Finance Fraud Defense - Rule Variant #03",
            description="Institutional rule protecting against financial fraud patterns at tier level 3.",
            priority=16,
            conditions=[
                Condition(field="amount", operator=">", value=900.0),
                Condition(field="tx_count_5m", operator=">=", value=1),
                Condition(field="tx_amount_sum_1h", operator=">", value=1800.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=135.0),
                Condition(field="is_new_device_used", operator="==", value=1),
            ],
            action=ActionType.MANUAL_REVIEW,
            risk_score_boost=0.484,
            is_active=True,
        )
    )
    rules.append(
        Rule(
            rule_id="INST_HSBC_GLOBAL_004",
            name="HSBC Cross-Border AML & Trade Finance Fraud Defense - Rule Variant #04",
            description="Institutional rule protecting against financial fraud patterns at tier level 4.",
            priority=18,
            conditions=[
                Condition(field="amount", operator=">", value=1200.0),
                Condition(field="tx_count_5m", operator=">=", value=2),
                Condition(field="tx_amount_sum_1h", operator=">", value=2400.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=180.0),
                Condition(field="is_new_device_used", operator="==", value=0),
            ],
            action=ActionType.MANUAL_REVIEW,
            risk_score_boost=0.512,
            is_active=True,
        )
    )
    rules.append(
        Rule(
            rule_id="INST_HSBC_GLOBAL_005",
            name="HSBC Cross-Border AML & Trade Finance Fraud Defense - Rule Variant #05",
            description="Institutional rule protecting against financial fraud patterns at tier level 5.",
            priority=20,
            conditions=[
                Condition(field="amount", operator=">", value=1500.0),
                Condition(field="tx_count_5m", operator=">=", value=2),
                Condition(field="tx_amount_sum_1h", operator=">", value=3000.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=225.0),
                Condition(field="is_new_device_used", operator="==", value=1),
            ],
            action=ActionType.MANUAL_REVIEW,
            risk_score_boost=0.54,
            is_active=True,
        )
    )
    rules.append(
        Rule(
            rule_id="INST_HSBC_GLOBAL_006",
            name="HSBC Cross-Border AML & Trade Finance Fraud Defense - Rule Variant #06",
            description="Institutional rule protecting against financial fraud patterns at tier level 6.",
            priority=22,
            conditions=[
                Condition(field="amount", operator=">", value=1800.0),
                Condition(field="tx_count_5m", operator=">=", value=3),
                Condition(field="tx_amount_sum_1h", operator=">", value=3600.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=270.0),
                Condition(field="is_new_device_used", operator="==", value=0),
            ],
            action=ActionType.MANUAL_REVIEW,
            risk_score_boost=0.568,
            is_active=True,
        )
    )
    rules.append(
        Rule(
            rule_id="INST_HSBC_GLOBAL_007",
            name="HSBC Cross-Border AML & Trade Finance Fraud Defense - Rule Variant #07",
            description="Institutional rule protecting against financial fraud patterns at tier level 7.",
            priority=24,
            conditions=[
                Condition(field="amount", operator=">", value=2100.0),
                Condition(field="tx_count_5m", operator=">=", value=3),
                Condition(field="tx_amount_sum_1h", operator=">", value=4200.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=315.0),
                Condition(field="is_new_device_used", operator="==", value=1),
            ],
            action=ActionType.CHALLENGE_2FA,
            risk_score_boost=0.596,
            is_active=True,
        )
    )
    rules.append(
        Rule(
            rule_id="INST_HSBC_GLOBAL_008",
            name="HSBC Cross-Border AML & Trade Finance Fraud Defense - Rule Variant #08",
            description="Institutional rule protecting against financial fraud patterns at tier level 8.",
            priority=26,
            conditions=[
                Condition(field="amount", operator=">", value=2400.0),
                Condition(field="tx_count_5m", operator=">=", value=4),
                Condition(field="tx_amount_sum_1h", operator=">", value=4800.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=360.0),
                Condition(field="is_new_device_used", operator="==", value=0),
            ],
            action=ActionType.CHALLENGE_2FA,
            risk_score_boost=0.624,
            is_active=True,
        )
    )
    rules.append(
        Rule(
            rule_id="INST_HSBC_GLOBAL_009",
            name="HSBC Cross-Border AML & Trade Finance Fraud Defense - Rule Variant #09",
            description="Institutional rule protecting against financial fraud patterns at tier level 9.",
            priority=28,
            conditions=[
                Condition(field="amount", operator=">", value=2700.0),
                Condition(field="tx_count_5m", operator=">=", value=4),
                Condition(field="tx_amount_sum_1h", operator=">", value=5400.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=405.0),
                Condition(field="is_new_device_used", operator="==", value=1),
            ],
            action=ActionType.CHALLENGE_2FA,
            risk_score_boost=0.652,
            is_active=True,
        )
    )
    rules.append(
        Rule(
            rule_id="INST_HSBC_GLOBAL_010",
            name="HSBC Cross-Border AML & Trade Finance Fraud Defense - Rule Variant #10",
            description="Institutional rule protecting against financial fraud patterns at tier level 10.",
            priority=30,
            conditions=[
                Condition(field="amount", operator=">", value=3000.0),
                Condition(field="tx_count_5m", operator=">=", value=5),
                Condition(field="tx_amount_sum_1h", operator=">", value=6000.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=450.0),
                Condition(field="is_new_device_used", operator="==", value=0),
            ],
            action=ActionType.CHALLENGE_2FA,
            risk_score_boost=0.68,
            is_active=True,
        )
    )
    rules.append(
        Rule(
            rule_id="INST_HSBC_GLOBAL_011",
            name="HSBC Cross-Border AML & Trade Finance Fraud Defense - Rule Variant #11",
            description="Institutional rule protecting against financial fraud patterns at tier level 11.",
            priority=32,
            conditions=[
                Condition(field="amount", operator=">", value=3300.0),
                Condition(field="tx_count_5m", operator=">=", value=5),
                Condition(field="tx_amount_sum_1h", operator=">", value=6600.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=495.0),
                Condition(field="is_new_device_used", operator="==", value=1),
            ],
            action=ActionType.CHALLENGE_2FA,
            risk_score_boost=0.708,
            is_active=True,
        )
    )
    rules.append(
        Rule(
            rule_id="INST_HSBC_GLOBAL_012",
            name="HSBC Cross-Border AML & Trade Finance Fraud Defense - Rule Variant #12",
            description="Institutional rule protecting against financial fraud patterns at tier level 12.",
            priority=34,
            conditions=[
                Condition(field="amount", operator=">", value=3600.0),
                Condition(field="tx_count_5m", operator=">=", value=6),
                Condition(field="tx_amount_sum_1h", operator=">", value=7200.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=540.0),
                Condition(field="is_new_device_used", operator="==", value=0),
            ],
            action=ActionType.CHALLENGE_2FA,
            risk_score_boost=0.736,
            is_active=True,
        )
    )
    rules.append(
        Rule(
            rule_id="INST_HSBC_GLOBAL_013",
            name="HSBC Cross-Border AML & Trade Finance Fraud Defense - Rule Variant #13",
            description="Institutional rule protecting against financial fraud patterns at tier level 13.",
            priority=36,
            conditions=[
                Condition(field="amount", operator=">", value=3900.0),
                Condition(field="tx_count_5m", operator=">=", value=6),
                Condition(field="tx_amount_sum_1h", operator=">", value=7800.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=585.0),
                Condition(field="is_new_device_used", operator="==", value=1),
            ],
            action=ActionType.BLOCK,
            risk_score_boost=0.764,
            is_active=True,
        )
    )
    rules.append(
        Rule(
            rule_id="INST_HSBC_GLOBAL_014",
            name="HSBC Cross-Border AML & Trade Finance Fraud Defense - Rule Variant #14",
            description="Institutional rule protecting against financial fraud patterns at tier level 14.",
            priority=38,
            conditions=[
                Condition(field="amount", operator=">", value=4200.0),
                Condition(field="tx_count_5m", operator=">=", value=7),
                Condition(field="tx_amount_sum_1h", operator=">", value=8400.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=630.0),
                Condition(field="is_new_device_used", operator="==", value=0),
            ],
            action=ActionType.BLOCK,
            risk_score_boost=0.792,
            is_active=True,
        )
    )
    rules.append(
        Rule(
            rule_id="INST_HSBC_GLOBAL_015",
            name="HSBC Cross-Border AML & Trade Finance Fraud Defense - Rule Variant #15",
            description="Institutional rule protecting against financial fraud patterns at tier level 15.",
            priority=40,
            conditions=[
                Condition(field="amount", operator=">", value=4500.0),
                Condition(field="tx_count_5m", operator=">=", value=7),
                Condition(field="tx_amount_sum_1h", operator=">", value=9000.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=675.0),
                Condition(field="is_new_device_used", operator="==", value=1),
            ],
            action=ActionType.BLOCK,
            risk_score_boost=0.82,
            is_active=True,
        )
    )
    rules.append(
        Rule(
            rule_id="INST_HSBC_GLOBAL_016",
            name="HSBC Cross-Border AML & Trade Finance Fraud Defense - Rule Variant #16",
            description="Institutional rule protecting against financial fraud patterns at tier level 16.",
            priority=42,
            conditions=[
                Condition(field="amount", operator=">", value=4800.0),
                Condition(field="tx_count_5m", operator=">=", value=8),
                Condition(field="tx_amount_sum_1h", operator=">", value=9600.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=720.0),
                Condition(field="is_new_device_used", operator="==", value=0),
            ],
            action=ActionType.BLOCK,
            risk_score_boost=0.848,
            is_active=True,
        )
    )
    rules.append(
        Rule(
            rule_id="INST_HSBC_GLOBAL_017",
            name="HSBC Cross-Border AML & Trade Finance Fraud Defense - Rule Variant #17",
            description="Institutional rule protecting against financial fraud patterns at tier level 17.",
            priority=44,
            conditions=[
                Condition(field="amount", operator=">", value=5100.0),
                Condition(field="tx_count_5m", operator=">=", value=8),
                Condition(field="tx_amount_sum_1h", operator=">", value=10200.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=765.0),
                Condition(field="is_new_device_used", operator="==", value=1),
            ],
            action=ActionType.BLOCK,
            risk_score_boost=0.876,
            is_active=True,
        )
    )
    rules.append(
        Rule(
            rule_id="INST_HSBC_GLOBAL_018",
            name="HSBC Cross-Border AML & Trade Finance Fraud Defense - Rule Variant #18",
            description="Institutional rule protecting against financial fraud patterns at tier level 18.",
            priority=46,
            conditions=[
                Condition(field="amount", operator=">", value=5400.0),
                Condition(field="tx_count_5m", operator=">=", value=9),
                Condition(field="tx_amount_sum_1h", operator=">", value=10800.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=810.0),
                Condition(field="is_new_device_used", operator="==", value=0),
            ],
            action=ActionType.BLOCK,
            risk_score_boost=0.904,
            is_active=True,
        )
    )
    rules.append(
        Rule(
            rule_id="INST_HSBC_GLOBAL_019",
            name="HSBC Cross-Border AML & Trade Finance Fraud Defense - Rule Variant #19",
            description="Institutional rule protecting against financial fraud patterns at tier level 19.",
            priority=48,
            conditions=[
                Condition(field="amount", operator=">", value=5700.0),
                Condition(field="tx_count_5m", operator=">=", value=9),
                Condition(field="tx_amount_sum_1h", operator=">", value=11400.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=855.0),
                Condition(field="is_new_device_used", operator="==", value=1),
            ],
            action=ActionType.BLOCK,
            risk_score_boost=0.932,
            is_active=True,
        )
    )
    rules.append(
        Rule(
            rule_id="INST_HSBC_GLOBAL_020",
            name="HSBC Cross-Border AML & Trade Finance Fraud Defense - Rule Variant #20",
            description="Institutional rule protecting against financial fraud patterns at tier level 20.",
            priority=50,
            conditions=[
                Condition(field="amount", operator=">", value=6000.0),
                Condition(field="tx_count_5m", operator=">=", value=10),
                Condition(field="tx_amount_sum_1h", operator=">", value=12000.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=900.0),
                Condition(field="is_new_device_used", operator="==", value=0),
            ],
            action=ActionType.BLOCK,
            risk_score_boost=0.96,
            is_active=True,
        )
    )
    return rules
