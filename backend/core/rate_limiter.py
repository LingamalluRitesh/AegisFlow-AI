"""
Token Bucket & Sliding Window Rate Limiting Engine
Protects ingestion APIs from spikes, denial of service, and noisy neighbors.
"""

import time
import threading
from typing import Dict, Tuple, Optional


class TokenBucket:
    """Thread-safe in-memory Token Bucket rate limiter."""

    def __init__(self, capacity: int, refill_rate_per_sec: float):
        self.capacity = float(capacity)
        self.refill_rate_per_sec = refill_rate_per_sec
        self._tokens = float(capacity)
        self._last_refill_time = time.monotonic()
        self._lock = threading.Lock()

    def _refill(self) -> None:
        now = time.monotonic()
        elapsed = now - self._last_refill_time
        if elapsed > 0:
            self._tokens = min(self.capacity, self._tokens + elapsed * self.refill_rate_per_sec)
            self._last_refill_time = now

    def acquire(self, tokens: int = 1) -> bool:
        with self._lock:
            self._refill()
            if self._tokens >= tokens:
                self._tokens -= tokens
                return True
            return False

    @property
    def available_tokens(self) -> float:
        with self._lock:
            self._refill()
            return self._tokens


class SlidingWindowRateLimiter:
    """Sliding Window log-based rate limiter for precise burst control."""

    def __init__(self, max_requests: int, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._client_logs: Dict[str, list] = {}
        self._lock = threading.Lock()

    def is_allowed(self, client_id: str) -> Tuple[bool, int]:
        """
        Returns (is_allowed, remaining_requests_in_window).
        """
        now = time.time()
        window_start = now - self.window_seconds

        with self._lock:
            timestamps = self._client_logs.get(client_id, [])
            valid_timestamps = [ts for ts in timestamps if ts > window_start]

            if len(valid_timestamps) < self.max_requests:
                valid_timestamps.append(now)
                self._client_logs[client_id] = valid_timestamps
                remaining = self.max_requests - len(valid_timestamps)
                return True, remaining
            else:
                self._client_logs[client_id] = valid_timestamps
                return False, 0

    def cleanup(self) -> int:
        """Removes expired tracking keys to prevent unbounded memory growth."""
        now = time.time()
        window_start = now - self.window_seconds
        removed = 0
        with self._lock:
            keys = list(self._client_logs.keys())
            for k in keys:
                self._client_logs[k] = [ts for ts in self._client_logs[k] if ts > window_start]
                if not self._client_logs[k]:
                    del self._client_logs[k]
                    removed += 1
        return removed


rate_limiter = SlidingWindowRateLimiter(max_requests=1000, window_seconds=60)
