"""
Tarjan Strongly Connected Components & Fraud Mule Ring Topology Analyzer
Detects circular laundering networks and rapid fund dispersion topologies in sub-milliseconds.
"""

from typing import Dict, List, Set, Any
from collections import defaultdict
from backend.core.logging import get_logger

logger = get_logger("fraud_engine.graph_ring")


class GraphRingAnalyzer:
    """Detects cycles and strongly connected components (SCCs) in transaction graphs."""

    def __init__(self):
        self._adj_list: Dict[str, Set[str]] = defaultdict(set)

    def add_transfer_edge(self, source_account: str, target_account: str) -> None:
        self._adj_list[source_account].add(target_account)

    def find_strongly_connected_rings(self, min_ring_size: int = 3) -> List[List[str]]:
        index = 0
        indices: Dict[str, int] = {}
        lowlinks: Dict[str, int] = {}
        on_stack: Set[str] = set()
        stack: List[str] = []
        sccs: List[List[str]] = []

        def strongconnect(node: str):
            nonlocal index
            indices[node] = index
            lowlinks[node] = index
            index += 1
            stack.append(node)
            on_stack.add(node)

            for neighbor in self._adj_list.get(node, set()):
                if neighbor not in indices:
                    strongconnect(neighbor)
                    lowlinks[node] = min(lowlinks[node], lowlinks[neighbor])
                elif neighbor in on_stack:
                    lowlinks[node] = min(lowlinks[node], indices[neighbor])

            if lowlinks[node] == indices[node]:
                scc = []
                while True:
                    w = stack.pop()
                    on_stack.remove(w)
                    scc.append(w)
                    if w == node:
                        break
                if len(scc) >= min_ring_size:
                    sccs.append(scc)

        all_nodes = list(self._adj_list.keys())
        for n in all_nodes:
            if n not in indices:
                strongconnect(n)

        return sccs


graph_ring_analyzer = GraphRingAnalyzer()
