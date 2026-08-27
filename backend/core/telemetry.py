"""
Telemetry, Metrics Registry, and OpenTelemetry Instrumentation Core
Tracks latency percentiles, throughput counters, gauge statuses, and span traces.
"""

import time
import functools
from typing import Dict, Any, Optional, Callable, List
from collections import defaultdict
import threading
from backend.core.logging import get_logger

logger = get_logger("telemetry.core")


class MetricCounter:
    """Thread-safe integer and float counter with label dimensions."""

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self._values: Dict[str, float] = defaultdict(float)
        self._lock = threading.Lock()

    def _format_labels(self, labels: Optional[Dict[str, str]]) -> str:
        if not labels:
            return ""
        return ",".join(f'{k}="{v}"' for k, v in sorted(labels.items()))

    def inc(self, value: float = 1.0, labels: Optional[Dict[str, str]] = None) -> None:
        key = self._format_labels(labels)
        with self._lock:
            self._values[key] += value

    def get_value(self, labels: Optional[Dict[str, str]] = None) -> float:
        key = self._format_labels(labels)
        with self._lock:
            return self._values.get(key, 0.0)

    def collect(self) -> List[Dict[str, Any]]:
        with self._lock:
            return [
                {"name": self.name, "labels": k, "value": v, "type": "counter"}
                for k, v in self._values.items()
            ]


class MetricGauge:
    """Thread-safe gauge representing an instantaneous numerical metric."""

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self._values: Dict[str, float] = {}
        self._lock = threading.Lock()

    def _format_labels(self, labels: Optional[Dict[str, str]]) -> str:
        if not labels:
            return ""
        return ",".join(f'{k}="{v}"' for k, v in sorted(labels.items()))

    def set(self, value: float, labels: Optional[Dict[str, str]] = None) -> None:
        key = self._format_labels(labels)
        with self._lock:
            self._values[key] = value

    def get_value(self, labels: Optional[Dict[str, str]] = None) -> float:
        key = self._format_labels(labels)
        with self._lock:
            return self._values.get(key, 0.0)

    def collect(self) -> List[Dict[str, Any]]:
        with self._lock:
            return [
                {"name": self.name, "labels": k, "value": v, "type": "gauge"}
                for k, v in self._values.items()
            ]


class MetricHistogram:
    """Thread-safe latency and duration histogram with standard bucket distributions."""

    DEFAULT_BUCKETS = (0.001, 0.005, 0.010, 0.025, 0.050, 0.100, 0.250, 0.500, 1.0, 2.5, 5.0, 10.0)

    def __init__(self, name: str, description: str, buckets: Optional[tuple] = None):
        self.name = name
        self.description = description
        self.buckets = buckets or self.DEFAULT_BUCKETS
        self._counts: Dict[str, Dict[float, int]] = defaultdict(lambda: {b: 0 for b in self.buckets})
        self._sums: Dict[str, float] = defaultdict(float)
        self._totals: Dict[str, int] = defaultdict(int)
        self._lock = threading.Lock()

    def _format_labels(self, labels: Optional[Dict[str, str]]) -> str:
        if not labels:
            return ""
        return ",".join(f'{k}="{v}"' for k, v in sorted(labels.items()))

    def observe(self, value: float, labels: Optional[Dict[str, str]] = None) -> None:
        key = self._format_labels(labels)
        with self._lock:
            self._sums[key] += value
            self._totals[key] += 1
            for b in self.buckets:
                if value <= b:
                    self._counts[key][b] += 1

    def collect(self) -> List[Dict[str, Any]]:
        with self._lock:
            results = []
            for key, total in self._totals.items():
                results.append({
                    "name": self.name,
                    "labels": key,
                    "count": total,
                    "sum": self._sums[key],
                    "buckets": dict(self._counts[key]),
                    "type": "histogram"
                })
            return results


class TelemetryRegistry:
    """Centralized metrics registry and Prometheus exposition manager."""

    def __init__(self):
        self._counters: Dict[str, MetricCounter] = {}
        self._gauges: Dict[str, MetricGauge] = {}
        self._histograms: Dict[str, MetricHistogram] = {}
        self._lock = threading.Lock()
        self._init_standard_metrics()

    def _init_standard_metrics(self):
        self.register_counter("aegis_http_requests_total", "Total incoming HTTP requests")
        self.register_counter("aegis_fraud_evaluations_total", "Total fraud evaluations processed")
        self.register_counter("aegis_fraud_blocked_total", "Total transactions blocked for fraud")
        self.register_counter("aegis_recommendations_served_total", "Total recommendations generated")
        self.register_counter("aegis_stream_events_ingested_total", "Total streaming events consumed")
        self.register_gauge("aegis_online_feature_cache_size", "Number of hot entities cached in online store")
        self.register_gauge("aegis_model_drift_psi_score", "Current population stability index for features")
        self.register_histogram("aegis_inference_latency_seconds", "Inference latency in seconds")
        self.register_histogram("aegis_feature_retrieval_latency_seconds", "Feature lookup latency in seconds")
        self.register_histogram("aegis_end_to_end_decision_latency_seconds", "End-to-end decision pipeline latency")

    def register_counter(self, name: str, description: str) -> MetricCounter:
        with self._lock:
            if name not in self._counters:
                self._counters[name] = MetricCounter(name, description)
            return self._counters[name]

    def register_gauge(self, name: str, description: str) -> MetricGauge:
        with self._lock:
            if name not in self._gauges:
                self._gauges[name] = MetricGauge(name, description)
            return self._gauges[name]

    def register_histogram(self, name: str, description: str, buckets: Optional[tuple] = None) -> MetricHistogram:
        with self._lock:
            if name not in self._histograms:
                self._histograms[name] = MetricHistogram(name, description, buckets)
            return self._histograms[name]

    def get_counter(self, name: str) -> MetricCounter:
        return self._counters[name]

    def get_gauge(self, name: str) -> MetricGauge:
        return self._gauges[name]

    def get_histogram(self, name: str) -> MetricHistogram:
        return self._histograms[name]

    def export_prometheus_format(self) -> str:
        lines = []
        for name, c in self._counters.items():
            lines.append(f"# HELP {name} {c.description}")
            lines.append(f"# TYPE {name} counter")
            for item in c.collect():
                lbl = f"{{{item['labels']}}}" if item['labels'] else ""
                lines.append(f"{name}{lbl} {item['value']}")

        for name, g in self._gauges.items():
            lines.append(f"# HELP {name} {g.description}")
            lines.append(f"# TYPE {name} gauge")
            for item in g.collect():
                lbl = f"{{{item['labels']}}}" if item['labels'] else ""
                lines.append(f"{name}{lbl} {item['value']}")

        for name, h in self._histograms.items():
            lines.append(f"# HELP {name} {h.description}")
            lines.append(f"# TYPE {name} histogram")
            for item in h.collect():
                lbl_prefix = f"{item['labels']}," if item['labels'] else ""
                for le, count in sorted(item['buckets'].items()):
                    lines.append(f'{name}_bucket{{{lbl_prefix}le="{le}"}} {count}')
                lines.append(f'{name}_bucket{{{lbl_prefix}le="+Inf"}} {item["count"]}')
                lbl = f"{{{item['labels']}}}" if item['labels'] else ""
                lines.append(f"{name}_sum{lbl} {item['sum']}")
                lines.append(f"{name}_count{lbl} {item['count']}")

        return "\n".join(lines) + "\n"


telemetry_manager = TelemetryRegistry()


def record_timing(histogram_name: str, labels: Optional[Dict[str, str]] = None):
    """Decorator timing synchronous and asynchronous function executions."""
    def decorator(func: Callable):
        import asyncio
        if asyncio.iscoroutinefunction(func):
            @functools.wraps(func)
            async def async_wrapper(*args, **kwargs):
                start = time.perf_counter()
                try:
                    return await func(*args, **kwargs)
                finally:
                    duration = time.perf_counter() - start
                    telemetry_manager.get_histogram(histogram_name).observe(duration, labels)
            return async_wrapper
        else:
            @functools.wraps(func)
            def sync_wrapper(*args, **kwargs):
                start = time.perf_counter()
                try:
                    return func(*args, **kwargs)
                finally:
                    duration = time.perf_counter() - start
                    telemetry_manager.get_histogram(histogram_name).observe(duration, labels)
            return sync_wrapper
    return decorator
