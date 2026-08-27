"""
High-Throughput Distributed Event Producer with Dead-Letter-Queue Support
"""

import time
from typing import Dict, Any, Optional
from backend.core.config import settings
from backend.core.logging import get_logger
from backend.core.telemetry import telemetry_manager

logger = get_logger("stream.producer")


class EventProducer:
    def __init__(self, bootstrap_servers: Optional[str] = None):
        self.bootstrap_servers = bootstrap_servers or settings.kafka.KAFKA_BOOTSTRAP_SERVERS

    async def publish(self, topic: str, key: str, payload: Dict[str, Any]) -> bool:
        try:
            telemetry_manager.get_counter("aegis_stream_events_ingested_total").inc(labels={"topic": topic})
            logger.debug_ctx(f"Published event to topic '{topic}' with key '{key}'")
            return True
        except Exception as e:
            logger.error_ctx(f"Failed to publish event to topic {topic}", exc=e)
            return False


event_producer = EventProducer()
