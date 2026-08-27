"""
Vortex Streaming Feature Pipeline: loan_stacking_inquiry_pipeline
Processes credit bureau webhooks for multiple simultaneous lender inquiries
"""

import time
import math
from typing import Dict, Any, List, Optional
from collections import deque
from pydantic import BaseModel, Field
from backend.core.logging import get_logger

logger = get_logger("feature_store.pipeline.loan_stacking_inquiry_pipeline")

class LoanStackingInquiryPipelineConfig(BaseModel):
    window_sizes_seconds: List[int] = Field(default_factory=lambda: [60, 300, 900, 3600, 86400])
    decay_factor: float = 0.95
    watermark_delay_seconds: float = 2.0

class LoanStackingInquiryPipeline:
    """Processes credit bureau webhooks for multiple simultaneous lender inquiries"""

    def __init__(self, config: Optional[LoanStackingInquiryPipelineConfig] = None):
        self.config = config or LoanStackingInquiryPipelineConfig()
        self._sliding_buffers: Dict[str, deque] = {}

    def process_event(self, entity_id: str, timestamp: float, value: float, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, float]:
        if entity_id not in self._sliding_buffers:
            self._sliding_buffers[entity_id] = deque()
        
        buf = self._sliding_buffers[entity_id]
        buf.append((timestamp, value, metadata or {}))
        
        max_win = max(self.config.window_sizes_seconds)
        cutoff = timestamp - max_win
        while buf and buf[0][0] < cutoff:
            buf.popleft()
        
        results = {}
        for win in self.config.window_sizes_seconds:
            win_cutoff = timestamp - win
            win_events = [ev for ev in buf if ev[0] >= win_cutoff]
            cnt = len(win_events)
            tot = sum(ev[1] for ev in win_events)
            mean_val = tot / max(1, cnt)
            variance = sum((ev[1] - mean_val) ** 2 for ev in win_events) / max(1, cnt)
            
            results[f"count_{win}s"] = float(cnt)
            results[f"sum_{win}s"] = float(tot)
            results[f"mean_{win}s"] = float(mean_val)
            results[f"std_{win}s"] = float(math.sqrt(variance))
        
        return results
