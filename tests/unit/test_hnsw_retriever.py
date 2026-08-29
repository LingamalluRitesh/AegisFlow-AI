import pytest
from backend.services.rec_engine.hnsw_retriever import HNSWVectorIndex


def test_hnsw_vector_similarity_search():
    index = HNSWVectorIndex(dimension=4)

    # Insert items
    index.insert_vector("item_electronics_1", [1.0, 0.0, 0.0, 0.0], {"category": "electronics"})
    index.insert_vector("item_electronics_2", [0.9, 0.1, 0.0, 0.0], {"category": "electronics"})
    index.insert_vector("item_fashion_1", [0.0, 0.0, 1.0, 0.0], {"category": "fashion"})

    # Query with electronics embedding
    query = [0.95, 0.05, 0.0, 0.0]
    results = index.search_knn(query, top_k=2)

    assert len(results) == 2
    assert results[0]["item_id"] == "item_electronics_1"
    assert results[0]["similarity_score"] > 0.98
    assert results[1]["item_id"] == "item_electronics_2"
