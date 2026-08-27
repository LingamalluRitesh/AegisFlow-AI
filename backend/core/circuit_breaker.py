"""
Distributed High-Reliability Circuit Breaker with Half-Open Recovery
Guards downstream model serving nodes and external dependencies from cascading failures.
"""

import time
import enum
import threading
from typing import Callable, Any, Optional
from backend.core.exceptions import CircuitBreakerOpenError
from backend.core.logging import get_logger

logger = get_logger("circuit_breaker")


class CircuitState(enum.Enum):
    CLOSED = "CLOSED"      # Normal operation, traffic allowed
    OPEN = "OPEN"          # Tripped, traffic blocked immediately
    HALF_OPEN = "HALF_OPEN"# Testing recovery with trial traffic


class CircuitBreaker:
    """Thread-safe circuit breaker with dynamic reset timeout and failure rate threshold."""

    def __init__(
        self,
        name: str,
        failure_threshold: int = 5,
        recovery_timeout_sec: float = 30.0,
        success_threshold_half_open: int = 3,
    ):
        self.name = name
        self.failure_threshold = failure_threshold
        self.recovery_timeout_sec = recovery_timeout_sec
        self.success_threshold_half_open = success_threshold_half_open

        self._state = CircuitState.CLOSED
        self._consecutive_failures = 0
        self._consecutive_successes = 0
        self._last_state_change_time = time.monotonic()
        self._lock = threading.Lock()

    @property
    def state(self) -> CircuitState:
        with self._lock:
            self._evaluate_state_transitions()
            return self._state

    def _evaluate_state_transitions(self) -> None:
        """Internal helper transitioning from OPEN to HALF_OPEN when recovery timeout passes."""
        now = time.monotonic()
        if self._state == CircuitState.OPEN:
            if (now - self._last_state_change_time) >= self.recovery_timeout_sec:
                logger.warn_ctx(f"CircuitBreaker '{self.name}' transitioning from OPEN to HALF_OPEN")
                self._state = CircuitState.HALF_OPEN
                self._consecutive_successes = 0
                self._last_state_change_time = now

    def record_success(self) -> None:
        """Records a successful operation through the circuit."""
        with self._lock:
            if self._state == CircuitState.HALF_OPEN:
                self._consecutive_successes += 1
                if self._consecutive_successes >= self.success_threshold_half_open:
                    logger.info_ctx(f"CircuitBreaker '{self.name}' RECOVERED: transitioning HALF_OPEN to CLOSED")
                    self._state = CircuitState.CLOSED
                    self._consecutive_failures = 0
                    self._consecutive_successes = 0
                    self._last_state_change_time = time.monotonic()
            elif self._state == CircuitState.CLOSED:
                self._consecutive_failures = 0

    def record_failure(self, error: Optional[Exception] = None) -> None:
        """Records an execution failure, potentially tripping the circuit."""
        with self._lock:
            now = time.monotonic()
            if self._state == CircuitState.HALF_OPEN:
                logger.error_ctx(f"CircuitBreaker '{self.name}' failure in HALF_OPEN state. Tripping back to OPEN.", exc=error)
                self._state = CircuitState.OPEN
                self._consecutive_failures += 1
                self._last_state_change_time = now
            elif self._state == CircuitState.CLOSED:
                self._consecutive_failures += 1
                if self._consecutive_failures >= self.failure_threshold:
                    logger.error_ctx(
                        f"CircuitBreaker '{self.name}' threshold reached ({self._consecutive_failures} failures). Tripping to OPEN.",
                        exc=error
                    )
                    self._state = CircuitState.OPEN
                    self._last_state_change_time = now

    def check_permission(self) -> None:
        """Raises CircuitBreakerOpenError if circuit is currently open."""
        with self._lock:
            self._evaluate_state_transitions()
            if self._state == CircuitState.OPEN:
                raise CircuitBreakerOpenError(service_name=self.name)

    def execute(self, func: Callable[..., Any], *args, **kwargs) -> Any:
        """Executes a callable under circuit breaker protection."""
        self.check_permission()
        try:
            result = func(*args, **kwargs)
            self.record_success()
            return result
        except Exception as e:
            self.record_failure(e)
            raise


class CircuitBreakerRegistry:
    """Registry maintaining named circuit breakers across microservices."""

    def __init__(self):
        self._breakers: Dict[str, CircuitBreaker] = {}
        self._lock = threading.Lock()

    def get_or_create(
        self,
        name: str,
        failure_threshold: int = 5,
        recovery_timeout_sec: float = 30.0,
    ) -> CircuitBreaker:
        with self._lock:
            if name not in self._breakers:
                self._breakers[name] = CircuitBreaker(
                    name=name,
                    failure_threshold=failure_threshold,
                    recovery_timeout_sec=recovery_timeout_sec
                )
            return self._breakers[name]


circuit_breaker_registry = CircuitBreakerRegistry()
