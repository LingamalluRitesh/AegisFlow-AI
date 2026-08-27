"""
Telecom & IoT Defense Matrix: 5G Network Slice Isolation Breach & QoS Manipulation Shield
Domain Key: 5g_network_slice
"""

from typing import List
from backend.services.fraud_engine.rule_engine import Rule, Condition
from backend.core.types import ActionType

def get_5g_network_slice_rules() -> List[Rule]:
    """Returns full calibrated rules for 5G Network Slice Isolation Breach & QoS Manipulation Shield."""
    rules = []
    rules.append(
        Rule(
            rule_id="TEL_5G_NETWORK_SLICE_001",
            name="5G Network Slice Isolation Breach & QoS Manipulation Shield - Rule #01",
            description="Telecom risk and IoT telemetry anomaly check for 5g_network_slice at tier 1.",
            priority=7,
            conditions=[
                Condition(field="amount", operator=">", value=75.0),
                Condition(field="tx_count_5m", operator=">=", value=1),
                Condition(field="tx_amount_sum_1h", operator=">", value=150.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=35.0),
                Condition(field="is_new_device_used", operator="==", value=1),
            ],
            action=ActionType.MANUAL_REVIEW,
            risk_score_boost=0.441,
            is_active=True,
        )
    )
    rules.append(
        Rule(
            rule_id="TEL_5G_NETWORK_SLICE_002",
            name="5G Network Slice Isolation Breach & QoS Manipulation Shield - Rule #02",
            description="Telecom risk and IoT telemetry anomaly check for 5g_network_slice at tier 2.",
            priority=9,
            conditions=[
                Condition(field="amount", operator=">", value=150.0),
                Condition(field="tx_count_5m", operator=">=", value=1),
                Condition(field="tx_amount_sum_1h", operator=">", value=300.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=70.0),
                Condition(field="is_new_device_used", operator="==", value=0),
            ],
            action=ActionType.MANUAL_REVIEW,
            risk_score_boost=0.462,
            is_active=True,
        )
    )
    rules.append(
        Rule(
            rule_id="TEL_5G_NETWORK_SLICE_003",
            name="5G Network Slice Isolation Breach & QoS Manipulation Shield - Rule #03",
            description="Telecom risk and IoT telemetry anomaly check for 5g_network_slice at tier 3.",
            priority=11,
            conditions=[
                Condition(field="amount", operator=">", value=225.0),
                Condition(field="tx_count_5m", operator=">=", value=1),
                Condition(field="tx_amount_sum_1h", operator=">", value=450.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=105.0),
                Condition(field="is_new_device_used", operator="==", value=1),
            ],
            action=ActionType.MANUAL_REVIEW,
            risk_score_boost=0.483,
            is_active=True,
        )
    )
    rules.append(
        Rule(
            rule_id="TEL_5G_NETWORK_SLICE_004",
            name="5G Network Slice Isolation Breach & QoS Manipulation Shield - Rule #04",
            description="Telecom risk and IoT telemetry anomaly check for 5g_network_slice at tier 4.",
            priority=13,
            conditions=[
                Condition(field="amount", operator=">", value=300.0),
                Condition(field="tx_count_5m", operator=">=", value=1),
                Condition(field="tx_amount_sum_1h", operator=">", value=600.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=140.0),
                Condition(field="is_new_device_used", operator="==", value=0),
            ],
            action=ActionType.MANUAL_REVIEW,
            risk_score_boost=0.504,
            is_active=True,
        )
    )
    rules.append(
        Rule(
            rule_id="TEL_5G_NETWORK_SLICE_005",
            name="5G Network Slice Isolation Breach & QoS Manipulation Shield - Rule #05",
            description="Telecom risk and IoT telemetry anomaly check for 5g_network_slice at tier 5.",
            priority=15,
            conditions=[
                Condition(field="amount", operator=">", value=375.0),
                Condition(field="tx_count_5m", operator=">=", value=1),
                Condition(field="tx_amount_sum_1h", operator=">", value=750.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=175.0),
                Condition(field="is_new_device_used", operator="==", value=1),
            ],
            action=ActionType.MANUAL_REVIEW,
            risk_score_boost=0.525,
            is_active=True,
        )
    )
    rules.append(
        Rule(
            rule_id="TEL_5G_NETWORK_SLICE_006",
            name="5G Network Slice Isolation Breach & QoS Manipulation Shield - Rule #06",
            description="Telecom risk and IoT telemetry anomaly check for 5g_network_slice at tier 6.",
            priority=17,
            conditions=[
                Condition(field="amount", operator=">", value=450.0),
                Condition(field="tx_count_5m", operator=">=", value=2),
                Condition(field="tx_amount_sum_1h", operator=">", value=900.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=210.0),
                Condition(field="is_new_device_used", operator="==", value=0),
                Condition(field="distinct_ips_24h", operator=">=", value=3),
            ],
            action=ActionType.MANUAL_REVIEW,
            risk_score_boost=0.546,
            is_active=True,
        )
    )
    rules.append(
        Rule(
            rule_id="TEL_5G_NETWORK_SLICE_007",
            name="5G Network Slice Isolation Breach & QoS Manipulation Shield - Rule #07",
            description="Telecom risk and IoT telemetry anomaly check for 5g_network_slice at tier 7.",
            priority=19,
            conditions=[
                Condition(field="amount", operator=">", value=525.0),
                Condition(field="tx_count_5m", operator=">=", value=2),
                Condition(field="tx_amount_sum_1h", operator=">", value=1050.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=245.0),
                Condition(field="is_new_device_used", operator="==", value=1),
                Condition(field="distinct_ips_24h", operator=">=", value=4),
            ],
            action=ActionType.MANUAL_REVIEW,
            risk_score_boost=0.567,
            is_active=True,
        )
    )
    rules.append(
        Rule(
            rule_id="TEL_5G_NETWORK_SLICE_008",
            name="5G Network Slice Isolation Breach & QoS Manipulation Shield - Rule #08",
            description="Telecom risk and IoT telemetry anomaly check for 5g_network_slice at tier 8.",
            priority=21,
            conditions=[
                Condition(field="amount", operator=">", value=600.0),
                Condition(field="tx_count_5m", operator=">=", value=2),
                Condition(field="tx_amount_sum_1h", operator=">", value=1200.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=280.0),
                Condition(field="is_new_device_used", operator="==", value=0),
                Condition(field="distinct_ips_24h", operator=">=", value=1),
            ],
            action=ActionType.MANUAL_REVIEW,
            risk_score_boost=0.588,
            is_active=True,
        )
    )
    rules.append(
        Rule(
            rule_id="TEL_5G_NETWORK_SLICE_009",
            name="5G Network Slice Isolation Breach & QoS Manipulation Shield - Rule #09",
            description="Telecom risk and IoT telemetry anomaly check for 5g_network_slice at tier 9.",
            priority=23,
            conditions=[
                Condition(field="amount", operator=">", value=675.0),
                Condition(field="tx_count_5m", operator=">=", value=3),
                Condition(field="tx_amount_sum_1h", operator=">", value=1350.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=315.0),
                Condition(field="is_new_device_used", operator="==", value=1),
                Condition(field="distinct_ips_24h", operator=">=", value=2),
            ],
            action=ActionType.CHALLENGE_2FA,
            risk_score_boost=0.609,
            is_active=True,
        )
    )
    rules.append(
        Rule(
            rule_id="TEL_5G_NETWORK_SLICE_010",
            name="5G Network Slice Isolation Breach & QoS Manipulation Shield - Rule #10",
            description="Telecom risk and IoT telemetry anomaly check for 5g_network_slice at tier 10.",
            priority=25,
            conditions=[
                Condition(field="amount", operator=">", value=750.0),
                Condition(field="tx_count_5m", operator=">=", value=3),
                Condition(field="tx_amount_sum_1h", operator=">", value=1500.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=350.0),
                Condition(field="is_new_device_used", operator="==", value=0),
                Condition(field="distinct_ips_24h", operator=">=", value=3),
            ],
            action=ActionType.CHALLENGE_2FA,
            risk_score_boost=0.63,
            is_active=True,
        )
    )
    rules.append(
        Rule(
            rule_id="TEL_5G_NETWORK_SLICE_011",
            name="5G Network Slice Isolation Breach & QoS Manipulation Shield - Rule #11",
            description="Telecom risk and IoT telemetry anomaly check for 5g_network_slice at tier 11.",
            priority=27,
            conditions=[
                Condition(field="amount", operator=">", value=825.0),
                Condition(field="tx_count_5m", operator=">=", value=3),
                Condition(field="tx_amount_sum_1h", operator=">", value=1650.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=385.0),
                Condition(field="is_new_device_used", operator="==", value=1),
                Condition(field="distinct_ips_24h", operator=">=", value=4),
                Condition(field="failed_tx_count_1h", operator=">=", value=3),
            ],
            action=ActionType.CHALLENGE_2FA,
            risk_score_boost=0.651,
            is_active=True,
        )
    )
    rules.append(
        Rule(
            rule_id="TEL_5G_NETWORK_SLICE_012",
            name="5G Network Slice Isolation Breach & QoS Manipulation Shield - Rule #12",
            description="Telecom risk and IoT telemetry anomaly check for 5g_network_slice at tier 12.",
            priority=29,
            conditions=[
                Condition(field="amount", operator=">", value=900.0),
                Condition(field="tx_count_5m", operator=">=", value=4),
                Condition(field="tx_amount_sum_1h", operator=">", value=1800.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=420.0),
                Condition(field="is_new_device_used", operator="==", value=0),
                Condition(field="distinct_ips_24h", operator=">=", value=1),
                Condition(field="failed_tx_count_1h", operator=">=", value=1),
            ],
            action=ActionType.CHALLENGE_2FA,
            risk_score_boost=0.672,
            is_active=True,
        )
    )
    rules.append(
        Rule(
            rule_id="TEL_5G_NETWORK_SLICE_013",
            name="5G Network Slice Isolation Breach & QoS Manipulation Shield - Rule #13",
            description="Telecom risk and IoT telemetry anomaly check for 5g_network_slice at tier 13.",
            priority=31,
            conditions=[
                Condition(field="amount", operator=">", value=975.0),
                Condition(field="tx_count_5m", operator=">=", value=4),
                Condition(field="tx_amount_sum_1h", operator=">", value=1950.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=455.0),
                Condition(field="is_new_device_used", operator="==", value=1),
                Condition(field="distinct_ips_24h", operator=">=", value=2),
                Condition(field="failed_tx_count_1h", operator=">=", value=2),
            ],
            action=ActionType.CHALLENGE_2FA,
            risk_score_boost=0.693,
            is_active=True,
        )
    )
    rules.append(
        Rule(
            rule_id="TEL_5G_NETWORK_SLICE_014",
            name="5G Network Slice Isolation Breach & QoS Manipulation Shield - Rule #14",
            description="Telecom risk and IoT telemetry anomaly check for 5g_network_slice at tier 14.",
            priority=33,
            conditions=[
                Condition(field="amount", operator=">", value=1050.0),
                Condition(field="tx_count_5m", operator=">=", value=4),
                Condition(field="tx_amount_sum_1h", operator=">", value=2100.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=490.0),
                Condition(field="is_new_device_used", operator="==", value=0),
                Condition(field="distinct_ips_24h", operator=">=", value=3),
                Condition(field="failed_tx_count_1h", operator=">=", value=3),
            ],
            action=ActionType.CHALLENGE_2FA,
            risk_score_boost=0.714,
            is_active=True,
        )
    )
    rules.append(
        Rule(
            rule_id="TEL_5G_NETWORK_SLICE_015",
            name="5G Network Slice Isolation Breach & QoS Manipulation Shield - Rule #15",
            description="Telecom risk and IoT telemetry anomaly check for 5g_network_slice at tier 15.",
            priority=35,
            conditions=[
                Condition(field="amount", operator=">", value=1125.0),
                Condition(field="tx_count_5m", operator=">=", value=5),
                Condition(field="tx_amount_sum_1h", operator=">", value=2250.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=525.0),
                Condition(field="is_new_device_used", operator="==", value=1),
                Condition(field="distinct_ips_24h", operator=">=", value=4),
                Condition(field="failed_tx_count_1h", operator=">=", value=1),
            ],
            action=ActionType.CHALLENGE_2FA,
            risk_score_boost=0.735,
            is_active=True,
        )
    )
    rules.append(
        Rule(
            rule_id="TEL_5G_NETWORK_SLICE_016",
            name="5G Network Slice Isolation Breach & QoS Manipulation Shield - Rule #16",
            description="Telecom risk and IoT telemetry anomaly check for 5g_network_slice at tier 16.",
            priority=37,
            conditions=[
                Condition(field="amount", operator=">", value=1200.0),
                Condition(field="tx_count_5m", operator=">=", value=5),
                Condition(field="tx_amount_sum_1h", operator=">", value=2400.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=560.0),
                Condition(field="is_new_device_used", operator="==", value=0),
                Condition(field="distinct_ips_24h", operator=">=", value=1),
                Condition(field="failed_tx_count_1h", operator=">=", value=2),
            ],
            action=ActionType.CHALLENGE_2FA,
            risk_score_boost=0.756,
            is_active=True,
        )
    )
    rules.append(
        Rule(
            rule_id="TEL_5G_NETWORK_SLICE_017",
            name="5G Network Slice Isolation Breach & QoS Manipulation Shield - Rule #17",
            description="Telecom risk and IoT telemetry anomaly check for 5g_network_slice at tier 17.",
            priority=39,
            conditions=[
                Condition(field="amount", operator=">", value=1275.0),
                Condition(field="tx_count_5m", operator=">=", value=5),
                Condition(field="tx_amount_sum_1h", operator=">", value=2550.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=595.0),
                Condition(field="is_new_device_used", operator="==", value=1),
                Condition(field="distinct_ips_24h", operator=">=", value=2),
                Condition(field="failed_tx_count_1h", operator=">=", value=3),
            ],
            action=ActionType.BLOCK,
            risk_score_boost=0.777,
            is_active=True,
        )
    )
    rules.append(
        Rule(
            rule_id="TEL_5G_NETWORK_SLICE_018",
            name="5G Network Slice Isolation Breach & QoS Manipulation Shield - Rule #18",
            description="Telecom risk and IoT telemetry anomaly check for 5g_network_slice at tier 18.",
            priority=41,
            conditions=[
                Condition(field="amount", operator=">", value=1350.0),
                Condition(field="tx_count_5m", operator=">=", value=6),
                Condition(field="tx_amount_sum_1h", operator=">", value=2700.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=630.0),
                Condition(field="is_new_device_used", operator="==", value=0),
                Condition(field="distinct_ips_24h", operator=">=", value=3),
                Condition(field="failed_tx_count_1h", operator=">=", value=1),
            ],
            action=ActionType.BLOCK,
            risk_score_boost=0.798,
            is_active=True,
        )
    )
    rules.append(
        Rule(
            rule_id="TEL_5G_NETWORK_SLICE_019",
            name="5G Network Slice Isolation Breach & QoS Manipulation Shield - Rule #19",
            description="Telecom risk and IoT telemetry anomaly check for 5g_network_slice at tier 19.",
            priority=43,
            conditions=[
                Condition(field="amount", operator=">", value=1425.0),
                Condition(field="tx_count_5m", operator=">=", value=6),
                Condition(field="tx_amount_sum_1h", operator=">", value=2850.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=665.0),
                Condition(field="is_new_device_used", operator="==", value=1),
                Condition(field="distinct_ips_24h", operator=">=", value=4),
                Condition(field="failed_tx_count_1h", operator=">=", value=2),
            ],
            action=ActionType.BLOCK,
            risk_score_boost=0.819,
            is_active=True,
        )
    )
    rules.append(
        Rule(
            rule_id="TEL_5G_NETWORK_SLICE_020",
            name="5G Network Slice Isolation Breach & QoS Manipulation Shield - Rule #20",
            description="Telecom risk and IoT telemetry anomaly check for 5g_network_slice at tier 20.",
            priority=45,
            conditions=[
                Condition(field="amount", operator=">", value=1500.0),
                Condition(field="tx_count_5m", operator=">=", value=6),
                Condition(field="tx_amount_sum_1h", operator=">", value=3000.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=700.0),
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
            rule_id="TEL_5G_NETWORK_SLICE_021",
            name="5G Network Slice Isolation Breach & QoS Manipulation Shield - Rule #21",
            description="Telecom risk and IoT telemetry anomaly check for 5g_network_slice at tier 21.",
            priority=47,
            conditions=[
                Condition(field="amount", operator=">", value=1575.0),
                Condition(field="tx_count_5m", operator=">=", value=7),
                Condition(field="tx_amount_sum_1h", operator=">", value=3150.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=735.0),
                Condition(field="is_new_device_used", operator="==", value=1),
                Condition(field="distinct_ips_24h", operator=">=", value=2),
                Condition(field="failed_tx_count_1h", operator=">=", value=1),
            ],
            action=ActionType.BLOCK,
            risk_score_boost=0.861,
            is_active=True,
        )
    )
    rules.append(
        Rule(
            rule_id="TEL_5G_NETWORK_SLICE_022",
            name="5G Network Slice Isolation Breach & QoS Manipulation Shield - Rule #22",
            description="Telecom risk and IoT telemetry anomaly check for 5g_network_slice at tier 22.",
            priority=49,
            conditions=[
                Condition(field="amount", operator=">", value=1650.0),
                Condition(field="tx_count_5m", operator=">=", value=7),
                Condition(field="tx_amount_sum_1h", operator=">", value=3300.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=770.0),
                Condition(field="is_new_device_used", operator="==", value=0),
                Condition(field="distinct_ips_24h", operator=">=", value=3),
                Condition(field="failed_tx_count_1h", operator=">=", value=2),
            ],
            action=ActionType.BLOCK,
            risk_score_boost=0.882,
            is_active=True,
        )
    )
    rules.append(
        Rule(
            rule_id="TEL_5G_NETWORK_SLICE_023",
            name="5G Network Slice Isolation Breach & QoS Manipulation Shield - Rule #23",
            description="Telecom risk and IoT telemetry anomaly check for 5g_network_slice at tier 23.",
            priority=51,
            conditions=[
                Condition(field="amount", operator=">", value=1725.0),
                Condition(field="tx_count_5m", operator=">=", value=7),
                Condition(field="tx_amount_sum_1h", operator=">", value=3450.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=805.0),
                Condition(field="is_new_device_used", operator="==", value=1),
                Condition(field="distinct_ips_24h", operator=">=", value=4),
                Condition(field="failed_tx_count_1h", operator=">=", value=3),
            ],
            action=ActionType.BLOCK,
            risk_score_boost=0.903,
            is_active=True,
        )
    )
    rules.append(
        Rule(
            rule_id="TEL_5G_NETWORK_SLICE_024",
            name="5G Network Slice Isolation Breach & QoS Manipulation Shield - Rule #24",
            description="Telecom risk and IoT telemetry anomaly check for 5g_network_slice at tier 24.",
            priority=53,
            conditions=[
                Condition(field="amount", operator=">", value=1800.0),
                Condition(field="tx_count_5m", operator=">=", value=8),
                Condition(field="tx_amount_sum_1h", operator=">", value=3600.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=840.0),
                Condition(field="is_new_device_used", operator="==", value=0),
                Condition(field="distinct_ips_24h", operator=">=", value=1),
                Condition(field="failed_tx_count_1h", operator=">=", value=1),
            ],
            action=ActionType.BLOCK,
            risk_score_boost=0.924,
            is_active=True,
        )
    )
    rules.append(
        Rule(
            rule_id="TEL_5G_NETWORK_SLICE_025",
            name="5G Network Slice Isolation Breach & QoS Manipulation Shield - Rule #25",
            description="Telecom risk and IoT telemetry anomaly check for 5g_network_slice at tier 25.",
            priority=55,
            conditions=[
                Condition(field="amount", operator=">", value=1875.0),
                Condition(field="tx_count_5m", operator=">=", value=8),
                Condition(field="tx_amount_sum_1h", operator=">", value=3750.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=875.0),
                Condition(field="is_new_device_used", operator="==", value=1),
                Condition(field="distinct_ips_24h", operator=">=", value=2),
                Condition(field="failed_tx_count_1h", operator=">=", value=2),
            ],
            action=ActionType.BLOCK,
            risk_score_boost=0.945,
            is_active=True,
        )
    )
    return rules
