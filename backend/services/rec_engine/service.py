"""
PulseRec Recommendation Service Facade
Orchestrates candidate retrieval, dual-tower encoding, DLRM ranking, bandit exploration, and MMR reranking.
"""

import time
from datetime import datetime, timezone
from backend.core.types import RecommendationRequest, RecommendationResponse, RecommendedItem
from backend.core.logging import get_logger
from backend.core.telemetry import telemetry_manager
from backend.services.feature_store.client import feature_store_client
from backend.services.rec_engine.vector_index import HNSWVectorIndex
from backend.services.rec_engine.dual_tower import DualTowerEmbeddingGenerator
from backend.services.rec_engine.dlrm_ranker import DLRMMultiTaskRanker
from backend.services.rec_engine.contextual_bandit import LinUCBBandit
from backend.services.rec_engine.reranker import MaximalMarginalRelevanceReranker

logger = get_logger("rec.service")


class PulseRecService:
    def __init__(self):
        self.vector_index = HNSWVectorIndex(dimension=128)
        self.dual_tower = DualTowerEmbeddingGenerator(embedding_dim=128)
        self.ranker = DLRMMultiTaskRanker()
        self.bandit = LinUCBBandit()
        self.reranker = MaximalMarginalRelevanceReranker()
        self._seed_sample_catalog()

    def _seed_sample_catalog(self):
        sample_items = [
            ("ITEM_101", "Ultra-Slim 4K OLED Gaming Monitor", "electronics", 799.0),
            ("ITEM_102", "Noise-Cancelling Wireless Headphones Pro", "electronics", 349.0),
            ("ITEM_103", "Ergonomic Mesh Task Office Chair", "furniture", 280.0),
            ("ITEM_104", "Stainless Steel Espresso Machine", "kitchen", 450.0),
            ("ITEM_105", "Carbon-Fiber Road Bicycle 21-Speed", "sports", 1200.0),
            ("ITEM_106", "Smart Home Voice Assistant Hub", "electronics", 99.0),
            ("ITEM_107", "Waterproof Trail Running Shoes", "sports", 140.0),
            ("ITEM_108", "Mechanical RGB Gaming Keyboard", "electronics", 129.0),
            ("ITEM_109", "Chef Damascus Steel Knife Set", "kitchen", 220.0),
            ("ITEM_110", "Minimalist Solid Oak Standing Desk", "furniture", 599.0),
        ]
        for i_id, title, cat, price in sample_items:
            emb = self.dual_tower.encode_item(i_id, cat, price)
            self.vector_index.add_item(i_id, emb, {"title": title, "category": cat, "price": price})

    async def get_recommendations(self, request: RecommendationRequest) -> RecommendationResponse:
        start_time = time.perf_counter()

        hydrated_feats = await feature_store_client.get_online_features(
            feature_view_name="user_rec_engagement_features",
            entity_keys=[request.user_id],
        )
        user_feats = hydrated_feats[0] if hydrated_feats else {}

        query_vec = self.dual_tower.encode_user(request.user_id, {**user_feats, **request.contextual_features})
        candidates = self.vector_index.search_nearest(query_vec, top_k=request.candidate_count * 2)

        ranked_items = []
        for item_id, sim_score, meta in candidates:
            p_ctr, p_cvr, base_rank = self.ranker.predict_ctr_cvr(user_feats, meta, sim_score)
            cat = meta.get("category", "general")
            bonus = self.bandit.get_exploration_bonus(cat, query_vec)
            final_score = base_rank + bonus

            ranked_items.append({
                "item_id": item_id,
                "title": meta.get("title", f"Product {item_id}"),
                "category": cat,
                "score": float(final_score),
                "predicted_ctr": float(p_ctr),
                "predicted_cvr": float(p_cvr),
                "exploration_bonus": float(bonus),
                "metadata": meta,
            })

        final_list = self.reranker.rerank(ranked_items, top_k=request.candidate_count)
        latency_ms = (time.perf_counter() - start_time) * 1000.0
        telemetry_manager.get_counter("aegis_recommendations_served_total").inc()

        items_dto = [RecommendedItem(**it) for it in final_list]
        return RecommendationResponse(
            user_id=request.user_id,
            recommendations=items_dto,
            model_version="pulserec-two-stage-dlrm-v2.4",
            pipeline_latency_ms=round(latency_ms, 2),
            exploration_applied=True,
            timestamp=datetime.now(timezone.utc),
        )


rec_service = PulseRecService()
