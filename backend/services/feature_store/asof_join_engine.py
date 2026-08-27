"""
Vortex High-Performance As-Of Temporal Merge Engine
Guarantees point-in-time correctness without lookahead bias across out-of-order streams.
"""

from typing import List, Dict, Any, Optional
import bisect
from backend.core.logging import get_logger

logger = get_logger("feature_store.asof")


class AsOfTemporalJoinEngine:
    """Performs exact point-in-time historical feature hydration."""

    def __init__(self):
        self._entity_timeseries: Dict[str, Dict[str, List[tuple]]] = {}

    def ingest_feature_record(
        self,
        view_name: str,
        entity_key: str,
        timestamp: float,
        features: Dict[str, Any],
    ) -> None:
        if view_name not in self._entity_timeseries:
            self._entity_timeseries[view_name] = {}
        if entity_key not in self._entity_timeseries[view_name]:
            self._entity_timeseries[view_name][entity_key] = []

        timeline = self._entity_timeseries[view_name][entity_key]
        bisect.insort(timeline, (timestamp, features))

    def point_in_time_lookup(
        self,
        view_name: str,
        entity_key: str,
        query_timestamp: float,
    ) -> Optional[Dict[str, Any]]:
        if view_name not in self._entity_timeseries or entity_key not in self._entity_timeseries[view_name]:
            return None

        timeline = self._entity_timeseries[view_name][entity_key]
        idx = bisect.bisect_right(timeline, (query_timestamp, {}))
        if idx == 0:
            return None
        return timeline[idx - 1][1]

    def batch_asof_join(
        self,
        driver_events: List[Dict[str, Any]],
        view_name: str,
        entity_key_field: str = "user_id",
        timestamp_field: str = "timestamp",
    ) -> List[Dict[str, Any]]:
        enriched = []
        for event in driver_events:
            ent = str(event.get(entity_key_field, ""))
            ts = float(event.get(timestamp_field, 0.0))
            features = self.point_in_time_lookup(view_name, ent, ts) or {}

            merged = dict(event)
            for k, v in features.items():
                merged[f"{view_name}__{k}"] = v
            enriched.append(merged)

        return enriched


asof_engine = AsOfTemporalJoinEngine()
