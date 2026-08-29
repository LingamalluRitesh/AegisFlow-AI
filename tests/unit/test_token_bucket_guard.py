import time
import pytest
from backend.core.token_bucket_guard import TokenBucketSecurityGuard


def test_token_bucket_normal_and_burst():
    guard = TokenBucketSecurityGuard(capacity=5.0, refill_rate_per_sec=10.0)

    # Allow initial burst up to capacity
    for _ in range(5):
        res = guard.allow_request("client_1", tokens_required=1.0)
        assert res["allowed"] is True

    # 6th request exhausts capacity -> triggers cooldown
    res6 = guard.allow_request("client_1", tokens_required=1.0)
    assert res6["allowed"] is False
    assert res6["reason"] in ["RATE_LIMIT_EXCEEDED", "CLIENT_IN_PENALTY_COOLDOWN"]


def test_token_bucket_refill():
    guard = TokenBucketSecurityGuard(capacity=10.0, refill_rate_per_sec=100.0)
    guard.allow_request("client_2", tokens_required=8.0)
    time.sleep(0.05)  # Refills 5 tokens
    res = guard.allow_request("client_2", tokens_required=2.0)
    assert res["allowed"] is True
