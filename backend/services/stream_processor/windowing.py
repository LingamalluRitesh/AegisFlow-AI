"""
Stateful Window Operators with Event-Time Watermarking
Implements Tumbling, Sliding, and Session windows for high-throughput streaming events.
"""

import time
from typing import Dict, Tuple
import threading


class StreamWindow:
    def __init__(self, window_size_seconds: int):
        self.window_size_seconds = window_size_seconds


class TumblingWindow(StreamWindow):
    def get_window_bounds(self, timestamp: float) -> Tuple[int, int]:
        start = int(timestamp // self.window_size_seconds) * self.window_size_seconds
        end = start + self.window_size_seconds
        return start, end


class SlidingWindow(StreamWindow):
    def __init__(self, window_size_seconds: int, slide_interval_seconds: int):
        super().__init__(window_size_seconds)
        self.slide_interval_seconds = slide_interval_seconds


class SessionWindow:
    def __init__(self, inactivity_gap_seconds: int = 1800):
        self.inactivity_gap_seconds = inactivity_gap_seconds
        self._user_last_active: Dict[str, float] = {}
        self._user_session_ids: Dict[str, str] = {}
        self._lock = threading.Lock()

    def get_or_create_session(self, user_id: str, timestamp: float) -> str:
        with self._lock:
            last_time = self._user_last_active.get(user_id, 0.0)
            if (timestamp - last_time) > self.inactivity_gap_seconds or user_id not in self._user_session_ids:
                session_id = f"sess_{user_id}_{int(timestamp)}"
                self._user_session_ids[user_id] = session_id

            self._user_last_active[user_id] = timestamp
            return self._user_session_ids[user_id]
