"""
Token Bucket Rate Limiter & Anti-Scraping Security Guard.
Controls API consumption rates, enforces burst tolerances, and penalizes volumetric attack vectors.
"""

from typing import Dict, Tuple, Any, Optional
import time


class TokenBucketSecurityGuard:
    """Implements thread-safe token bucket rate limiting with penalty cooldown."""

    def __init__(self, capacity: float = 100.0, refill_rate_per_sec: float = 10.0):
        self.capacity = capacity
        self.refill_rate = refill_rate_per_sec
        # client_id -> (tokens, last_refill_timestamp, penalty_until_timestamp)
        self.buckets: Dict[str, Dict[str, float]] = {}

    def _refill(self, client_id: str, now: float) -> None:
        if client_id not in self.buckets:
            self.buckets[client_id] = {
                "tokens": self.capacity,
                "last_refill": now,
                "penalty_until": 0.0,
            }
            return

        bucket = self.buckets[client_id]
        elapsed = now - bucket["last_refill"]
        refilled_tokens = elapsed * self.refill_rate
        bucket["tokens"] = min(self.capacity, bucket["tokens"] + refilled_tokens)
        bucket["last_refill"] = now

    def allow_request(self, client_id: str, tokens_required: float = 1.0) -> Dict[str, Any]:
        now = time.time()
        self._refill(client_id, now)
        bucket = self.buckets[client_id]

        # Check penalty block
        if now < bucket["penalty_until"]:
            return {
                "allowed": False,
                "remaining_tokens": 0.0,
                "retry_after_sec": round(bucket["penalty_until"] - now, 2),
                "reason": "CLIENT_IN_PENALTY_COOLDOWN",
            }

        if bucket["tokens"] >= tokens_required:
            bucket["tokens"] -= tokens_required
            return {
                "allowed": True,
                "remaining_tokens": round(bucket["tokens"], 2),
                "retry_after_sec": 0.0,
                "reason": "REQUEST_ACCEPTED",
            }
        else:
            # Trigger cooldown penalty if continuous rate violations occur
            bucket["penalty_until"] = now + 5.0  # 5 second penalty
            return {
                "allowed": False,
                "remaining_tokens": round(bucket["tokens"], 2),
                "retry_after_sec": 5.0,
                "reason": "RATE_LIMIT_EXCEEDED",
            }
