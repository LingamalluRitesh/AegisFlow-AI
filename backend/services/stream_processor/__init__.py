"""
StreamEngine: Distributed Stateful Streaming Pipeline for Real-Time ML
Handles continuous event ingestion, watermarked window operators, dynamic aggregations,
and dead-letter queues.
"""

from backend.services.stream_processor.engine import StreamingEngine, streaming_engine
from backend.services.stream_processor.windowing import TumblingWindow, SlidingWindow, SessionWindow
from backend.services.stream_processor.kafka_producer import EventProducer, event_producer
from backend.services.stream_processor.kafka_consumer import EventConsumer
from backend.services.stream_processor.dead_letter_queue import DeadLetterQueueManager, dlq_manager

__all__ = [
    "StreamingEngine",
    "streaming_engine",
    "TumblingWindow",
    "SlidingWindow",
    "SessionWindow",
    "EventProducer",
    "event_producer",
    "EventConsumer",
    "DeadLetterQueueManager",
    "dlq_manager",
]
