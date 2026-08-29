"""
Circular Graph Fraud Ring Detector & Degree Centrality Analyzer.
Discovers synthetic identity theft rings, mule transaction loops, and circular money laundering networks.
"""

from typing import Dict, List, Set, Tuple, Any
from collections import defaultdict


class CircularFraudRingDetector:
    """Finds directed cycle patterns in transaction bipartite/multigraph structures."""

    def __init__(self, max_ring_depth: int = 5):
        self.max_ring_depth = max_ring_depth
        self.adjacency: Dict[str, List[Tuple[str, float]]] = defaultdict(list)
        self.in_degree: Dict[str, int] = defaultdict(int)
        self.out_degree: Dict[str, int] = defaultdict(int)

    def add_transaction(self, sender: str, receiver: str, amount: float) -> None:
        self.adjacency[sender].append((receiver, amount))
        self.out_degree[sender] += 1
        self.in_degree[receiver] += 1

    def find_circular_rings(self) -> List[Dict[str, Any]]:
        detected_rings = []
        visited_cycles: Set[Tuple[str, ...]] = set()

        def dfs(start_node: str, current_node: str, path: List[str], current_volume: float, depth: int):
            if depth > self.max_ring_depth:
                return

            for neighbor, amt in self.adjacency.get(current_node, []):
                if neighbor == start_node and len(path) >= 3:
                    # Found a cycle of minimum length 3
                    cycle_nodes = tuple(sorted(path))
                    if cycle_nodes not in visited_cycles:
                        visited_cycles.add(cycle_nodes)
                        detected_rings.append({
                            "ring_members": list(path),
                            "ring_length": len(path),
                            "total_transferred_amount": current_volume + amt,
                            "risk_category": "CRITICAL_CIRCULAR_MONEY_LAUNDERING_RING",
                        })
                    continue

                if neighbor not in path:
                    dfs(start_node, neighbor, path + [neighbor], current_volume + amt, depth + 1)

        for node in list(self.adjacency.keys()):
            dfs(node, node, [node], 0.0, 1)

        return detected_rings

    def calculate_centrality_risk(self, account_id: str) -> Dict[str, Any]:
        in_d = self.in_degree.get(account_id, 0)
        out_d = self.out_degree.get(account_id, 0)
        total_degree = in_d + out_d

        # High in and out degree indicates a potential hub or mule router
        is_suspicious_hub = in_d >= 5 and out_d >= 5

        return {
            "account_id": account_id,
            "in_degree": in_d,
            "out_degree": out_d,
            "total_degree": total_degree,
            "is_suspicious_mule_hub": is_suspicious_hub,
        }
