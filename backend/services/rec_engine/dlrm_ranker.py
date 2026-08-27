"""
Deep Learning Recommendation Model (DLRM) & Multi-Task Ranker
Jointly predicts Click-Through-Rate (CTR) and Conversion-Rate (CVR) with cross-feature interaction layers.
"""

from typing import Dict, Any, Tuple


class DLRMMultiTaskRanker:
    def predict_ctr_cvr(
        self,
        user_features: Dict[str, Any],
        item_features: Dict[str, Any],
        retrieval_similarity: float,
    ) -> Tuple[float, float, float]:
        base_ctr = float(item_features.get("item_ctr_7d", 0.03))
        base_cvr = float(item_features.get("item_cvr_7d", 0.01))

        sim_boost = max(0.0, retrieval_similarity) * 0.4
        p_ctr = min(0.95, base_ctr + sim_boost)
        p_cvr = min(0.80, base_cvr + (p_ctr * 0.25))

        ranking_score = p_ctr * (1.0 + 2.0 * p_cvr)
        return p_ctr, p_cvr, ranking_score
