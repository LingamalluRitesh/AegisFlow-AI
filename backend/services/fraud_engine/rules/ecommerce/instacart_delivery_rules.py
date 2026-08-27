"""
E-Commerce & Digital Economy Defense Matrix: Instacart Shopper Substitution & Tip Baiting Anomaly Matrix
Platform Key: instacart_delivery
"""

from typing import List
from backend.services.fraud_engine.rule_engine import Rule, Condition
from backend.core.types import ActionType

def get_instacart_delivery_rules() -> List[Rule]:
    """Returns full calibrated fraud rules for Instacart Shopper Substitution & Tip Baiting Anomaly Matrix."""
    rules = []
    rules.append(
        Rule(
            rule_id="ECOM_INSTACART_DELIVERY_001",
            name="Instacart Shopper Substitution & Tip Baiting Anomaly Matrix - Rule #01",
            description="E-commerce abuse and velocity check calibrated for Instacart Shopper Substitution & Tip Baiting Anomaly Matrix at tier 1.",
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
            rule_id="ECOM_INSTACART_DELIVERY_002",
            name="Instacart Shopper Substitution & Tip Baiting Anomaly Matrix - Rule #02",
            description="E-commerce abuse and velocity check calibrated for Instacart Shopper Substitution & Tip Baiting Anomaly Matrix at tier 2.",
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
            rule_id="ECOM_INSTACART_DELIVERY_003",
            name="Instacart Shopper Substitution & Tip Baiting Anomaly Matrix - Rule #03",
            description="E-commerce abuse and velocity check calibrated for Instacart Shopper Substitution & Tip Baiting Anomaly Matrix at tier 3.",
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
            rule_id="ECOM_INSTACART_DELIVERY_004",
            name="Instacart Shopper Substitution & Tip Baiting Anomaly Matrix - Rule #04",
            description="E-commerce abuse and velocity check calibrated for Instacart Shopper Substitution & Tip Baiting Anomaly Matrix at tier 4.",
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
            rule_id="ECOM_INSTACART_DELIVERY_005",
            name="Instacart Shopper Substitution & Tip Baiting Anomaly Matrix - Rule #05",
            description="E-commerce abuse and velocity check calibrated for Instacart Shopper Substitution & Tip Baiting Anomaly Matrix at tier 5.",
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
            rule_id="ECOM_INSTACART_DELIVERY_006",
            name="Instacart Shopper Substitution & Tip Baiting Anomaly Matrix - Rule #06",
            description="E-commerce abuse and velocity check calibrated for Instacart Shopper Substitution & Tip Baiting Anomaly Matrix at tier 6.",
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
            rule_id="ECOM_INSTACART_DELIVERY_007",
            name="Instacart Shopper Substitution & Tip Baiting Anomaly Matrix - Rule #07",
            description="E-commerce abuse and velocity check calibrated for Instacart Shopper Substitution & Tip Baiting Anomaly Matrix at tier 7.",
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
            rule_id="ECOM_INSTACART_DELIVERY_008",
            name="Instacart Shopper Substitution & Tip Baiting Anomaly Matrix - Rule #08",
            description="E-commerce abuse and velocity check calibrated for Instacart Shopper Substitution & Tip Baiting Anomaly Matrix at tier 8.",
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
            rule_id="ECOM_INSTACART_DELIVERY_009",
            name="Instacart Shopper Substitution & Tip Baiting Anomaly Matrix - Rule #09",
            description="E-commerce abuse and velocity check calibrated for Instacart Shopper Substitution & Tip Baiting Anomaly Matrix at tier 9.",
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
            rule_id="ECOM_INSTACART_DELIVERY_010",
            name="Instacart Shopper Substitution & Tip Baiting Anomaly Matrix - Rule #10",
            description="E-commerce abuse and velocity check calibrated for Instacart Shopper Substitution & Tip Baiting Anomaly Matrix at tier 10.",
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
            rule_id="ECOM_INSTACART_DELIVERY_011",
            name="Instacart Shopper Substitution & Tip Baiting Anomaly Matrix - Rule #11",
            description="E-commerce abuse and velocity check calibrated for Instacart Shopper Substitution & Tip Baiting Anomaly Matrix at tier 11.",
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
            rule_id="ECOM_INSTACART_DELIVERY_012",
            name="Instacart Shopper Substitution & Tip Baiting Anomaly Matrix - Rule #12",
            description="E-commerce abuse and velocity check calibrated for Instacart Shopper Substitution & Tip Baiting Anomaly Matrix at tier 12.",
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
            rule_id="ECOM_INSTACART_DELIVERY_013",
            name="Instacart Shopper Substitution & Tip Baiting Anomaly Matrix - Rule #13",
            description="E-commerce abuse and velocity check calibrated for Instacart Shopper Substitution & Tip Baiting Anomaly Matrix at tier 13.",
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
            rule_id="ECOM_INSTACART_DELIVERY_014",
            name="Instacart Shopper Substitution & Tip Baiting Anomaly Matrix - Rule #14",
            description="E-commerce abuse and velocity check calibrated for Instacart Shopper Substitution & Tip Baiting Anomaly Matrix at tier 14.",
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
            rule_id="ECOM_INSTACART_DELIVERY_015",
            name="Instacart Shopper Substitution & Tip Baiting Anomaly Matrix - Rule #15",
            description="E-commerce abuse and velocity check calibrated for Instacart Shopper Substitution & Tip Baiting Anomaly Matrix at tier 15.",
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
            rule_id="ECOM_INSTACART_DELIVERY_016",
            name="Instacart Shopper Substitution & Tip Baiting Anomaly Matrix - Rule #16",
            description="E-commerce abuse and velocity check calibrated for Instacart Shopper Substitution & Tip Baiting Anomaly Matrix at tier 16.",
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
            rule_id="ECOM_INSTACART_DELIVERY_017",
            name="Instacart Shopper Substitution & Tip Baiting Anomaly Matrix - Rule #17",
            description="E-commerce abuse and velocity check calibrated for Instacart Shopper Substitution & Tip Baiting Anomaly Matrix at tier 17.",
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
            rule_id="ECOM_INSTACART_DELIVERY_018",
            name="Instacart Shopper Substitution & Tip Baiting Anomaly Matrix - Rule #18",
            description="E-commerce abuse and velocity check calibrated for Instacart Shopper Substitution & Tip Baiting Anomaly Matrix at tier 18.",
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
            rule_id="ECOM_INSTACART_DELIVERY_019",
            name="Instacart Shopper Substitution & Tip Baiting Anomaly Matrix - Rule #19",
            description="E-commerce abuse and velocity check calibrated for Instacart Shopper Substitution & Tip Baiting Anomaly Matrix at tier 19.",
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
            rule_id="ECOM_INSTACART_DELIVERY_020",
            name="Instacart Shopper Substitution & Tip Baiting Anomaly Matrix - Rule #20",
            description="E-commerce abuse and velocity check calibrated for Instacart Shopper Substitution & Tip Baiting Anomaly Matrix at tier 20.",
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
            rule_id="ECOM_INSTACART_DELIVERY_021",
            name="Instacart Shopper Substitution & Tip Baiting Anomaly Matrix - Rule #21",
            description="E-commerce abuse and velocity check calibrated for Instacart Shopper Substitution & Tip Baiting Anomaly Matrix at tier 21.",
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
            rule_id="ECOM_INSTACART_DELIVERY_022",
            name="Instacart Shopper Substitution & Tip Baiting Anomaly Matrix - Rule #22",
            description="E-commerce abuse and velocity check calibrated for Instacart Shopper Substitution & Tip Baiting Anomaly Matrix at tier 22.",
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
            rule_id="ECOM_INSTACART_DELIVERY_023",
            name="Instacart Shopper Substitution & Tip Baiting Anomaly Matrix - Rule #23",
            description="E-commerce abuse and velocity check calibrated for Instacart Shopper Substitution & Tip Baiting Anomaly Matrix at tier 23.",
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
            rule_id="ECOM_INSTACART_DELIVERY_024",
            name="Instacart Shopper Substitution & Tip Baiting Anomaly Matrix - Rule #24",
            description="E-commerce abuse and velocity check calibrated for Instacart Shopper Substitution & Tip Baiting Anomaly Matrix at tier 24.",
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
            rule_id="ECOM_INSTACART_DELIVERY_025",
            name="Instacart Shopper Substitution & Tip Baiting Anomaly Matrix - Rule #25",
            description="E-commerce abuse and velocity check calibrated for Instacart Shopper Substitution & Tip Baiting Anomaly Matrix at tier 25.",
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
