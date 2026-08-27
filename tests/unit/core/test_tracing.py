"""
Unit tests for distributed span tracing and context propagation.
"""

import time
from backend.core.tracing import tracer, Span


def test_span_lifecycle():
    span = Span(name="test_span", tags={"module": "core"})
    assert span.name == "test_span"
    assert span.tags["module"] == "core"
    assert span.end_time is None

    span.set_tag("user_id", "usr_123")
    span.log_event("sub_task_completed", {"items": 5})

    time.sleep(0.01)
    duration = span.finish()
    assert duration > 5.0
    assert span.end_time is not None
    assert len(span.events) == 1


def test_tracer_context_manager():
    with tracer.start_span("parent_operation", tags={"env": "test"}) as parent:
        parent.set_tag("step", "init")
        with tracer.start_span("child_operation") as child:
            assert child.parent_id == parent.span_id
            child.set_tag("child_status", "ok")

        assert parent.tags["step"] == "init"
