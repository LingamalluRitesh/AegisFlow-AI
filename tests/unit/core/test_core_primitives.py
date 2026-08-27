import pytest
from backend.core.config import settings
from backend.core.crypto import crypto_manager
from backend.core.circuit_breaker import CircuitBreaker, CircuitState
from backend.core.rate_limiter import SlidingWindowRateLimiter
from backend.core.cache import LRUCacheL1
from backend.core.math_utils import (
    vector_cosine_similarity,
    calculate_haversine_distance_km,
    compute_population_stability_index,
    compute_kolmogorov_smirnov_statistic,
)


def test_crypto_hashing_and_hmac():
    token = crypto_manager.generate_token(16)
    assert len(token) == 32
    h = crypto_manager.hash_sha256("test_data")
    assert len(h) == 64
    sig = crypto_manager.hmac_sign("message_1")
    assert crypto_manager.hmac_verify("message_1", sig) is True
    assert crypto_manager.hmac_verify("tampered_message", sig) is False


def test_circuit_breaker_lifecycle():
    cb = CircuitBreaker(name="test_service", failure_threshold=2, recovery_timeout_sec=0.1)
    assert cb.state == CircuitState.CLOSED
    cb.record_failure()
    assert cb.state == CircuitState.CLOSED
    cb.record_failure()
    assert cb.state == CircuitState.OPEN


def test_rate_limiter_sliding_window():
    limiter = SlidingWindowRateLimiter(max_requests=3, window_seconds=10)
    allowed1, rem1 = limiter.is_allowed("user_1")
    allowed2, rem2 = limiter.is_allowed("user_1")
    allowed3, rem3 = limiter.is_allowed("user_1")
    allowed4, rem4 = limiter.is_allowed("user_1")
    assert allowed1 is True
    assert allowed2 is True
    assert allowed3 is True
    assert allowed4 is False


def test_lru_cache_ttl():
    cache = LRUCacheL1(capacity=2, default_ttl_sec=100.0)
    cache.set("k1", "v1")
    cache.set("k2", "v2")
    assert cache.get("k1") == "v1"
    cache.set("k3", "v3")
    assert cache.get("k3") == "v3"


def test_math_statistics_and_drift():
    v1 = [1.0, 0.0, 0.0]
    v2 = [1.0, 0.0, 0.0]
    assert vector_cosine_similarity(v1, v2) == pytest.approx(1.0)

    dist = calculate_haversine_distance_km(40.7128, -74.0060, 34.0522, -118.2437)
    assert dist > 3900.0 and dist < 4000.0

    exp = [1.0, 2.0, 3.0, 4.0, 5.0] * 20
    act = [1.1, 2.1, 3.0, 4.2, 4.9] * 20
    psi = compute_population_stability_index(exp, act)
    assert psi >= 0.0
