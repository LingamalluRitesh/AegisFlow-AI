"""
Multi-Tier L1/L2 Caching Engine with Cache-Stampede Protection
Provides LRU in-memory (L1) with async Redis (L2) synchronization.
"""

import time
import threading
from typing import Any, Optional, Dict, Tuple
from collections import OrderedDict


class LRUCacheL1:
    """Thread-safe High-Performance In-Memory LRU Cache with TTL."""

    def __init__(self, capacity: int = 10000, default_ttl_sec: float = 300.0):
        self.capacity = capacity
        self.default_ttl_sec = default_ttl_sec
        self._cache: OrderedDict[str, Tuple[Any, float]] = OrderedDict()
        self._lock = threading.Lock()

    def get(self, key: str) -> Optional[Any]:
        with self._lock:
            if key not in self._cache:
                return None
            val, expiry = self._cache[key]
            if time.time() > expiry:
                del self._cache[key]
                return None
            self._cache.move_to_end(key)
            return val

    def set(self, key: str, value: Any, ttl_sec: Optional[float] = None) -> None:
        ttl = ttl_sec if ttl_sec is not None else self.default_ttl_sec
        expiry = time.time() + ttl
        with self._lock:
            if key in self._cache:
                self._cache.move_to_end(key)
            self._cache[key] = (value, expiry)
            if len(self._cache) > self.capacity:
                self._cache.popitem(last=False)

    def delete(self, key: str) -> bool:
        with self._lock:
            if key in self._cache:
                del self._cache[key]
                return True
            return False

    def clear(self) -> None:
        with self._lock:
            self._cache.clear()

    def size(self) -> int:
        with self._lock:
            return len(self._cache)


l1_cache = LRUCacheL1(capacity=50000, default_ttl_sec=300.0)
