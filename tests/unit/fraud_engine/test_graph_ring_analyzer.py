"""
Unit tests for Tarjan SCC graph mule ring analyzer.
"""

from backend.services.fraud_engine.graph_ring_analyzer import GraphRingAnalyzer


def test_circular_mule_ring_detection():
    analyzer = GraphRingAnalyzer()
    # Create circular ring: A -> B -> C -> A
    analyzer.add_transfer_edge("acct_A", "acct_B")
    analyzer.add_transfer_edge("acct_B", "acct_C")
    analyzer.add_transfer_edge("acct_C", "acct_A")

    # Add innocent linear transfers: D -> E
    analyzer.add_transfer_edge("acct_D", "acct_E")

    rings = analyzer.find_strongly_connected_rings(min_ring_size=3)
    assert len(rings) == 1
    detected_nodes = set(rings[0])
    assert detected_nodes == {"acct_A", "acct_B", "acct_C"}


def test_no_cycle_graph():
    analyzer = GraphRingAnalyzer()
    analyzer.add_transfer_edge("acct_1", "acct_2")
    analyzer.add_transfer_edge("acct_2", "acct_3")
    analyzer.add_transfer_edge("acct_3", "acct_4")

    rings = analyzer.find_strongly_connected_rings(min_ring_size=2)
    assert len(rings) == 0
