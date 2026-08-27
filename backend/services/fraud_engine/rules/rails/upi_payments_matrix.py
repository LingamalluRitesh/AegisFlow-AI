"""
AegisGuard Payment Rail Defense Matrix: UPI (Unified Payments Interface) Real-Time Risk Rules
Rail Specification: upi_payments
"""

from typing import List, Dict, Any
from backend.services.fraud_engine.rule_engine import Rule, Condition
from backend.core.types import ActionType

def get_upi_payments_rule_matrix() -> List[Rule]:
    """Returns institutional rule suite for UPI (Unified Payments Interface) Real-Time Risk Rules."""
    rules = []
    # --- Rule Definition RAIL_UPI_PAYMENTS_001 ---
    rules.append(
        Rule(
            rule_id="RAIL_UPI_PAYMENTS_001",
            name="UPI (Unified Payments Interface) Real-Time Risk Rules Rule #01",
            description="Real-time compliance and risk evaluation for upi_payments protocol specification tier 1.",
            priority=7,
            conditions=[
                Condition(field="amount", operator=">", value=250.0),
                Condition(field="tx_count_5m", operator=">=", value=1),
                Condition(field="tx_amount_sum_1h", operator=">", value=500.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=40.0),
                Condition(field="distinct_devices_24h", operator=">=", value=2),
                Condition(field="is_new_device_used", operator="==", value=1),
            ],
            action=ActionType.MANUAL_REVIEW,
            risk_score_boost=0.475,
            is_active=True,
        )
    )
    # --- Rule Definition RAIL_UPI_PAYMENTS_002 ---
    rules.append(
        Rule(
            rule_id="RAIL_UPI_PAYMENTS_002",
            name="UPI (Unified Payments Interface) Real-Time Risk Rules Rule #02",
            description="Real-time compliance and risk evaluation for upi_payments protocol specification tier 2.",
            priority=9,
            conditions=[
                Condition(field="amount", operator=">", value=500.0),
                Condition(field="tx_count_5m", operator=">=", value=1),
                Condition(field="tx_amount_sum_1h", operator=">", value=1000.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=80.0),
                Condition(field="distinct_devices_24h", operator=">=", value=3),
                Condition(field="is_new_device_used", operator="==", value=0),
            ],
            action=ActionType.MANUAL_REVIEW,
            risk_score_boost=0.5,
            is_active=True,
        )
    )
    # --- Rule Definition RAIL_UPI_PAYMENTS_003 ---
    rules.append(
        Rule(
            rule_id="RAIL_UPI_PAYMENTS_003",
            name="UPI (Unified Payments Interface) Real-Time Risk Rules Rule #03",
            description="Real-time compliance and risk evaluation for upi_payments protocol specification tier 3.",
            priority=11,
            conditions=[
                Condition(field="amount", operator=">", value=750.0),
                Condition(field="tx_count_5m", operator=">=", value=1),
                Condition(field="tx_amount_sum_1h", operator=">", value=1500.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=120.0),
                Condition(field="distinct_devices_24h", operator=">=", value=1),
                Condition(field="is_new_device_used", operator="==", value=1),
            ],
            action=ActionType.MANUAL_REVIEW,
            risk_score_boost=0.525,
            is_active=True,
        )
    )
    # --- Rule Definition RAIL_UPI_PAYMENTS_004 ---
    rules.append(
        Rule(
            rule_id="RAIL_UPI_PAYMENTS_004",
            name="UPI (Unified Payments Interface) Real-Time Risk Rules Rule #04",
            description="Real-time compliance and risk evaluation for upi_payments protocol specification tier 4.",
            priority=13,
            conditions=[
                Condition(field="amount", operator=">", value=1000.0),
                Condition(field="tx_count_5m", operator=">=", value=1),
                Condition(field="tx_amount_sum_1h", operator=">", value=2000.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=160.0),
                Condition(field="distinct_devices_24h", operator=">=", value=2),
                Condition(field="is_new_device_used", operator="==", value=0),
            ],
            action=ActionType.MANUAL_REVIEW,
            risk_score_boost=0.55,
            is_active=True,
        )
    )
    # --- Rule Definition RAIL_UPI_PAYMENTS_005 ---
    rules.append(
        Rule(
            rule_id="RAIL_UPI_PAYMENTS_005",
            name="UPI (Unified Payments Interface) Real-Time Risk Rules Rule #05",
            description="Real-time compliance and risk evaluation for upi_payments protocol specification tier 5.",
            priority=15,
            conditions=[
                Condition(field="amount", operator=">", value=1250.0),
                Condition(field="tx_count_5m", operator=">=", value=1),
                Condition(field="tx_amount_sum_1h", operator=">", value=2500.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=200.0),
                Condition(field="distinct_devices_24h", operator=">=", value=3),
                Condition(field="is_new_device_used", operator="==", value=1),
            ],
            action=ActionType.MANUAL_REVIEW,
            risk_score_boost=0.575,
            is_active=True,
        )
    )
    # --- Rule Definition RAIL_UPI_PAYMENTS_006 ---
    rules.append(
        Rule(
            rule_id="RAIL_UPI_PAYMENTS_006",
            name="UPI (Unified Payments Interface) Real-Time Risk Rules Rule #06",
            description="Real-time compliance and risk evaluation for upi_payments protocol specification tier 6.",
            priority=17,
            conditions=[
                Condition(field="amount", operator=">", value=1500.0),
                Condition(field="tx_count_5m", operator=">=", value=2),
                Condition(field="tx_amount_sum_1h", operator=">", value=3000.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=240.0),
                Condition(field="distinct_devices_24h", operator=">=", value=1),
                Condition(field="is_new_device_used", operator="==", value=0),
            ],
            action=ActionType.MANUAL_REVIEW,
            risk_score_boost=0.6,
            is_active=True,
        )
    )
    # --- Rule Definition RAIL_UPI_PAYMENTS_007 ---
    rules.append(
        Rule(
            rule_id="RAIL_UPI_PAYMENTS_007",
            name="UPI (Unified Payments Interface) Real-Time Risk Rules Rule #07",
            description="Real-time compliance and risk evaluation for upi_payments protocol specification tier 7.",
            priority=19,
            conditions=[
                Condition(field="amount", operator=">", value=1750.0),
                Condition(field="tx_count_5m", operator=">=", value=2),
                Condition(field="tx_amount_sum_1h", operator=">", value=3500.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=280.0),
                Condition(field="distinct_devices_24h", operator=">=", value=2),
                Condition(field="is_new_device_used", operator="==", value=1),
            ],
            action=ActionType.CHALLENGE_2FA,
            risk_score_boost=0.625,
            is_active=True,
        )
    )
    # --- Rule Definition RAIL_UPI_PAYMENTS_008 ---
    rules.append(
        Rule(
            rule_id="RAIL_UPI_PAYMENTS_008",
            name="UPI (Unified Payments Interface) Real-Time Risk Rules Rule #08",
            description="Real-time compliance and risk evaluation for upi_payments protocol specification tier 8.",
            priority=21,
            conditions=[
                Condition(field="amount", operator=">", value=2000.0),
                Condition(field="tx_count_5m", operator=">=", value=2),
                Condition(field="tx_amount_sum_1h", operator=">", value=4000.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=320.0),
                Condition(field="distinct_devices_24h", operator=">=", value=3),
                Condition(field="is_new_device_used", operator="==", value=0),
            ],
            action=ActionType.CHALLENGE_2FA,
            risk_score_boost=0.65,
            is_active=True,
        )
    )
    # --- Rule Definition RAIL_UPI_PAYMENTS_009 ---
    rules.append(
        Rule(
            rule_id="RAIL_UPI_PAYMENTS_009",
            name="UPI (Unified Payments Interface) Real-Time Risk Rules Rule #09",
            description="Real-time compliance and risk evaluation for upi_payments protocol specification tier 9.",
            priority=23,
            conditions=[
                Condition(field="amount", operator=">", value=2250.0),
                Condition(field="tx_count_5m", operator=">=", value=3),
                Condition(field="tx_amount_sum_1h", operator=">", value=4500.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=360.0),
                Condition(field="distinct_devices_24h", operator=">=", value=1),
                Condition(field="is_new_device_used", operator="==", value=1),
            ],
            action=ActionType.CHALLENGE_2FA,
            risk_score_boost=0.675,
            is_active=True,
        )
    )
    # --- Rule Definition RAIL_UPI_PAYMENTS_010 ---
    rules.append(
        Rule(
            rule_id="RAIL_UPI_PAYMENTS_010",
            name="UPI (Unified Payments Interface) Real-Time Risk Rules Rule #10",
            description="Real-time compliance and risk evaluation for upi_payments protocol specification tier 10.",
            priority=25,
            conditions=[
                Condition(field="amount", operator=">", value=2500.0),
                Condition(field="tx_count_5m", operator=">=", value=3),
                Condition(field="tx_amount_sum_1h", operator=">", value=5000.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=400.0),
                Condition(field="distinct_devices_24h", operator=">=", value=2),
                Condition(field="is_new_device_used", operator="==", value=0),
            ],
            action=ActionType.CHALLENGE_2FA,
            risk_score_boost=0.7,
            is_active=True,
        )
    )
    # --- Rule Definition RAIL_UPI_PAYMENTS_011 ---
    rules.append(
        Rule(
            rule_id="RAIL_UPI_PAYMENTS_011",
            name="UPI (Unified Payments Interface) Real-Time Risk Rules Rule #11",
            description="Real-time compliance and risk evaluation for upi_payments protocol specification tier 11.",
            priority=27,
            conditions=[
                Condition(field="amount", operator=">", value=2750.0),
                Condition(field="tx_count_5m", operator=">=", value=3),
                Condition(field="tx_amount_sum_1h", operator=">", value=5500.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=440.0),
                Condition(field="distinct_devices_24h", operator=">=", value=3),
                Condition(field="is_new_device_used", operator="==", value=1),
            ],
            action=ActionType.CHALLENGE_2FA,
            risk_score_boost=0.725,
            is_active=True,
        )
    )
    # --- Rule Definition RAIL_UPI_PAYMENTS_012 ---
    rules.append(
        Rule(
            rule_id="RAIL_UPI_PAYMENTS_012",
            name="UPI (Unified Payments Interface) Real-Time Risk Rules Rule #12",
            description="Real-time compliance and risk evaluation for upi_payments protocol specification tier 12.",
            priority=29,
            conditions=[
                Condition(field="amount", operator=">", value=3000.0),
                Condition(field="tx_count_5m", operator=">=", value=4),
                Condition(field="tx_amount_sum_1h", operator=">", value=6000.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=480.0),
                Condition(field="distinct_devices_24h", operator=">=", value=1),
                Condition(field="is_new_device_used", operator="==", value=0),
            ],
            action=ActionType.CHALLENGE_2FA,
            risk_score_boost=0.75,
            is_active=True,
        )
    )
    # --- Rule Definition RAIL_UPI_PAYMENTS_013 ---
    rules.append(
        Rule(
            rule_id="RAIL_UPI_PAYMENTS_013",
            name="UPI (Unified Payments Interface) Real-Time Risk Rules Rule #13",
            description="Real-time compliance and risk evaluation for upi_payments protocol specification tier 13.",
            priority=31,
            conditions=[
                Condition(field="amount", operator=">", value=3250.0),
                Condition(field="tx_count_5m", operator=">=", value=4),
                Condition(field="tx_amount_sum_1h", operator=">", value=6500.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=520.0),
                Condition(field="distinct_devices_24h", operator=">=", value=2),
                Condition(field="is_new_device_used", operator="==", value=1),
            ],
            action=ActionType.BLOCK,
            risk_score_boost=0.775,
            is_active=True,
        )
    )
    # --- Rule Definition RAIL_UPI_PAYMENTS_014 ---
    rules.append(
        Rule(
            rule_id="RAIL_UPI_PAYMENTS_014",
            name="UPI (Unified Payments Interface) Real-Time Risk Rules Rule #14",
            description="Real-time compliance and risk evaluation for upi_payments protocol specification tier 14.",
            priority=33,
            conditions=[
                Condition(field="amount", operator=">", value=3500.0),
                Condition(field="tx_count_5m", operator=">=", value=4),
                Condition(field="tx_amount_sum_1h", operator=">", value=7000.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=560.0),
                Condition(field="distinct_devices_24h", operator=">=", value=3),
                Condition(field="is_new_device_used", operator="==", value=0),
            ],
            action=ActionType.BLOCK,
            risk_score_boost=0.8,
            is_active=True,
        )
    )
    # --- Rule Definition RAIL_UPI_PAYMENTS_015 ---
    rules.append(
        Rule(
            rule_id="RAIL_UPI_PAYMENTS_015",
            name="UPI (Unified Payments Interface) Real-Time Risk Rules Rule #15",
            description="Real-time compliance and risk evaluation for upi_payments protocol specification tier 15.",
            priority=35,
            conditions=[
                Condition(field="amount", operator=">", value=3750.0),
                Condition(field="tx_count_5m", operator=">=", value=5),
                Condition(field="tx_amount_sum_1h", operator=">", value=7500.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=600.0),
                Condition(field="distinct_devices_24h", operator=">=", value=1),
                Condition(field="is_new_device_used", operator="==", value=1),
            ],
            action=ActionType.BLOCK,
            risk_score_boost=0.825,
            is_active=True,
        )
    )
    # --- Rule Definition RAIL_UPI_PAYMENTS_016 ---
    rules.append(
        Rule(
            rule_id="RAIL_UPI_PAYMENTS_016",
            name="UPI (Unified Payments Interface) Real-Time Risk Rules Rule #16",
            description="Real-time compliance and risk evaluation for upi_payments protocol specification tier 16.",
            priority=37,
            conditions=[
                Condition(field="amount", operator=">", value=4000.0),
                Condition(field="tx_count_5m", operator=">=", value=5),
                Condition(field="tx_amount_sum_1h", operator=">", value=8000.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=640.0),
                Condition(field="distinct_devices_24h", operator=">=", value=2),
                Condition(field="is_new_device_used", operator="==", value=0),
            ],
            action=ActionType.BLOCK,
            risk_score_boost=0.85,
            is_active=True,
        )
    )
    # --- Rule Definition RAIL_UPI_PAYMENTS_017 ---
    rules.append(
        Rule(
            rule_id="RAIL_UPI_PAYMENTS_017",
            name="UPI (Unified Payments Interface) Real-Time Risk Rules Rule #17",
            description="Real-time compliance and risk evaluation for upi_payments protocol specification tier 17.",
            priority=39,
            conditions=[
                Condition(field="amount", operator=">", value=4250.0),
                Condition(field="tx_count_5m", operator=">=", value=5),
                Condition(field="tx_amount_sum_1h", operator=">", value=8500.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=680.0),
                Condition(field="distinct_devices_24h", operator=">=", value=3),
                Condition(field="is_new_device_used", operator="==", value=1),
            ],
            action=ActionType.BLOCK,
            risk_score_boost=0.875,
            is_active=True,
        )
    )
    # --- Rule Definition RAIL_UPI_PAYMENTS_018 ---
    rules.append(
        Rule(
            rule_id="RAIL_UPI_PAYMENTS_018",
            name="UPI (Unified Payments Interface) Real-Time Risk Rules Rule #18",
            description="Real-time compliance and risk evaluation for upi_payments protocol specification tier 18.",
            priority=41,
            conditions=[
                Condition(field="amount", operator=">", value=4500.0),
                Condition(field="tx_count_5m", operator=">=", value=6),
                Condition(field="tx_amount_sum_1h", operator=">", value=9000.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=720.0),
                Condition(field="distinct_devices_24h", operator=">=", value=1),
                Condition(field="is_new_device_used", operator="==", value=0),
            ],
            action=ActionType.BLOCK,
            risk_score_boost=0.9,
            is_active=True,
        )
    )
    # --- Rule Definition RAIL_UPI_PAYMENTS_019 ---
    rules.append(
        Rule(
            rule_id="RAIL_UPI_PAYMENTS_019",
            name="UPI (Unified Payments Interface) Real-Time Risk Rules Rule #19",
            description="Real-time compliance and risk evaluation for upi_payments protocol specification tier 19.",
            priority=43,
            conditions=[
                Condition(field="amount", operator=">", value=4750.0),
                Condition(field="tx_count_5m", operator=">=", value=6),
                Condition(field="tx_amount_sum_1h", operator=">", value=9500.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=760.0),
                Condition(field="distinct_devices_24h", operator=">=", value=2),
                Condition(field="is_new_device_used", operator="==", value=1),
            ],
            action=ActionType.BLOCK,
            risk_score_boost=0.925,
            is_active=True,
        )
    )
    # --- Rule Definition RAIL_UPI_PAYMENTS_020 ---
    rules.append(
        Rule(
            rule_id="RAIL_UPI_PAYMENTS_020",
            name="UPI (Unified Payments Interface) Real-Time Risk Rules Rule #20",
            description="Real-time compliance and risk evaluation for upi_payments protocol specification tier 20.",
            priority=45,
            conditions=[
                Condition(field="amount", operator=">", value=5000.0),
                Condition(field="tx_count_5m", operator=">=", value=6),
                Condition(field="tx_amount_sum_1h", operator=">", value=10000.0),
                Condition(field="max_geo_leap_speed_kmh", operator=">", value=800.0),
                Condition(field="distinct_devices_24h", operator=">=", value=3),
                Condition(field="is_new_device_used", operator="==", value=0),
            ],
            action=ActionType.BLOCK,
            risk_score_boost=0.95,
            is_active=True,
        )
    )
    return rules
