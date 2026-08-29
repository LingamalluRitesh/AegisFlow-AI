"""
Prometheus Telemetry Exporter & SLA Latency Monitor.
Tracks real-time fraud decision throughput, latency distributions, and feature store cache hit rates.
"""

from typing import Dict, List, Any
import time


class AegisMetricsRegistry:
    """Collects real-time telemetry metrics and serializes to Prometheus exposition text."""

    def __init__(self):
        self.decisions_total: Dict[str, int] = {}
        self.scoring_latencies_ms: List[float] = []
        self.cache_hits_total: int = 0
        self.cache_misses_total: int = 0

    def record_decision(self, decision: str, latency_ms: float) -> None:
        self.decisions_total[decision] = self.decisions_total.get(decision, 0) + 1
        self.scoring_latencies_ms.append(latency_ms)

    def record_cache_lookup(self, hit: bool) -> None:
        if hit:
            self.cache_hits_total += 1
        else:
            self.cache_misses_total += 1

    def get_summary(self) -> Dict[str, Any]:
        total_evals = sum(self.decisions_total.values())
        avg_lat = (sum(self.scoring_latencies_ms) / len(self.scoring_latencies_ms)) if self.scoring_latencies_ms else 0.0
        total_lookups = self.cache_hits_total + self.cache_misses_total
        hit_rate = (self.cache_hits_total / total_lookups) if total_lookups > 0 else 1.0

        return {
            "total_evaluations": total_evals,
            "decisions": self.decisions_total,
            "avg_latency_ms": round(avg_lat, 2),
            "feature_cache_hit_rate": round(hit_rate, 4),
        }

    def export_prometheus(self) -> str:
        lines = [
            "# HELP aegisflow_decisions_total Total fraud decisions evaluated",
            "# TYPE aegisflow_decisions_total counter",
        ]
        for dec, count in self.decisions_total.items():
            lines.append(f'aegisflow_decisions_total{{decision="{dec}"}} {count}')

        lines.extend([
            "# HELP aegisflow_feature_cache_hits_total Total feature store cache hits",
            "# TYPE aegisflow_feature_cache_hits_total counter",
            f"aegisflow_feature_cache_hits_total {self.cache_hits_total}",
            "# HELP aegisflow_feature_cache_misses_total Total feature store cache misses",
            "# TYPE aegisflow_feature_cache_misses_total counter",
            f"aegisflow_feature_cache_misses_total {self.cache_misses_total}",
        ])

        return "\n".join(lines) + "\n"
