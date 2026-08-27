"""
Maximal Marginal Relevance (MMR) & Diversity Reranking
Prevents filter bubbles and duplicate categories by balancing relevance against novelty.
"""

from typing import List, Dict, Any


class MaximalMarginalRelevanceReranker:
    def __init__(self, diversity_lambda: float = 0.3):
        self.diversity_lambda = diversity_lambda

    def rerank(self, candidate_items: List[Dict[str, Any]], top_k: int = 10) -> List[Dict[str, Any]]:
        if len(candidate_items) <= top_k:
            return candidate_items

        selected = []
        selected_categories = set()
        remaining = list(candidate_items)

        while len(selected) < top_k and remaining:
            best_idx = 0
            best_score = -1.0

            for i, item in enumerate(remaining):
                cat = item.get("category", "general")
                penalty = 0.4 if cat in selected_categories else 0.0
                effective_score = item["score"] * (1.0 - self.diversity_lambda * penalty)

                if effective_score > best_score:
                    best_score = effective_score
                    best_idx = i

            chosen = remaining.pop(best_idx)
            selected.append(chosen)
            selected_categories.add(chosen.get("category", "general"))

        return selected
