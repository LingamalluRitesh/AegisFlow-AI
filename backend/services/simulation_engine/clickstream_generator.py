"""
E-Commerce Clickstream Event Simulator
"""

import random
import time
from typing import Dict, Any


class ClickstreamGenerator:
    def __init__(self):
        self.event_types = ["item_view", "item_view", "item_view", "add_to_cart", "purchase"]
        self.items = [f"ITEM_10{i}" for i in range(1, 10)]

    def generate_click_event(self, user_id: str) -> Dict[str, Any]:
        return {
            "event_id": f"evt_{random.randint(100000, 999999)}",
            "user_id": user_id,
            "item_id": random.choice(self.items),
            "event_type": random.choice(self.event_types),
            "timestamp": time.time(),
        }
