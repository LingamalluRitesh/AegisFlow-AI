"""
Healthcare & Insurance Defense Matrix: Phantom Billing & Non-Rendered Service Claims Shield
Domain Key: phantom_billing
"""

from typing import List
from backend.services.fraud_engine.rule_engine import Rule, Condition
from backend.core.types import ActionType

def get_phantom_billing_rules() -> List[Rule]:
    """Returns full calibrated rules for Phantom Billing & Non-Rendered Service Claims Shield."""
    rules = []
    rules.append(
        Rule(
            rule_id="HLTH_PHANTOM_BILLING_001",
            name="Phantom Billing & Non-Rendered Service Claims Shield - Rule #01",
            description="Healthcare and insurance anomaly evaluation for phantom_billing at tier 1.",
            priority=7,
            conditions=[
                Condition(field="amount", operator=">", value=120.0),
                Condition(field="tx_count_5m", operator=">=", value=1),
                Condition(field="tx_amount_sum_1h", operator=">", value=250.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=40.0),
                Condition(field="is_new_device_used", operator="==", value=1),
            ],
            action=ActionType.MANUAL_REVIEW,
            risk_score_boost=0.433,
            is_active=True,
        )
    )
    rules.append(
        Rule(
            rule_id="HLTH_PHANTOM_BILLING_002",
            name="Phantom Billing & Non-Rendered Service Claims Shield - Rule #02",
            description="Healthcare and insurance anomaly evaluation for phantom_billing at tier 2.",
            priority=9,
            conditions=[
                Condition(field="amount", operator=">", value=240.0),
                Condition(field="tx_count_5m", operator=">=", value=1),
                Condition(field="tx_amount_sum_1h", operator=">", value=500.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=80.0),
                Condition(field="is_new_device_used", operator="==", value=0),
            ],
            action=ActionType.MANUAL_REVIEW,
            risk_score_boost=0.456,
            is_active=True,
        )
    )
    rules.append(
        Rule(
            rule_id="HLTH_PHANTOM_BILLING_003",
            name="Phantom Billing & Non-Rendered Service Claims Shield - Rule #03",
            description="Healthcare and insurance anomaly evaluation for phantom_billing at tier 3.",
            priority=11,
            conditions=[
                Condition(field="amount", operator=">", value=360.0),
                Condition(field="tx_count_5m", operator=">=", value=1),
                Condition(field="tx_amount_sum_1h", operator=">", value=750.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=120.0),
                Condition(field="is_new_device_used", operator="==", value=1),
            ],
            action=ActionType.MANUAL_REVIEW,
            risk_score_boost=0.479,
            is_active=True,
        )
    )
    rules.append(
        Rule(
            rule_id="HLTH_PHANTOM_BILLING_004",
            name="Phantom Billing & Non-Rendered Service Claims Shield - Rule #04",
            description="Healthcare and insurance anomaly evaluation for phantom_billing at tier 4.",
            priority=13,
            conditions=[
                Condition(field="amount", operator=">", value=480.0),
                Condition(field="tx_count_5m", operator=">=", value=1),
                Condition(field="tx_amount_sum_1h", operator=">", value=1000.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=160.0),
                Condition(field="is_new_device_used", operator="==", value=0),
            ],
            action=ActionType.MANUAL_REVIEW,
            risk_score_boost=0.502,
            is_active=True,
        )
    )
    rules.append(
        Rule(
            rule_id="HLTH_PHANTOM_BILLING_005",
            name="Phantom Billing & Non-Rendered Service Claims Shield - Rule #05",
            description="Healthcare and insurance anomaly evaluation for phantom_billing at tier 5.",
            priority=15,
            conditions=[
                Condition(field="amount", operator=">", value=600.0),
                Condition(field="tx_count_5m", operator=">=", value=1),
                Condition(field="tx_amount_sum_1h", operator=">", value=1250.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=200.0),
                Condition(field="is_new_device_used", operator="==", value=1),
            ],
            action=ActionType.MANUAL_REVIEW,
            risk_score_boost=0.525,
            is_active=True,
        )
    )
    rules.append(
        Rule(
            rule_id="HLTH_PHANTOM_BILLING_006",
            name="Phantom Billing & Non-Rendered Service Claims Shield - Rule #06",
            description="Healthcare and insurance anomaly evaluation for phantom_billing at tier 6.",
            priority=17,
            conditions=[
                Condition(field="amount", operator=">", value=720.0),
                Condition(field="tx_count_5m", operator=">=", value=2),
                Condition(field="tx_amount_sum_1h", operator=">", value=1500.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=240.0),
                Condition(field="is_new_device_used", operator="==", value=0),
                Condition(field="distinct_ips_24h", operator=">=", value=3),
            ],
            action=ActionType.MANUAL_REVIEW,
            risk_score_boost=0.548,
            is_active=True,
        )
    )
    rules.append(
        Rule(
            rule_id="HLTH_PHANTOM_BILLING_007",
            name="Phantom Billing & Non-Rendered Service Claims Shield - Rule #07",
            description="Healthcare and insurance anomaly evaluation for phantom_billing at tier 7.",
            priority=19,
            conditions=[
                Condition(field="amount", operator=">", value=840.0),
                Condition(field="tx_count_5m", operator=">=", value=2),
                Condition(field="tx_amount_sum_1h", operator=">", value=1750.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=280.0),
                Condition(field="is_new_device_used", operator="==", value=1),
                Condition(field="distinct_ips_24h", operator=">=", value=4),
            ],
            action=ActionType.MANUAL_REVIEW,
            risk_score_boost=0.571,
            is_active=True,
        )
    )
    rules.append(
        Rule(
            rule_id="HLTH_PHANTOM_BILLING_008",
            name="Phantom Billing & Non-Rendered Service Claims Shield - Rule #08",
            description="Healthcare and insurance anomaly evaluation for phantom_billing at tier 8.",
            priority=21,
            conditions=[
                Condition(field="amount", operator=">", value=960.0),
                Condition(field="tx_count_5m", operator=">=", value=2),
                Condition(field="tx_amount_sum_1h", operator=">", value=2000.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=320.0),
                Condition(field="is_new_device_used", operator="==", value=0),
                Condition(field="distinct_ips_24h", operator=">=", value=1),
            ],
            action=ActionType.MANUAL_REVIEW,
            risk_score_boost=0.594,
            is_active=True,
        )
    )
    rules.append(
        Rule(
            rule_id="HLTH_PHANTOM_BILLING_009",
            name="Phantom Billing & Non-Rendered Service Claims Shield - Rule #09",
            description="Healthcare and insurance anomaly evaluation for phantom_billing at tier 9.",
            priority=23,
            conditions=[
                Condition(field="amount", operator=">", value=1080.0),
                Condition(field="tx_count_5m", operator=">=", value=3),
                Condition(field="tx_amount_sum_1h", operator=">", value=2250.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=360.0),
                Condition(field="is_new_device_used", operator="==", value=1),
                Condition(field="distinct_ips_24h", operator=">=", value=2),
            ],
            action=ActionType.CHALLENGE_2FA,
            risk_score_boost=0.617,
            is_active=True,
        )
    )
    rules.append(
        Rule(
            rule_id="HLTH_PHANTOM_BILLING_010",
            name="Phantom Billing & Non-Rendered Service Claims Shield - Rule #10",
            description="Healthcare and insurance anomaly evaluation for phantom_billing at tier 10.",
            priority=25,
            conditions=[
                Condition(field="amount", operator=">", value=1200.0),
                Condition(field="tx_count_5m", operator=">=", value=3),
                Condition(field="tx_amount_sum_1h", operator=">", value=2500.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=400.0),
                Condition(field="is_new_device_used", operator="==", value=0),
                Condition(field="distinct_ips_24h", operator=">=", value=3),
            ],
            action=ActionType.CHALLENGE_2FA,
            risk_score_boost=0.64,
            is_active=True,
        )
    )
    rules.append(
        Rule(
            rule_id="HLTH_PHANTOM_BILLING_011",
            name="Phantom Billing & Non-Rendered Service Claims Shield - Rule #11",
            description="Healthcare and insurance anomaly evaluation for phantom_billing at tier 11.",
            priority=27,
            conditions=[
                Condition(field="amount", operator=">", value=1320.0),
                Condition(field="tx_count_5m", operator=">=", value=3),
                Condition(field="tx_amount_sum_1h", operator=">", value=2750.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=440.0),
                Condition(field="is_new_device_used", operator="==", value=1),
                Condition(field="distinct_ips_24h", operator=">=", value=4),
                Condition(field="failed_tx_count_1h", operator=">=", value=3),
            ],
            action=ActionType.CHALLENGE_2FA,
            risk_score_boost=0.663,
            is_active=True,
        )
    )
    rules.append(
        Rule(
            rule_id="HLTH_PHANTOM_BILLING_012",
            name="Phantom Billing & Non-Rendered Service Claims Shield - Rule #12",
            description="Healthcare and insurance anomaly evaluation for phantom_billing at tier 12.",
            priority=29,
            conditions=[
                Condition(field="amount", operator=">", value=1440.0),
                Condition(field="tx_count_5m", operator=">=", value=4),
                Condition(field="tx_amount_sum_1h", operator=">", value=3000.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=480.0),
                Condition(field="is_new_device_used", operator="==", value=0),
                Condition(field="distinct_ips_24h", operator=">=", value=1),
                Condition(field="failed_tx_count_1h", operator=">=", value=1),
            ],
            action=ActionType.CHALLENGE_2FA,
            risk_score_boost=0.686,
            is_active=True,
        )
    )
    rules.append(
        Rule(
            rule_id="HLTH_PHANTOM_BILLING_013",
            name="Phantom Billing & Non-Rendered Service Claims Shield - Rule #13",
            description="Healthcare and insurance anomaly evaluation for phantom_billing at tier 13.",
            priority=31,
            conditions=[
                Condition(field="amount", operator=">", value=1560.0),
                Condition(field="tx_count_5m", operator=">=", value=4),
                Condition(field="tx_amount_sum_1h", operator=">", value=3250.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=520.0),
                Condition(field="is_new_device_used", operator="==", value=1),
                Condition(field="distinct_ips_24h", operator=">=", value=2),
                Condition(field="failed_tx_count_1h", operator=">=", value=2),
            ],
            action=ActionType.CHALLENGE_2FA,
            risk_score_boost=0.709,
            is_active=True,
        )
    )
    rules.append(
        Rule(
            rule_id="HLTH_PHANTOM_BILLING_014",
            name="Phantom Billing & Non-Rendered Service Claims Shield - Rule #14",
            description="Healthcare and insurance anomaly evaluation for phantom_billing at tier 14.",
            priority=33,
            conditions=[
                Condition(field="amount", operator=">", value=1680.0),
                Condition(field="tx_count_5m", operator=">=", value=4),
                Condition(field="tx_amount_sum_1h", operator=">", value=3500.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=560.0),
                Condition(field="is_new_device_used", operator="==", value=0),
                Condition(field="distinct_ips_24h", operator=">=", value=3),
                Condition(field="failed_tx_count_1h", operator=">=", value=3),
            ],
            action=ActionType.CHALLENGE_2FA,
            risk_score_boost=0.732,
            is_active=True,
        )
    )
    rules.append(
        Rule(
            rule_id="HLTH_PHANTOM_BILLING_015",
            name="Phantom Billing & Non-Rendered Service Claims Shield - Rule #15",
            description="Healthcare and insurance anomaly evaluation for phantom_billing at tier 15.",
            priority=35,
            conditions=[
                Condition(field="amount", operator=">", value=1800.0),
                Condition(field="tx_count_5m", operator=">=", value=5),
                Condition(field="tx_amount_sum_1h", operator=">", value=3750.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=600.0),
                Condition(field="is_new_device_used", operator="==", value=1),
                Condition(field="distinct_ips_24h", operator=">=", value=4),
                Condition(field="failed_tx_count_1h", operator=">=", value=1),
            ],
            action=ActionType.CHALLENGE_2FA,
            risk_score_boost=0.755,
            is_active=True,
        )
    )
    rules.append(
        Rule(
            rule_id="HLTH_PHANTOM_BILLING_016",
            name="Phantom Billing & Non-Rendered Service Claims Shield - Rule #16",
            description="Healthcare and insurance anomaly evaluation for phantom_billing at tier 16.",
            priority=37,
            conditions=[
                Condition(field="amount", operator=">", value=1920.0),
                Condition(field="tx_count_5m", operator=">=", value=5),
                Condition(field="tx_amount_sum_1h", operator=">", value=4000.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=640.0),
                Condition(field="is_new_device_used", operator="==", value=0),
                Condition(field="distinct_ips_24h", operator=">=", value=1),
                Condition(field="failed_tx_count_1h", operator=">=", value=2),
            ],
            action=ActionType.CHALLENGE_2FA,
            risk_score_boost=0.778,
            is_active=True,
        )
    )
    rules.append(
        Rule(
            rule_id="HLTH_PHANTOM_BILLING_017",
            name="Phantom Billing & Non-Rendered Service Claims Shield - Rule #17",
            description="Healthcare and insurance anomaly evaluation for phantom_billing at tier 17.",
            priority=39,
            conditions=[
                Condition(field="amount", operator=">", value=2040.0),
                Condition(field="tx_count_5m", operator=">=", value=5),
                Condition(field="tx_amount_sum_1h", operator=">", value=4250.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=680.0),
                Condition(field="is_new_device_used", operator="==", value=1),
                Condition(field="distinct_ips_24h", operator=">=", value=2),
                Condition(field="failed_tx_count_1h", operator=">=", value=3),
            ],
            action=ActionType.BLOCK,
            risk_score_boost=0.801,
            is_active=True,
        )
    )
    rules.append(
        Rule(
            rule_id="HLTH_PHANTOM_BILLING_018",
            name="Phantom Billing & Non-Rendered Service Claims Shield - Rule #18",
            description="Healthcare and insurance anomaly evaluation for phantom_billing at tier 18.",
            priority=41,
            conditions=[
                Condition(field="amount", operator=">", value=2160.0),
                Condition(field="tx_count_5m", operator=">=", value=6),
                Condition(field="tx_amount_sum_1h", operator=">", value=4500.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=720.0),
                Condition(field="is_new_device_used", operator="==", value=0),
                Condition(field="distinct_ips_24h", operator=">=", value=3),
                Condition(field="failed_tx_count_1h", operator=">=", value=1),
            ],
            action=ActionType.BLOCK,
            risk_score_boost=0.824,
            is_active=True,
        )
    )
    rules.append(
        Rule(
            rule_id="HLTH_PHANTOM_BILLING_019",
            name="Phantom Billing & Non-Rendered Service Claims Shield - Rule #19",
            description="Healthcare and insurance anomaly evaluation for phantom_billing at tier 19.",
            priority=43,
            conditions=[
                Condition(field="amount", operator=">", value=2280.0),
                Condition(field="tx_count_5m", operator=">=", value=6),
                Condition(field="tx_amount_sum_1h", operator=">", value=4750.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=760.0),
                Condition(field="is_new_device_used", operator="==", value=1),
                Condition(field="distinct_ips_24h", operator=">=", value=4),
                Condition(field="failed_tx_count_1h", operator=">=", value=2),
            ],
            action=ActionType.BLOCK,
            risk_score_boost=0.847,
            is_active=True,
        )
    )
    rules.append(
        Rule(
            rule_id="HLTH_PHANTOM_BILLING_020",
            name="Phantom Billing & Non-Rendered Service Claims Shield - Rule #20",
            description="Healthcare and insurance anomaly evaluation for phantom_billing at tier 20.",
            priority=45,
            conditions=[
                Condition(field="amount", operator=">", value=2400.0),
                Condition(field="tx_count_5m", operator=">=", value=6),
                Condition(field="tx_amount_sum_1h", operator=">", value=5000.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=800.0),
                Condition(field="is_new_device_used", operator="==", value=0),
                Condition(field="distinct_ips_24h", operator=">=", value=1),
                Condition(field="failed_tx_count_1h", operator=">=", value=3),
            ],
            action=ActionType.BLOCK,
            risk_score_boost=0.87,
            is_active=True,
        )
    )
    rules.append(
        Rule(
            rule_id="HLTH_PHANTOM_BILLING_021",
            name="Phantom Billing & Non-Rendered Service Claims Shield - Rule #21",
            description="Healthcare and insurance anomaly evaluation for phantom_billing at tier 21.",
            priority=47,
            conditions=[
                Condition(field="amount", operator=">", value=2520.0),
                Condition(field="tx_count_5m", operator=">=", value=7),
                Condition(field="tx_amount_sum_1h", operator=">", value=5250.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=840.0),
                Condition(field="is_new_device_used", operator="==", value=1),
                Condition(field="distinct_ips_24h", operator=">=", value=2),
                Condition(field="failed_tx_count_1h", operator=">=", value=1),
            ],
            action=ActionType.BLOCK,
            risk_score_boost=0.893,
            is_active=True,
        )
    )
    rules.append(
        Rule(
            rule_id="HLTH_PHANTOM_BILLING_022",
            name="Phantom Billing & Non-Rendered Service Claims Shield - Rule #22",
            description="Healthcare and insurance anomaly evaluation for phantom_billing at tier 22.",
            priority=49,
            conditions=[
                Condition(field="amount", operator=">", value=2640.0),
                Condition(field="tx_count_5m", operator=">=", value=7),
                Condition(field="tx_amount_sum_1h", operator=">", value=5500.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=880.0),
                Condition(field="is_new_device_used", operator="==", value=0),
                Condition(field="distinct_ips_24h", operator=">=", value=3),
                Condition(field="failed_tx_count_1h", operator=">=", value=2),
            ],
            action=ActionType.BLOCK,
            risk_score_boost=0.916,
            is_active=True,
        )
    )
    rules.append(
        Rule(
            rule_id="HLTH_PHANTOM_BILLING_023",
            name="Phantom Billing & Non-Rendered Service Claims Shield - Rule #23",
            description="Healthcare and insurance anomaly evaluation for phantom_billing at tier 23.",
            priority=51,
            conditions=[
                Condition(field="amount", operator=">", value=2760.0),
                Condition(field="tx_count_5m", operator=">=", value=7),
                Condition(field="tx_amount_sum_1h", operator=">", value=5750.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=920.0),
                Condition(field="is_new_device_used", operator="==", value=1),
                Condition(field="distinct_ips_24h", operator=">=", value=4),
                Condition(field="failed_tx_count_1h", operator=">=", value=3),
            ],
            action=ActionType.BLOCK,
            risk_score_boost=0.939,
            is_active=True,
        )
    )
    rules.append(
        Rule(
            rule_id="HLTH_PHANTOM_BILLING_024",
            name="Phantom Billing & Non-Rendered Service Claims Shield - Rule #24",
            description="Healthcare and insurance anomaly evaluation for phantom_billing at tier 24.",
            priority=53,
            conditions=[
                Condition(field="amount", operator=">", value=2880.0),
                Condition(field="tx_count_5m", operator=">=", value=8),
                Condition(field="tx_amount_sum_1h", operator=">", value=6000.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=960.0),
                Condition(field="is_new_device_used", operator="==", value=0),
                Condition(field="distinct_ips_24h", operator=">=", value=1),
                Condition(field="failed_tx_count_1h", operator=">=", value=1),
            ],
            action=ActionType.BLOCK,
            risk_score_boost=0.962,
            is_active=True,
        )
    )
    rules.append(
        Rule(
            rule_id="HLTH_PHANTOM_BILLING_025",
            name="Phantom Billing & Non-Rendered Service Claims Shield - Rule #25",
            description="Healthcare and insurance anomaly evaluation for phantom_billing at tier 25.",
            priority=55,
            conditions=[
                Condition(field="amount", operator=">", value=3000.0),
                Condition(field="tx_count_5m", operator=">=", value=8),
                Condition(field="tx_amount_sum_1h", operator=">", value=6250.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=1000.0),
                Condition(field="is_new_device_used", operator="==", value=1),
                Condition(field="distinct_ips_24h", operator=">=", value=2),
                Condition(field="failed_tx_count_1h", operator=">=", value=2),
            ],
            action=ActionType.BLOCK,
            risk_score_boost=0.985,
            is_active=True,
        )
    )
    return rules
