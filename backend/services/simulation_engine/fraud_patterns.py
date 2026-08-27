"""
Synthetic Fraud Pattern Injector
Simulates specific financial crime behaviors: velocity bursts, card testing, credential stuffing, geo leaps.
"""

import random
import uuid
import time
from typing import Dict, Any, List


class FraudPatternInjector:
    @staticmethod
    def generate_velocity_burst(user_id: str, count: int = 8) -> List[Dict[str, Any]]:
        events = []
        base_time = time.time()
        for i in range(count):
            events.append({
                "transaction_id": f"tx_burst_{str(uuid.uuid4())[:8]}",
                "user_id": user_id,
                "source_account_id": f"acct_{user_id}",
                "target_account_id": f"acct_mule_{random.randint(100, 999)}",
                "amount": round(random.uniform(200.0, 950.0), 2),
                "timestamp_unix": base_time + (i * 15),
                "device_id": "dev_hacked_001",
                "ip_address": "198.51.100.44",
                "channel": "mobile_app",
            })
        return events

    @staticmethod
    def generate_impossible_travel(user_id: str) -> List[Dict[str, Any]]:
        return [
            {
                "transaction_id": f"tx_geo1_{str(uuid.uuid4())[:8]}",
                "user_id": user_id,
                "source_account_id": f"acct_{user_id}",
                "target_account_id": "acct_ny_merchant",
                "amount": 45.0,
                "timestamp_unix": time.time() - 600,
                "latitude": 40.7128,
                "longitude": -74.0060,
                "device_id": "dev_user_phone",
                "ip_address": "72.229.28.185",
            },
            {
                "transaction_id": f"tx_geo2_{str(uuid.uuid4())[:8]}",
                "user_id": user_id,
                "source_account_id": f"acct_{user_id}",
                "target_account_id": "acct_tokyo_atm",
                "amount": 950.0,
                "timestamp_unix": time.time(),
                "latitude": 35.6762,
                "longitude": 139.6503,
                "device_id": "dev_unknown_terminal",
                "ip_address": "133.242.0.1",
            },
        ]
