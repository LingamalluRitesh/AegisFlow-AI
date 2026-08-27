"""
Distributed Span Tracing & OpenTelemetry Context Propagator
Provides lightweight, zero-overhead span instrumentation and distributed context propagation.
"""

import time
import uuid
from typing import Dict, Any, Optional, List
from contextlib import contextmanager
from backend.core.logging import get_logger, correlation_id_var

logger = get_logger("core.tracing")


class Span:
    """Represents an individual unit of work within a distributed trace."""

    def __init__(self, name: str, parent_id: Optional[str] = None, tags: Optional[Dict[str, Any]] = None):
        self.name = name
        self.span_id = str(uuid.uuid4())[:12]
        self.trace_id = correlation_id_var.get()
        self.parent_id = parent_id
        self.start_time: float = time.perf_counter()
        self.end_time: Optional[float] = None
        self.duration_ms: float = 0.0
        self.tags: Dict[str, Any] = tags or {}
        self.events: List[Dict[str, Any]] = []

    def set_tag(self, key: str, value: Any) -> "Span":
        self.tags[key] = value
        return self

    def log_event(self, event_name: str, payload: Optional[Dict[str, Any]] = None) -> None:
        self.events.append({
            "name": event_name,
            "timestamp": time.perf_counter(),
            "payload": payload or {},
        })

    def finish(self) -> float:
        self.end_time = time.perf_counter()
        self.duration_ms = (self.end_time - self.start_time) * 1000.0
        return self.duration_ms


class Tracer:
    """Global lightweight distributed tracer instance."""

    def __init__(self):
        self._active_spans: List[Span] = []

    @contextmanager
    def start_span(self, name: str, tags: Optional[Dict[str, Any]] = None):
        parent_id = self._active_spans[-1].span_id if self._active_spans else None
        span = Span(name=name, parent_id=parent_id, tags=tags)
        self._active_spans.append(span)
        try:
            yield span
        finally:
            span.finish()
            self._active_spans.pop()
            logger.debug_ctx(
                f"Span completed: {name}",
                span_id=span.span_id,
                duration_ms=round(span.duration_ms, 3),
                tags=span.tags,
            )


tracer = Tracer()
