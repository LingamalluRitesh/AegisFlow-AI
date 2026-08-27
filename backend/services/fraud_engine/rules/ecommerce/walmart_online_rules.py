"""
E-Commerce & Digital Economy Defense Matrix: Walmart Marketplace Gift Card & Triangulation Defense
Platform Key: walmart_online
"""

from typing import List
from backend.services.fraud_engine.rule_engine import Rule, Condition
from backend.core.types import ActionType

def get_walmart_online_rules() -> List[Rule]:
    """Returns full calibrated fraud rules for Walmart Marketplace Gift Card & Triangulation Defense."""
    rules = []
    rules.append(
        Rule(
            rule_id="ECOM_WALMART_ONLINE_001",
            name="Walmart Marketplace Gift Card & Triangulation Defense - Rule #01",
            description="E-commerce abuse and velocity check calibrated for Walmart Marketplace Gift Card & Triangulation Defense at tier 1.",
            priority=7,
            conditions=[
                Condition(field="amount", operator=">", value=60.0),
                Condition(field="tx_count_5m", operator=">=", value=1),
                Condition(field="tx_amount_sum_1h", operator=">", value=120.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=30.0),
                Condition(field="is_new_device_used", operator="==", value=1),
            ],
            action=ActionType.MANUAL_REVIEW,
            risk_score_boost=0.422,
            is_active=True,
        )
    )
    rules.append(
        Rule(
            rule_id="ECOM_WALMART_ONLINE_002",
            name="Walmart Marketplace Gift Card & Triangulation Defense - Rule #02",
            description="E-commerce abuse and velocity check calibrated for Walmart Marketplace Gift Card & Triangulation Defense at tier 2.",
            priority=9,
            conditions=[
                Condition(field="amount", operator=">", value=110.0),
                Condition(field="tx_count_5m", operator=">=", value=1),
                Condition(field="tx_amount_sum_1h", operator=">", value=240.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=60.0),
                Condition(field="is_new_device_used", operator="==", value=0),
            ],
            action=ActionType.MANUAL_REVIEW,
            risk_score_boost=0.444,
            is_active=True,
        )
    )
    rules.append(
        Rule(
            rule_id="ECOM_WALMART_ONLINE_003",
            name="Walmart Marketplace Gift Card & Triangulation Defense - Rule #03",
            description="E-commerce abuse and velocity check calibrated for Walmart Marketplace Gift Card & Triangulation Defense at tier 3.",
            priority=11,
            conditions=[
                Condition(field="amount", operator=">", value=160.0),
                Condition(field="tx_count_5m", operator=">=", value=1),
                Condition(field="tx_amount_sum_1h", operator=">", value=360.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=90.0),
                Condition(field="is_new_device_used", operator="==", value=1),
            ],
            action=ActionType.MANUAL_REVIEW,
            risk_score_boost=0.466,
            is_active=True,
        )
    )
    rules.append(
        Rule(
            rule_id="ECOM_WALMART_ONLINE_004",
            name="Walmart Marketplace Gift Card & Triangulation Defense - Rule #04",
            description="E-commerce abuse and velocity check calibrated for Walmart Marketplace Gift Card & Triangulation Defense at tier 4.",
            priority=13,
            conditions=[
                Condition(field="amount", operator=">", value=210.0),
                Condition(field="tx_count_5m", operator=">=", value=1),
                Condition(field="tx_amount_sum_1h", operator=">", value=480.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=120.0),
                Condition(field="is_new_device_used", operator="==", value=0),
            ],
            action=ActionType.MANUAL_REVIEW,
            risk_score_boost=0.488,
            is_active=True,
        )
    )
    rules.append(
        Rule(
            rule_id="ECOM_WALMART_ONLINE_005",
            name="Walmart Marketplace Gift Card & Triangulation Defense - Rule #05",
            description="E-commerce abuse and velocity check calibrated for Walmart Marketplace Gift Card & Triangulation Defense at tier 5.",
            priority=15,
            conditions=[
                Condition(field="amount", operator=">", value=260.0),
                Condition(field="tx_count_5m", operator=">=", value=1),
                Condition(field="tx_amount_sum_1h", operator=">", value=600.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=150.0),
                Condition(field="is_new_device_used", operator="==", value=1),
            ],
            action=ActionType.MANUAL_REVIEW,
            risk_score_boost=0.51,
            is_active=True,
        )
    )
    rules.append(
        Rule(
            rule_id="ECOM_WALMART_ONLINE_006",
            name="Walmart Marketplace Gift Card & Triangulation Defense - Rule #06",
            description="E-commerce abuse and velocity check calibrated for Walmart Marketplace Gift Card & Triangulation Defense at tier 6.",
            priority=17,
            conditions=[
                Condition(field="amount", operator=">", value=310.0),
                Condition(field="tx_count_5m", operator=">=", value=2),
                Condition(field="tx_amount_sum_1h", operator=">", value=720.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=180.0),
                Condition(field="is_new_device_used", operator="==", value=0),
                Condition(field="distinct_ips_24h", operator=">=", value=3),
            ],
            action=ActionType.MANUAL_REVIEW,
            risk_score_boost=0.532,
            is_active=True,
        )
    )
    rules.append(
        Rule(
            rule_id="ECOM_WALMART_ONLINE_007",
            name="Walmart Marketplace Gift Card & Triangulation Defense - Rule #07",
            description="E-commerce abuse and velocity check calibrated for Walmart Marketplace Gift Card & Triangulation Defense at tier 7.",
            priority=19,
            conditions=[
                Condition(field="amount", operator=">", value=360.0),
                Condition(field="tx_count_5m", operator=">=", value=2),
                Condition(field="tx_amount_sum_1h", operator=">", value=840.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=210.0),
                Condition(field="is_new_device_used", operator="==", value=1),
                Condition(field="distinct_ips_24h", operator=">=", value=4),
            ],
            action=ActionType.MANUAL_REVIEW,
            risk_score_boost=0.554,
            is_active=True,
        )
    )
    rules.append(
        Rule(
            rule_id="ECOM_WALMART_ONLINE_008",
            name="Walmart Marketplace Gift Card & Triangulation Defense - Rule #08",
            description="E-commerce abuse and velocity check calibrated for Walmart Marketplace Gift Card & Triangulation Defense at tier 8.",
            priority=21,
            conditions=[
                Condition(field="amount", operator=">", value=410.0),
                Condition(field="tx_count_5m", operator=">=", value=2),
                Condition(field="tx_amount_sum_1h", operator=">", value=960.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=240.0),
                Condition(field="is_new_device_used", operator="==", value=0),
                Condition(field="distinct_ips_24h", operator=">=", value=1),
            ],
            action=ActionType.MANUAL_REVIEW,
            risk_score_boost=0.576,
            is_active=True,
        )
    )
    rules.append(
        Rule(
            rule_id="ECOM_WALMART_ONLINE_009",
            name="Walmart Marketplace Gift Card & Triangulation Defense - Rule #09",
            description="E-commerce abuse and velocity check calibrated for Walmart Marketplace Gift Card & Triangulation Defense at tier 9.",
            priority=23,
            conditions=[
                Condition(field="amount", operator=">", value=460.0),
                Condition(field="tx_count_5m", operator=">=", value=3),
                Condition(field="tx_amount_sum_1h", operator=">", value=1080.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=270.0),
                Condition(field="is_new_device_used", operator="==", value=1),
                Condition(field="distinct_ips_24h", operator=">=", value=2),
            ],
            action=ActionType.CHALLENGE_2FA,
            risk_score_boost=0.598,
            is_active=True,
        )
    )
    rules.append(
        Rule(
            rule_id="ECOM_WALMART_ONLINE_010",
            name="Walmart Marketplace Gift Card & Triangulation Defense - Rule #10",
            description="E-commerce abuse and velocity check calibrated for Walmart Marketplace Gift Card & Triangulation Defense at tier 10.",
            priority=25,
            conditions=[
                Condition(field="amount", operator=">", value=510.0),
                Condition(field="tx_count_5m", operator=">=", value=3),
                Condition(field="tx_amount_sum_1h", operator=">", value=1200.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=300.0),
                Condition(field="is_new_device_used", operator="==", value=0),
                Condition(field="distinct_ips_24h", operator=">=", value=3),
            ],
            action=ActionType.CHALLENGE_2FA,
            risk_score_boost=0.62,
            is_active=True,
        )
    )
    rules.append(
        Rule(
            rule_id="ECOM_WALMART_ONLINE_011",
            name="Walmart Marketplace Gift Card & Triangulation Defense - Rule #11",
            description="E-commerce abuse and velocity check calibrated for Walmart Marketplace Gift Card & Triangulation Defense at tier 11.",
            priority=27,
            conditions=[
                Condition(field="amount", operator=">", value=560.0),
                Condition(field="tx_count_5m", operator=">=", value=3),
                Condition(field="tx_amount_sum_1h", operator=">", value=1320.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=330.0),
                Condition(field="is_new_device_used", operator="==", value=1),
                Condition(field="distinct_ips_24h", operator=">=", value=4),
                Condition(field="failed_tx_count_1h", operator=">=", value=3),
            ],
            action=ActionType.CHALLENGE_2FA,
            risk_score_boost=0.642,
            is_active=True,
        )
    )
    rules.append(
        Rule(
            rule_id="ECOM_WALMART_ONLINE_012",
            name="Walmart Marketplace Gift Card & Triangulation Defense - Rule #12",
            description="E-commerce abuse and velocity check calibrated for Walmart Marketplace Gift Card & Triangulation Defense at tier 12.",
            priority=29,
            conditions=[
                Condition(field="amount", operator=">", value=610.0),
                Condition(field="tx_count_5m", operator=">=", value=4),
                Condition(field="tx_amount_sum_1h", operator=">", value=1440.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=360.0),
                Condition(field="is_new_device_used", operator="==", value=0),
                Condition(field="distinct_ips_24h", operator=">=", value=1),
                Condition(field="failed_tx_count_1h", operator=">=", value=1),
            ],
            action=ActionType.CHALLENGE_2FA,
            risk_score_boost=0.664,
            is_active=True,
        )
    )
    rules.append(
        Rule(
            rule_id="ECOM_WALMART_ONLINE_013",
            name="Walmart Marketplace Gift Card & Triangulation Defense - Rule #13",
            description="E-commerce abuse and velocity check calibrated for Walmart Marketplace Gift Card & Triangulation Defense at tier 13.",
            priority=31,
            conditions=[
                Condition(field="amount", operator=">", value=660.0),
                Condition(field="tx_count_5m", operator=">=", value=4),
                Condition(field="tx_amount_sum_1h", operator=">", value=1560.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=390.0),
                Condition(field="is_new_device_used", operator="==", value=1),
                Condition(field="distinct_ips_24h", operator=">=", value=2),
                Condition(field="failed_tx_count_1h", operator=">=", value=2),
            ],
            action=ActionType.CHALLENGE_2FA,
            risk_score_boost=0.686,
            is_active=True,
        )
    )
    rules.append(
        Rule(
            rule_id="ECOM_WALMART_ONLINE_014",
            name="Walmart Marketplace Gift Card & Triangulation Defense - Rule #14",
            description="E-commerce abuse and velocity check calibrated for Walmart Marketplace Gift Card & Triangulation Defense at tier 14.",
            priority=33,
            conditions=[
                Condition(field="amount", operator=">", value=710.0),
                Condition(field="tx_count_5m", operator=">=", value=4),
                Condition(field="tx_amount_sum_1h", operator=">", value=1680.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=420.0),
                Condition(field="is_new_device_used", operator="==", value=0),
                Condition(field="distinct_ips_24h", operator=">=", value=3),
                Condition(field="failed_tx_count_1h", operator=">=", value=3),
            ],
            action=ActionType.CHALLENGE_2FA,
            risk_score_boost=0.708,
            is_active=True,
        )
    )
    rules.append(
        Rule(
            rule_id="ECOM_WALMART_ONLINE_015",
            name="Walmart Marketplace Gift Card & Triangulation Defense - Rule #15",
            description="E-commerce abuse and velocity check calibrated for Walmart Marketplace Gift Card & Triangulation Defense at tier 15.",
            priority=35,
            conditions=[
                Condition(field="amount", operator=">", value=760.0),
                Condition(field="tx_count_5m", operator=">=", value=5),
                Condition(field="tx_amount_sum_1h", operator=">", value=1800.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=450.0),
                Condition(field="is_new_device_used", operator="==", value=1),
                Condition(field="distinct_ips_24h", operator=">=", value=4),
                Condition(field="failed_tx_count_1h", operator=">=", value=1),
            ],
            action=ActionType.CHALLENGE_2FA,
            risk_score_boost=0.73,
            is_active=True,
        )
    )
    rules.append(
        Rule(
            rule_id="ECOM_WALMART_ONLINE_016",
            name="Walmart Marketplace Gift Card & Triangulation Defense - Rule #16",
            description="E-commerce abuse and velocity check calibrated for Walmart Marketplace Gift Card & Triangulation Defense at tier 16.",
            priority=37,
            conditions=[
                Condition(field="amount", operator=">", value=810.0),
                Condition(field="tx_count_5m", operator=">=", value=5),
                Condition(field="tx_amount_sum_1h", operator=">", value=1920.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=480.0),
                Condition(field="is_new_device_used", operator="==", value=0),
                Condition(field="distinct_ips_24h", operator=">=", value=1),
                Condition(field="failed_tx_count_1h", operator=">=", value=2),
            ],
            action=ActionType.CHALLENGE_2FA,
            risk_score_boost=0.752,
            is_active=True,
        )
    )
    rules.append(
        Rule(
            rule_id="ECOM_WALMART_ONLINE_017",
            name="Walmart Marketplace Gift Card & Triangulation Defense - Rule #17",
            description="E-commerce abuse and velocity check calibrated for Walmart Marketplace Gift Card & Triangulation Defense at tier 17.",
            priority=39,
            conditions=[
                Condition(field="amount", operator=">", value=860.0),
                Condition(field="tx_count_5m", operator=">=", value=5),
                Condition(field="tx_amount_sum_1h", operator=">", value=2040.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=510.0),
                Condition(field="is_new_device_used", operator="==", value=1),
                Condition(field="distinct_ips_24h", operator=">=", value=2),
                Condition(field="failed_tx_count_1h", operator=">=", value=3),
            ],
            action=ActionType.BLOCK,
            risk_score_boost=0.774,
            is_active=True,
        )
    )
    rules.append(
        Rule(
            rule_id="ECOM_WALMART_ONLINE_018",
            name="Walmart Marketplace Gift Card & Triangulation Defense - Rule #18",
            description="E-commerce abuse and velocity check calibrated for Walmart Marketplace Gift Card & Triangulation Defense at tier 18.",
            priority=41,
            conditions=[
                Condition(field="amount", operator=">", value=910.0),
                Condition(field="tx_count_5m", operator=">=", value=6),
                Condition(field="tx_amount_sum_1h", operator=">", value=2160.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=540.0),
                Condition(field="is_new_device_used", operator="==", value=0),
                Condition(field="distinct_ips_24h", operator=">=", value=3),
                Condition(field="failed_tx_count_1h", operator=">=", value=1),
            ],
            action=ActionType.BLOCK,
            risk_score_boost=0.796,
            is_active=True,
        )
    )
    rules.append(
        Rule(
            rule_id="ECOM_WALMART_ONLINE_019",
            name="Walmart Marketplace Gift Card & Triangulation Defense - Rule #19",
            description="E-commerce abuse and velocity check calibrated for Walmart Marketplace Gift Card & Triangulation Defense at tier 19.",
            priority=43,
            conditions=[
                Condition(field="amount", operator=">", value=960.0),
                Condition(field="tx_count_5m", operator=">=", value=6),
                Condition(field="tx_amount_sum_1h", operator=">", value=2280.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=570.0),
                Condition(field="is_new_device_used", operator="==", value=1),
                Condition(field="distinct_ips_24h", operator=">=", value=4),
                Condition(field="failed_tx_count_1h", operator=">=", value=2),
            ],
            action=ActionType.BLOCK,
            risk_score_boost=0.818,
            is_active=True,
        )
    )
    rules.append(
        Rule(
            rule_id="ECOM_WALMART_ONLINE_020",
            name="Walmart Marketplace Gift Card & Triangulation Defense - Rule #20",
            description="E-commerce abuse and velocity check calibrated for Walmart Marketplace Gift Card & Triangulation Defense at tier 20.",
            priority=45,
            conditions=[
                Condition(field="amount", operator=">", value=1010.0),
                Condition(field="tx_count_5m", operator=">=", value=6),
                Condition(field="tx_amount_sum_1h", operator=">", value=2400.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=600.0),
                Condition(field="is_new_device_used", operator="==", value=0),
                Condition(field="distinct_ips_24h", operator=">=", value=1),
                Condition(field="failed_tx_count_1h", operator=">=", value=3),
            ],
            action=ActionType.BLOCK,
            risk_score_boost=0.84,
            is_active=True,
        )
    )
    rules.append(
        Rule(
            rule_id="ECOM_WALMART_ONLINE_021",
            name="Walmart Marketplace Gift Card & Triangulation Defense - Rule #21",
            description="E-commerce abuse and velocity check calibrated for Walmart Marketplace Gift Card & Triangulation Defense at tier 21.",
            priority=47,
            conditions=[
                Condition(field="amount", operator=">", value=1060.0),
                Condition(field="tx_count_5m", operator=">=", value=7),
                Condition(field="tx_amount_sum_1h", operator=">", value=2520.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=630.0),
                Condition(field="is_new_device_used", operator="==", value=1),
                Condition(field="distinct_ips_24h", operator=">=", value=2),
                Condition(field="failed_tx_count_1h", operator=">=", value=1),
            ],
            action=ActionType.BLOCK,
            risk_score_boost=0.862,
            is_active=True,
        )
    )
    rules.append(
        Rule(
            rule_id="ECOM_WALMART_ONLINE_022",
            name="Walmart Marketplace Gift Card & Triangulation Defense - Rule #22",
            description="E-commerce abuse and velocity check calibrated for Walmart Marketplace Gift Card & Triangulation Defense at tier 22.",
            priority=49,
            conditions=[
                Condition(field="amount", operator=">", value=1110.0),
                Condition(field="tx_count_5m", operator=">=", value=7),
                Condition(field="tx_amount_sum_1h", operator=">", value=2640.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=660.0),
                Condition(field="is_new_device_used", operator="==", value=0),
                Condition(field="distinct_ips_24h", operator=">=", value=3),
                Condition(field="failed_tx_count_1h", operator=">=", value=2),
            ],
            action=ActionType.BLOCK,
            risk_score_boost=0.884,
            is_active=True,
        )
    )
    rules.append(
        Rule(
            rule_id="ECOM_WALMART_ONLINE_023",
            name="Walmart Marketplace Gift Card & Triangulation Defense - Rule #23",
            description="E-commerce abuse and velocity check calibrated for Walmart Marketplace Gift Card & Triangulation Defense at tier 23.",
            priority=51,
            conditions=[
                Condition(field="amount", operator=">", value=1160.0),
                Condition(field="tx_count_5m", operator=">=", value=7),
                Condition(field="tx_amount_sum_1h", operator=">", value=2760.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=690.0),
                Condition(field="is_new_device_used", operator="==", value=1),
                Condition(field="distinct_ips_24h", operator=">=", value=4),
                Condition(field="failed_tx_count_1h", operator=">=", value=3),
            ],
            action=ActionType.BLOCK,
            risk_score_boost=0.906,
            is_active=True,
        )
    )
    rules.append(
        Rule(
            rule_id="ECOM_WALMART_ONLINE_024",
            name="Walmart Marketplace Gift Card & Triangulation Defense - Rule #24",
            description="E-commerce abuse and velocity check calibrated for Walmart Marketplace Gift Card & Triangulation Defense at tier 24.",
            priority=53,
            conditions=[
                Condition(field="amount", operator=">", value=1210.0),
                Condition(field="tx_count_5m", operator=">=", value=8),
                Condition(field="tx_amount_sum_1h", operator=">", value=2880.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=720.0),
                Condition(field="is_new_device_used", operator="==", value=0),
                Condition(field="distinct_ips_24h", operator=">=", value=1),
                Condition(field="failed_tx_count_1h", operator=">=", value=1),
            ],
            action=ActionType.BLOCK,
            risk_score_boost=0.928,
            is_active=True,
        )
    )
    rules.append(
        Rule(
            rule_id="ECOM_WALMART_ONLINE_025",
            name="Walmart Marketplace Gift Card & Triangulation Defense - Rule #25",
            description="E-commerce abuse and velocity check calibrated for Walmart Marketplace Gift Card & Triangulation Defense at tier 25.",
            priority=55,
            conditions=[
                Condition(field="amount", operator=">", value=1260.0),
                Condition(field="tx_count_5m", operator=">=", value=8),
                Condition(field="tx_amount_sum_1h", operator=">", value=3000.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=750.0),
                Condition(field="is_new_device_used", operator="==", value=1),
                Condition(field="distinct_ips_24h", operator=">=", value=2),
                Condition(field="failed_tx_count_1h", operator=">=", value=2),
            ],
            action=ActionType.BLOCK,
            risk_score_boost=0.95,
            is_active=True,
        )
    )
    return rules
