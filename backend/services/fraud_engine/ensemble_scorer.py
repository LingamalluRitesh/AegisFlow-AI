"""
Ensemble Risk Scoring Engine
Fuses deterministic rule boosts, graph multipliers, supervised tree probabilities, and anomaly scores.
"""

class EnsembleRiskScorer:
    def __init__(
        self,
        rule_weight: float = 0.40,
        ml_model_weight: float = 0.35,
        anomaly_weight: float = 0.15,
        graph_weight: float = 0.10,
    ):
        self.rule_weight = rule_weight
        self.ml_model_weight = ml_model_weight
        self.anomaly_weight = anomaly_weight
        self.graph_weight = graph_weight

    def compute_ensemble_score(
        self,
        rule_boost: float,
        ml_model_prob: float,
        anomaly_score: float,
        graph_multiplier: float,
    ) -> float:
        base_score = (
            self.rule_weight * rule_boost
            + self.ml_model_weight * ml_model_prob
            + self.anomaly_weight * anomaly_score
        )
        final_score = base_score * (1.0 + (graph_multiplier - 1.0) * self.graph_weight)
        return float(max(0.0, min(1.0, final_score)))
