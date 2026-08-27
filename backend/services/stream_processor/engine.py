"""
StreamEngine Coordinator: Manages Active Stream Processors and Dynamic Feature Aggregations
"""

import time
from typing import Dict, Any
from backend.core.logging import get_logger
from backend.services.feature_store.aggregations import SlidingWindowAggregator
from backend.services.feature_store.client import feature_store_client

logger = get_logger("stream.engine")


class StreamingEngine:
    def __init__(self):
        self._user_aggregators: Dict[str, SlidingWindowAggregator] = {}
        self._is_running = False

    def get_or_create_user_aggregator(self, user_id: str) -> SlidingWindowAggregator:
        if user_id not in self._user_aggregators:
            self._user_aggregators[user_id] = SlidingWindowAggregator(entity_id=user_id)
        return self._user_aggregators[user_id]

    async def process_transaction_event(self, event_data: Dict[str, Any]) -> None:
        user_id = event_data.get("user_id", "unknown")
        amount = float(event_data.get("amount", 0.0))
        ts = float(event_data.get("timestamp_unix", 0.0)) or time.time()

        agg = self.get_or_create_user_aggregator(user_id)
        agg.add_event(timestamp=ts, amount=amount)

        stats_5m = agg.compute_window_stats(300, ts)
        stats_1h = agg.compute_window_stats(3600, ts)
        stats_24h = agg.compute_window_stats(86400, ts)

        features = {
            "tx_count_5m": int(stats_5m["count"]),
            "tx_amount_sum_5m": float(stats_5m["sum"]),
            "tx_count_1h": int(stats_1h["count"]),
            "tx_amount_sum_1h": float(stats_1h["sum"]),
            "tx_count_24h": int(stats_24h["count"]),
            "tx_amount_sum_24h": float(stats_24h["sum"]),
            "tx_amount_mean_24h": float(stats_24h["mean"]),
            "tx_amount_stddev_24h": float(stats_24h["stddev"]),
        }

        await feature_store_client.push_streaming_features(
            feature_view_name="user_fraud_velocity_features",
            features_by_entity={user_id: features},
        )


streaming_engine = StreamingEngine()
