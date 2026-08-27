"""
Dead Letter Queue (DLQ) Manager for Malformed and Poison-Pill Stream Events
"""

import time
from typing import Dict, Any, List
from collections import deque
import threading
from backend.core.logging import get_logger

logger = get_logger("stream.dlq")


class DeadLetterQueueManager:
    def __init__(self, max_items: int = 5000):
        self.max_items = max_items
        self._dlq: deque = deque(maxlen=max_items)
        self._lock = threading.Lock()

    def record_failure(self, topic: str, raw_payload: Any, error: str) -> None:
        entry = {
            "topic": topic,
            "raw_payload": str(raw_payload)[:1000],
            "error": error,
            "failed_at": time.time(),
        }
        with self._lock:
            self._dlq.append(entry)
        logger.error_ctx(f"Event routed to Dead-Letter-Queue on topic '{topic}': {error}")

    def list_dlq_entries(self, limit: int = 100) -> List[Dict[str, Any]]:
        with self._lock:
            return list(self._dlq)[-limit:]


dlq_manager = DeadLetterQueueManager()
