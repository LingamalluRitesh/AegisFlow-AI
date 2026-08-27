"""
Healthcare & Insurance Defense Matrix: Cross-Payer Multi-Submission & Duplicate Claim Defense
Domain Key: duplicate_claims_cross_payer
"""

from typing import List
from backend.services.fraud_engine.rule_engine import Rule, Condition
from backend.core.types import ActionType

def get_duplicate_claims_cross_payer_rules() -> List[Rule]:
    """Returns full calibrated rules for Cross-Payer Multi-Submission & Duplicate Claim Defense."""
    rules = []
    rules.append(
        Rule(
            rule_id="HLTH_DUPLICATE_CLAIMS_CROSS_PAYER_001",
            name="Cross-Payer Multi-Submission & Duplicate Claim Defense - Rule #01",
            description="Healthcare and insurance anomaly evaluation for duplicate_claims_cross_payer at tier 1.",
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
            rule_id="HLTH_DUPLICATE_CLAIMS_CROSS_PAYER_002",
            name="Cross-Payer Multi-Submission & Duplicate Claim Defense - Rule #02",
            description="Healthcare and insurance anomaly evaluation for duplicate_claims_cross_payer at tier 2.",
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
            rule_id="HLTH_DUPLICATE_CLAIMS_CROSS_PAYER_003",
            name="Cross-Payer Multi-Submission & Duplicate Claim Defense - Rule #03",
            description="Healthcare and insurance anomaly evaluation for duplicate_claims_cross_payer at tier 3.",
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
            rule_id="HLTH_DUPLICATE_CLAIMS_CROSS_PAYER_004",
            name="Cross-Payer Multi-Submission & Duplicate Claim Defense - Rule #04",
            description="Healthcare and insurance anomaly evaluation for duplicate_claims_cross_payer at tier 4.",
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
            rule_id="HLTH_DUPLICATE_CLAIMS_CROSS_PAYER_005",
            name="Cross-Payer Multi-Submission & Duplicate Claim Defense - Rule #05",
            description="Healthcare and insurance anomaly evaluation for duplicate_claims_cross_payer at tier 5.",
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
            rule_id="HLTH_DUPLICATE_CLAIMS_CROSS_PAYER_006",
            name="Cross-Payer Multi-Submission & Duplicate Claim Defense - Rule #06",
            description="Healthcare and insurance anomaly evaluation for duplicate_claims_cross_payer at tier 6.",
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
            rule_id="HLTH_DUPLICATE_CLAIMS_CROSS_PAYER_007",
            name="Cross-Payer Multi-Submission & Duplicate Claim Defense - Rule #07",
            description="Healthcare and insurance anomaly evaluation for duplicate_claims_cross_payer at tier 7.",
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
            rule_id="HLTH_DUPLICATE_CLAIMS_CROSS_PAYER_008",
            name="Cross-Payer Multi-Submission & Duplicate Claim Defense - Rule #08",
            description="Healthcare and insurance anomaly evaluation for duplicate_claims_cross_payer at tier 8.",
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
            rule_id="HLTH_DUPLICATE_CLAIMS_CROSS_PAYER_009",
            name="Cross-Payer Multi-Submission & Duplicate Claim Defense - Rule #09",
            description="Healthcare and insurance anomaly evaluation for duplicate_claims_cross_payer at tier 9.",
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
            rule_id="HLTH_DUPLICATE_CLAIMS_CROSS_PAYER_010",
            name="Cross-Payer Multi-Submission & Duplicate Claim Defense - Rule #10",
            description="Healthcare and insurance anomaly evaluation for duplicate_claims_cross_payer at tier 10.",
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
            rule_id="HLTH_DUPLICATE_CLAIMS_CROSS_PAYER_011",
            name="Cross-Payer Multi-Submission & Duplicate Claim Defense - Rule #11",
            description="Healthcare and insurance anomaly evaluation for duplicate_claims_cross_payer at tier 11.",
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
            rule_id="HLTH_DUPLICATE_CLAIMS_CROSS_PAYER_012",
            name="Cross-Payer Multi-Submission & Duplicate Claim Defense - Rule #12",
            description="Healthcare and insurance anomaly evaluation for duplicate_claims_cross_payer at tier 12.",
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
            rule_id="HLTH_DUPLICATE_CLAIMS_CROSS_PAYER_013",
            name="Cross-Payer Multi-Submission & Duplicate Claim Defense - Rule #13",
            description="Healthcare and insurance anomaly evaluation for duplicate_claims_cross_payer at tier 13.",
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
            rule_id="HLTH_DUPLICATE_CLAIMS_CROSS_PAYER_014",
            name="Cross-Payer Multi-Submission & Duplicate Claim Defense - Rule #14",
            description="Healthcare and insurance anomaly evaluation for duplicate_claims_cross_payer at tier 14.",
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
            rule_id="HLTH_DUPLICATE_CLAIMS_CROSS_PAYER_015",
            name="Cross-Payer Multi-Submission & Duplicate Claim Defense - Rule #15",
            description="Healthcare and insurance anomaly evaluation for duplicate_claims_cross_payer at tier 15.",
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
            rule_id="HLTH_DUPLICATE_CLAIMS_CROSS_PAYER_016",
            name="Cross-Payer Multi-Submission & Duplicate Claim Defense - Rule #16",
            description="Healthcare and insurance anomaly evaluation for duplicate_claims_cross_payer at tier 16.",
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
            rule_id="HLTH_DUPLICATE_CLAIMS_CROSS_PAYER_017",
            name="Cross-Payer Multi-Submission & Duplicate Claim Defense - Rule #17",
            description="Healthcare and insurance anomaly evaluation for duplicate_claims_cross_payer at tier 17.",
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
            rule_id="HLTH_DUPLICATE_CLAIMS_CROSS_PAYER_018",
            name="Cross-Payer Multi-Submission & Duplicate Claim Defense - Rule #18",
            description="Healthcare and insurance anomaly evaluation for duplicate_claims_cross_payer at tier 18.",
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
            rule_id="HLTH_DUPLICATE_CLAIMS_CROSS_PAYER_019",
            name="Cross-Payer Multi-Submission & Duplicate Claim Defense - Rule #19",
            description="Healthcare and insurance anomaly evaluation for duplicate_claims_cross_payer at tier 19.",
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
            rule_id="HLTH_DUPLICATE_CLAIMS_CROSS_PAYER_020",
            name="Cross-Payer Multi-Submission & Duplicate Claim Defense - Rule #20",
            description="Healthcare and insurance anomaly evaluation for duplicate_claims_cross_payer at tier 20.",
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
            rule_id="HLTH_DUPLICATE_CLAIMS_CROSS_PAYER_021",
            name="Cross-Payer Multi-Submission & Duplicate Claim Defense - Rule #21",
            description="Healthcare and insurance anomaly evaluation for duplicate_claims_cross_payer at tier 21.",
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
            rule_id="HLTH_DUPLICATE_CLAIMS_CROSS_PAYER_022",
            name="Cross-Payer Multi-Submission & Duplicate Claim Defense - Rule #22",
            description="Healthcare and insurance anomaly evaluation for duplicate_claims_cross_payer at tier 22.",
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
            rule_id="HLTH_DUPLICATE_CLAIMS_CROSS_PAYER_023",
            name="Cross-Payer Multi-Submission & Duplicate Claim Defense - Rule #23",
            description="Healthcare and insurance anomaly evaluation for duplicate_claims_cross_payer at tier 23.",
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
            rule_id="HLTH_DUPLICATE_CLAIMS_CROSS_PAYER_024",
            name="Cross-Payer Multi-Submission & Duplicate Claim Defense - Rule #24",
            description="Healthcare and insurance anomaly evaluation for duplicate_claims_cross_payer at tier 24.",
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
            rule_id="HLTH_DUPLICATE_CLAIMS_CROSS_PAYER_025",
            name="Cross-Payer Multi-Submission & Duplicate Claim Defense - Rule #25",
            description="Healthcare and insurance anomaly evaluation for duplicate_claims_cross_payer at tier 25.",
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
