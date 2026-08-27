"""
AegisFlow AI Core Infrastructure Package
Provides foundational configuration, telemetry, logging, cryptography,
resilience primitives, math utilities, and type schemas.
"""

from backend.core.config import settings, Settings
from backend.core.logging import get_logger, configure_logging
from backend.core.telemetry import telemetry_manager, record_timing
from backend.core.exceptions import (
    AegisFlowException,
    InferenceError,
    FeatureStoreError,
    FraudRuleError,
    StreamProcessingError,
    ModelDriftError,
    AuthenticationError,
    ValidationError
)

__all__ = [
    "settings",
    "Settings",
    "get_logger",
    "configure_logging",
    "telemetry_manager",
    "record_timing",
    "AegisFlowException",
    "InferenceError",
    "FeatureStoreError",
    "FraudRuleError",
    "StreamProcessingError",
    "ModelDriftError",
    "AuthenticationError",
    "ValidationError",
]
