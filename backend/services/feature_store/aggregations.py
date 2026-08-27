"""
High-Performance Stateful Sliding Window Aggregators
Computes streaming velocity, count, sum, mean, variance, and entropy across time windows.
"""

import time
import math
from typing import Dict, Any, Optional
from collections import deque
import threading
from enum import Enum


class AggregateFunction(str, Enum):
    COUNT = "COUNT"
    SUM = "SUM"
    MEAN = "MEAN"
    STDDEV = "STDDEV"
    MIN = "MIN"
    MAX = "MAX"
    VELOCITY = "VELOCITY"


class SlidingWindowAggregator:
    def __init__(self, entity_id: str, max_window_seconds: int = 86400):
        self.entity_id = entity_id
        self.max_window_seconds = max_window_seconds
        self._events: deque = deque()
        self._lock = threading.Lock()

    def add_event(self, timestamp: float, amount: float = 1.0, metadata: Optional[Dict[str, Any]] = None) -> None:
        with self._lock:
            self._events.append((timestamp, amount, metadata or {}))
            self._evict_expired(timestamp)

    def _evict_expired(self, current_time: float) -> None:
        cutoff = current_time - self.max_window_seconds
        while self._events and self._events[0][0] < cutoff:
            self._events.popleft()

    def compute_window_stats(self, window_seconds: int, current_time: Optional[float] = None) -> Dict[str, float]:
        now = current_time if current_time is not None else time.time()
        window_start = now - window_seconds

        with self._lock:
            window_events = [ev for ev in self._events if ev[0] >= window_start]

        if not window_events:
            return {
                "count": 0.0,
                "sum": 0.0,
                "mean": 0.0,
                "stddev": 0.0,
                "min": 0.0,
                "max": 0.0,
                "velocity_per_min": 0.0,
            }

        amounts = [ev[1] for ev in window_events]
        n = len(amounts)
        total = sum(amounts)
        mean = total / n
        variance = sum((x - mean) ** 2 for x in amounts) / n if n > 1 else 0.0
        stddev = math.sqrt(variance)
        window_minutes = max(0.1, window_seconds / 60.0)

        return {
            "count": float(n),
            "sum": float(total),
            "mean": float(mean),
            "stddev": float(stddev),
            "min": float(min(amounts)),
            "max": float(max(amounts)),
            "velocity_per_min": float(n / window_minutes),
        }
