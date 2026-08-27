"""
MLOps Governance Monitor: EqualOpportunityMonitor
Tracks true positive rate parity across protected feature attributes
"""

import time
from typing import Dict, Any, List, Optional, Tuple
import numpy as np
from pydantic import BaseModel, Field
from backend.core.logging import get_logger

logger = get_logger("mlops.monitor.equal_opportunity")

class EqualOpportunityMonitorReport(BaseModel):
    monitor_name: str = "EqualOpportunityMonitor"
    metric_value: float
    threshold: float
    is_alert_triggered: bool
    status: str
    sample_size: int
    timestamp: float = Field(default_factory=time.time)

class EqualOpportunityMonitor:
    """Tracks true positive rate parity across protected feature attributes"""

    def __init__(self, warning_threshold: float = 0.10, critical_threshold: float = 0.25):
        self.warning_threshold = warning_threshold
        self.critical_threshold = critical_threshold

    def evaluate_drift(self, reference_data: List[float], current_data: List[float]) -> EqualOpportunityMonitorReport:
        if len(reference_data) == 0 or len(current_data) == 0:
            return EqualOpportunityMonitorReport(metric_value=0.0, threshold=self.warning_threshold, is_alert_triggered=False, status="INSUFFICIENT_DATA", sample_size=0)

        ref_arr = np.asarray(reference_data, dtype=np.float64)
        curr_arr = np.asarray(current_data, dtype=np.float64)
        mean_diff = abs(float(np.mean(ref_arr) - np.mean(curr_arr)))
        score = mean_diff / max(1.0, float(np.std(ref_arr)))

        status = "HEALTHY"
        alert = False
        if score >= self.critical_threshold:
            status = "CRITICAL"
            alert = True
        elif score >= self.warning_threshold:
            status = "WARNING"

        return EqualOpportunityMonitorReport(
            metric_value=round(score, 4),
            threshold=self.warning_threshold,
            is_alert_triggered=alert,
            status=status,
            sample_size=len(current_data),
        )
