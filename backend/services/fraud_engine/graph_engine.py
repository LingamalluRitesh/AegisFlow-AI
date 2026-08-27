"""
Graph-Based Fraud Ring & Entity Linkage Engine
Analyzes bipartite and heterogeneous transaction graphs to detect coordinated fraud rings and mule networks.
"""

from typing import Dict, Any, List, Set, Optional
from collections import defaultdict
import threading
from backend.core.logging import get_logger

logger = get_logger("fraud.graph_engine")


class FraudGraphEngine:
    def __init__(self):
        self._user_to_devices: Dict[str, Set[str]] = defaultdict(set)
        self._device_to_users: Dict[str, Set[str]] = defaultdict(set)
        self._user_to_ips: Dict[str, Set[str]] = defaultdict(set)
        self._ip_to_users: Dict[str, Set[str]] = defaultdict(set)
        self._user_to_cards: Dict[str, Set[str]] = defaultdict(set)
        self._card_to_users: Dict[str, Set[str]] = defaultdict(set)
        self._lock = threading.Lock()

    def record_edge(self, user_id: str, device_id: Optional[str], ip_address: Optional[str], card_id: Optional[str]) -> None:
        with self._lock:
            if device_id:
                self._user_to_devices[user_id].add(device_id)
                self._device_to_users[device_id].add(user_id)
            if ip_address:
                self._user_to_ips[user_id].add(ip_address)
                self._ip_to_users[ip_address].add(user_id)
            if card_id:
                self._user_to_cards[user_id].add(card_id)
                self._card_to_users[card_id].add(user_id)

    def calculate_entity_risk_multiplier(self, user_id: str, device_id: Optional[str], ip_address: Optional[str]) -> float:
        with self._lock:
            multiplier = 1.0

            if device_id and device_id in self._device_to_users:
                shared_users = len(self._device_to_users[device_id])
                if shared_users > 5:
                    multiplier += 1.2
                elif shared_users > 2:
                    multiplier += 0.5

            if ip_address and ip_address in self._ip_to_users:
                shared_ip_users = len(self._ip_to_users[ip_address])
                if shared_ip_users > 10:
                    multiplier += 0.4

            return min(3.0, multiplier)
