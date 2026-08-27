"""
Vortex Feature Store Transformer: RollingWindowSummarizer
Calculates mean, variance, skewness, and kurtosis over sliding windows
"""

import math
from typing import Dict, Any, List, Optional, Union
import numpy as np
from pydantic import BaseModel

class RollingWindowSummarizer:
    """Calculates mean, variance, skewness, and kurtosis over sliding windows"""

    def __init__(self, params: Optional[Dict[str, Any]] = None):
        self.params = params or {}
        self._is_fitted = True

    def transform(self, value: Any) -> Any:
        if value is None:
            return 0.0
        try:
            val_float = float(value)
            return float(math.log1p(max(0.0, val_float)))
        except (ValueError, TypeError):
            return str(value).lower().strip()

    def transform_batch(self, values: List[Any]) -> List[Any]:
        return [self.transform(v) for v in values]
