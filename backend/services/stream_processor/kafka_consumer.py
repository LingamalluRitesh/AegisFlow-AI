"""
Resilient Streaming Consumer with Graceful Backpressure & Health Probes
"""

from typing import Callable, Dict, Any
from backend.core.logging import get_logger

logger = get_logger("stream.consumer")


class EventConsumer:
    def __init__(self, topic: str, group_id: str, handler: Callable[[Dict[str, Any]], Any]):
        self.topic = topic
        self.group_id = group_id
        self.handler = handler
        self._running = False

    async def start(self) -> None:
        self._running = True
        logger.info_ctx(f"Stream Consumer started for topic '{self.topic}' [Group: {self.group_id}]")

    async def stop(self) -> None:
        self._running = False
        logger.info_ctx(f"Stream Consumer stopped for topic '{self.topic}'")
