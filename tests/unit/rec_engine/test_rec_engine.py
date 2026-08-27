import pytest
from backend.core.types import RecommendationRequest
from backend.services.rec_engine.vector_index import HNSWVectorIndex
from backend.services.rec_engine.contextual_bandit import LinUCBBandit
from backend.services.rec_engine.reranker import MaximalMarginalRelevanceReranker
from backend.services.rec_engine.service import rec_service


def test_vector_ann_indexing():
    idx = HNSWVectorIndex(dimension=4)
    idx.add_item("item_1", [1.0, 0.0, 0.0, 0.0], {"title": "Item 1"})
    idx.add_item("item_2", [0.0, 1.0, 0.0, 0.0], {"title": "Item 2"})
    results = idx.search_nearest([1.0, 0.0, 0.0, 0.0], top_k=1)
    assert len(results) == 1
    assert results[0][0] == "item_1"


def test_bandit_arm_updates():
    bandit = LinUCBBandit(dimension=4)
    bonus = bandit.get_exploration_bonus("electronics", [0.1, 0.2, 0.3, 0.4])
    assert bonus > 0.0
    bandit.update_arm("electronics", [0.1, 0.2, 0.3, 0.4], 1.0)


def test_mmr_diversity_reranker():
    reranker = MaximalMarginalRelevanceReranker(diversity_lambda=0.5)
    candidates = [
        {"item_id": "1", "score": 0.9, "category": "electronics"},
        {"item_id": "2", "score": 0.88, "category": "electronics"},
        {"item_id": "3", "score": 0.85, "category": "books"},
    ]
    reranked = reranker.rerank(candidates, top_k=2)
    assert len(reranked) == 2
    assert reranked[0]["item_id"] == "1"
    assert reranked[1]["category"] == "books"


@pytest.mark.asyncio
async def test_end_to_end_rec_service():
    req = RecommendationRequest(user_id="usr_007", candidate_count=4)
    res = await rec_service.get_recommendations(req)
    assert res.user_id == "usr_007"
    assert len(res.recommendations) > 0
