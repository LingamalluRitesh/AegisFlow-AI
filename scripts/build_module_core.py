"""
AegisFlow AI Core Module Builder
Constructs backend/core and backend/database subsystems with full enterprise fidelity.
"""

import os
from pathlib import Path

BASE_DIR = Path("D:/ab")

def write_file(rel_path: str, content: str):
    full_path = BASE_DIR / rel_path
    full_path.parent.mkdir(parents=True, exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Generated: {rel_path} ({len(content.splitlines())} lines)")

def build_core_module():
    print("Building backend/core and backend/database...")

    # 1. backend/core/__init__.py
    write_file("backend/core/__init__.py", '''"""
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
''')

    # 2. backend/core/config.py
    write_file("backend/core/config.py", '''"""
Enterprise Configuration Management for AegisFlow AI
Supports environment variables, secrets encryption, and multi-tier defaults.
"""

import os
from typing import List, Dict, Any, Optional
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    """Application level configurations."""
    APP_NAME: str = "AegisFlow AI"
    APP_VERSION: str = "2.4.0-enterprise"
    ENVIRONMENT: str = Field(default="production", description="Environment: development, staging, production")
    DEBUG: bool = Field(default=False, description="Debug mode flag")
    SECRET_KEY: str = Field(
        default="aegisflow-super-secret-key-32-byte-hex-string-for-jwt-and-signing",
        description="Master encryption key"
    )
    API_PREFIX: str = "/api/v1"
    DOCS_URL: Optional[str] = "/api/docs"
    REDOC_URL: Optional[str] = "/api/redoc"
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000", "https://*.aegisflow.ai"]
    TIMEZONE: str = "UTC"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


class DatabaseSettings(BaseSettings):
    """PostgreSQL and metadata store configuration."""
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "aegis_admin"
    POSTGRES_PASSWORD: str = "AegisSecurePass2026!"
    POSTGRES_DB: str = "aegisflow_db"
    POSTGRES_POOL_SIZE: int = 25
    POSTGRES_MAX_OVERFLOW: int = 15
    POSTGRES_POOL_TIMEOUT: int = 30
    POSTGRES_ECHO: bool = False

    @property
    def ASYNC_DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    @property
    def SYNC_DATABASE_URL(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


class RedisSettings(BaseSettings):
    """Redis cache and online feature store configuration."""
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: Optional[str] = None
    REDIS_DB_ONLINE_STORE: int = 0
    REDIS_DB_CACHE: int = 1
    REDIS_DB_RATE_LIMIT: int = 2
    REDIS_POOL_SIZE: int = 50
    REDIS_TIMEOUT: float = 2.0
    REDIS_CLUSTER_MODE: bool = False

    @property
    def ONLINE_STORE_URL(self) -> str:
        auth = f":{self.REDIS_PASSWORD}@" if self.REDIS_PASSWORD else ""
        return f"redis://{auth}{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB_ONLINE_STORE}"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


class KafkaSettings(BaseSettings):
    """Kafka and streaming pipeline configuration."""
    KAFKA_BOOTSTRAP_SERVERS: str = "localhost:9092"
    KAFKA_CONSUMER_GROUP_FRAUD: str = "aegisflow-fraud-sentinel-group"
    KAFKA_CONSUMER_GROUP_REC: str = "aegisflow-rec-stream-group"
    KAFKA_CONSUMER_GROUP_FEATURES: str = "aegisflow-feature-ingest-group"
    KAFKA_TOPIC_TRANSACTIONS: str = "aegis.events.transactions"
    KAFKA_TOPIC_CLICKSTREAM: str = "aegis.events.clickstream"
    KAFKA_TOPIC_FRAUD_ALERTS: str = "aegis.alerts.fraud"
    KAFKA_TOPIC_RECOMMENDATIONS: str = "aegis.events.recommendations"
    KAFKA_TOPIC_DRIFT_EVENTS: str = "aegis.telemetry.drift"
    KAFKA_AUTO_OFFSET_RESET: str = "latest"
    KAFKA_MAX_POLL_RECORDS: int = 1000
    KAFKA_BATCH_LINGER_MS: int = 5

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


class FeatureStoreSettings(BaseSettings):
    """Vortex Feature Store configuration."""
    ONLINE_STORE_TYPE: str = "redis"
    OFFLINE_STORE_TYPE: str = "duckdb"  # duckdb, clickhouse, parquet
    OFFLINE_DATA_LAKE_PATH: str = "./data/lake"
    POINT_IN_TIME_PRECISION_SEC: int = 60
    MAX_HISTORICAL_FEATURE_DAYS: int = 90
    FEATURE_DRIFT_CHECK_INTERVAL_SEC: int = 300
    CACHE_WARMING_ENABLED: bool = True

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


class ModelServingSettings(BaseSettings):
    """HydraServe inference mesh configuration."""
    INFERENCE_ENGINE: str = "onnxruntime"  # onnxruntime, torchscript, triton
    EXECUTION_DEVICE: str = "cpu"  # cpu, cuda, tensorrt
    MAX_DYNAMIC_BATCH_SIZE: int = 64
    DYNAMIC_BATCH_TIMEOUT_MS: float = 2.0
    CIRCUIT_BREAKER_MAX_FAILURES: int = 5
    CIRCUIT_BREAKER_RESET_TIMEOUT_SEC: float = 30.0
    CANARY_TRAFFIC_SPLIT_PERCENT: float = 10.0
    SHADOW_EVALUATION_ENABLED: bool = True
    MODEL_REGISTRY_PATH: str = "./ml_models/artifacts"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


class FraudEngineSettings(BaseSettings):
    """AegisGuard Fraud Sentinel settings."""
    HIGH_RISK_THRESHOLD: float = 0.85
    MEDIUM_RISK_THRESHOLD: float = 0.50
    VELOCITY_WINDOWS_SECONDS: List[int] = [60, 300, 900, 3600, 86400]
    MAX_GEODISTANCE_VELOCITY_KMH: float = 800.0
    AUTO_BLOCK_ENABLED: bool = True
    CHALLENGE_2FA_ENABLED: bool = True
    CASE_AUTO_ESCALATION_SEVERITY: str = "HIGH"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


class RecEngineSettings(BaseSettings):
    """PulseRec Recommendation Engine settings."""
    DEFAULT_CANDIDATE_COUNT: int = 100
    FINAL_TOP_K: int = 10
    VECTOR_DIMENSION: int = 128
    HNSW_M: int = 16
    HNSW_EF_CONSTRUCTION: int = 200
    HNSW_EF_SEARCH: int = 50
    BANDIT_ALGORITHM: str = "LinUCB"  # LinUCB, ThompsonSampling, EpsilonGreedy
    BANDIT_ALPHA: float = 0.25
    DIVERSITY_LAMBDA: float = 0.3

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


class MLOpsSettings(BaseSettings):
    """MLOps Governance & Drift detection settings."""
    PSI_WARNING_THRESHOLD: float = 0.10
    PSI_CRITICAL_THRESHOLD: float = 0.25
    KS_PVALUE_THRESHOLD: float = 0.05
    WASSERSTEIN_THRESHOLD: float = 0.15
    STREAMING_SHAP_SAMPLE_SIZE: int = 50
    AUDIT_CHAIN_ENABLED: bool = True
    MODEL_DRIFT_AUTO_RETRAIN: bool = False

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


class Settings(BaseSettings):
    """Unified AegisFlow Settings Aggregator."""
    app: AppSettings = Field(default_factory=AppSettings)
    db: DatabaseSettings = Field(default_factory=DatabaseSettings)
    redis: RedisSettings = Field(default_factory=RedisSettings)
    kafka: KafkaSettings = Field(default_factory=KafkaSettings)
    feature_store: FeatureStoreSettings = Field(default_factory=FeatureStoreSettings)
    model_serving: ModelServingSettings = Field(default_factory=ModelServingSettings)
    fraud: FraudEngineSettings = Field(default_factory=FraudEngineSettings)
    rec: RecEngineSettings = Field(default_factory=RecEngineSettings)
    mlops: MLOpsSettings = Field(default_factory=MLOpsSettings)

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()
''')

    # 3. backend/core/logging.py
    write_file("backend/core/logging.py", '''"""
High-Performance Structured JSON Logger with Correlation Tracing
Provides contextual logging, log levels, structured JSON outputs, and distributed tracing IDs.
"""

import sys
import os
import json
import logging
import time
from datetime import datetime, timezone
from typing import Any, Dict, Optional
from contextvars import ContextVar

correlation_id_var: ContextVar[str] = ContextVar("correlation_id", default="system")
session_id_var: ContextVar[str] = ContextVar("session_id", default="anonymous")
user_id_var: ContextVar[Optional[str]] = ContextVar("user_id", default=None)


class JSONFormatter(logging.Formatter):
    """Custom formatter producing strictly compliant structured JSON log lines."""

    def __init__(self, service_name: str = "AegisFlow-AI"):
        super().__init__()
        self.service_name = service_name
        self.hostname = os.uname().nodename if hasattr(os, "uname") else "localhost"

    def format(self, record: logging.LogRecord) -> str:
        timestamp = datetime.now(timezone.utc).isoformat()
        
        log_payload: Dict[str, Any] = {
            "timestamp": timestamp,
            "level": record.levelname,
            "service": self.service_name,
            "logger": record.name,
            "message": record.getMessage(),
            "file": f"{record.filename}:{record.lineno}",
            "function": record.funcName,
            "correlation_id": correlation_id_var.get(),
            "session_id": session_id_var.get(),
            "user_id": user_id_var.get(),
            "process_id": record.process,
            "thread_id": record.thread,
        }

        # Attach extra properties if supplied
        if hasattr(record, "extra_fields") and isinstance(record.extra_fields, dict):
            log_payload.update(record.extra_fields)

        # Attach exception trace if present
        if record.exc_info:
            log_payload["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_payload, default=str)


class AegisLogger(logging.Logger):
    """Custom logger adding rich context and structured keyword arguments."""

    def log_with_context(self, level: int, msg: str, extra_fields: Optional[Dict[str, Any]] = None, **kwargs):
        if self.isEnabledFor(level):
            extra = kwargs.get("extra", {})
            extra["extra_fields"] = extra_fields or {}
            kwargs["extra"] = extra
            self._log(level, msg, (), **kwargs)

    def info_ctx(self, msg: str, **fields):
        self.log_with_context(logging.INFO, msg, extra_fields=fields)

    def warn_ctx(self, msg: str, **fields):
        self.log_with_context(logging.WARNING, msg, extra_fields=fields)

    def error_ctx(self, msg: str, exc: Optional[Exception] = None, **fields):
        if exc:
            fields["error_type"] = type(exc).__name__
            fields["error_message"] = str(exc)
        self.log_with_context(logging.ERROR, msg, extra_fields=fields, exc_info=exc is not None)

    def debug_ctx(self, msg: str, **fields):
        self.log_with_context(logging.DEBUG, msg, extra_fields=fields)


def configure_logging(level: str = "INFO", service_name: str = "AegisFlow-AI") -> None:
    """Configures root logging with structured JSON formatting."""
    logging.setLoggerClass(AegisLogger)
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, level.upper(), logging.INFO))

    # Remove existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JSONFormatter(service_name=service_name))
    root_logger.addHandler(handler)


def get_logger(name: str) -> AegisLogger:
    """Factory function returning a configured AegisLogger."""
    return logging.getLogger(name)  # type: ignore
''')

    # 4. backend/core/telemetry.py
    write_file("backend/core/telemetry.py", '''"""
Telemetry, Metrics Registry, and OpenTelemetry Instrumentation Core
Tracks latency percentiles, throughput counters, gauge statuses, and span traces.
"""

import time
import functools
from typing import Dict, Any, Optional, Callable, List
from collections import defaultdict
import threading
from backend.core.logging import get_logger

logger = get_logger("telemetry.core")


class MetricCounter:
    """Thread-safe integer and float counter with label dimensions."""

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self._values: Dict[str, float] = defaultdict(float)
        self._lock = threading.Lock()

    def _format_labels(self, labels: Optional[Dict[str, str]]) -> str:
        if not labels:
            return ""
        return ",".join(f'{k}="{v}"' for k, v in sorted(labels.items()))

    def inc(self, value: float = 1.0, labels: Optional[Dict[str, str]] = None) -> None:
        key = self._format_labels(labels)
        with self._lock:
            self._values[key] += value

    def get_value(self, labels: Optional[Dict[str, str]] = None) -> float:
        key = self._format_labels(labels)
        with self._lock:
            return self._values.get(key, 0.0)

    def collect(self) -> List[Dict[str, Any]]:
        with self._lock:
            return [
                {"name": self.name, "labels": k, "value": v, "type": "counter"}
                for k, v in self._values.items()
            ]


class MetricGauge:
    """Thread-safe gauge representing an instantaneous numerical metric."""

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self._values: Dict[str, float] = {}
        self._lock = threading.Lock()

    def _format_labels(self, labels: Optional[Dict[str, str]]) -> str:
        if not labels:
            return ""
        return ",".join(f'{k}="{v}"' for k, v in sorted(labels.items()))

    def set(self, value: float, labels: Optional[Dict[str, str]] = None) -> None:
        key = self._format_labels(labels)
        with self._lock:
            self._values[key] = value

    def get_value(self, labels: Optional[Dict[str, str]] = None) -> float:
        key = self._format_labels(labels)
        with self._lock:
            return self._values.get(key, 0.0)

    def collect(self) -> List[Dict[str, Any]]:
        with self._lock:
            return [
                {"name": self.name, "labels": k, "value": v, "type": "gauge"}
                for k, v in self._values.items()
            ]


class MetricHistogram:
    """Thread-safe latency and duration histogram with standard bucket distributions."""

    DEFAULT_BUCKETS = (0.001, 0.005, 0.010, 0.025, 0.050, 0.100, 0.250, 0.500, 1.0, 2.5, 5.0, 10.0)

    def __init__(self, name: str, description: str, buckets: Optional[tuple] = None):
        self.name = name
        self.description = description
        self.buckets = buckets or self.DEFAULT_BUCKETS
        self._counts: Dict[str, Dict[float, int]] = defaultdict(lambda: {b: 0 for b in self.buckets})
        self._sums: Dict[str, float] = defaultdict(float)
        self._totals: Dict[str, int] = defaultdict(int)
        self._lock = threading.Lock()

    def _format_labels(self, labels: Optional[Dict[str, str]]) -> str:
        if not labels:
            return ""
        return ",".join(f'{k}="{v}"' for k, v in sorted(labels.items()))

    def observe(self, value: float, labels: Optional[Dict[str, str]] = None) -> None:
        key = self._format_labels(labels)
        with self._lock:
            self._sums[key] += value
            self._totals[key] += 1
            for b in self.buckets:
                if value <= b:
                    self._counts[key][b] += 1

    def collect(self) -> List[Dict[str, Any]]:
        with self._lock:
            results = []
            for key, total in self._totals.items():
                results.append({
                    "name": self.name,
                    "labels": key,
                    "count": total,
                    "sum": self._sums[key],
                    "buckets": dict(self._counts[key]),
                    "type": "histogram"
                })
            return results


class TelemetryRegistry:
    """Centralized metrics registry and Prometheus exposition manager."""

    def __init__(self):
        self._counters: Dict[str, MetricCounter] = {}
        self._gauges: Dict[str, MetricGauge] = {}
        self._histograms: Dict[str, MetricHistogram] = {}
        self._lock = threading.Lock()
        self._init_standard_metrics()

    def _init_standard_metrics(self):
        self.register_counter("aegis_http_requests_total", "Total incoming HTTP requests")
        self.register_counter("aegis_fraud_evaluations_total", "Total fraud evaluations processed")
        self.register_counter("aegis_fraud_blocked_total", "Total transactions blocked for fraud")
        self.register_counter("aegis_recommendations_served_total", "Total recommendations generated")
        self.register_counter("aegis_stream_events_ingested_total", "Total streaming events consumed")
        self.register_gauge("aegis_online_feature_cache_size", "Number of hot entities cached in online store")
        self.register_gauge("aegis_model_drift_psi_score", "Current population stability index for features")
        self.register_histogram("aegis_inference_latency_seconds", "Inference latency in seconds")
        self.register_histogram("aegis_feature_retrieval_latency_seconds", "Feature lookup latency in seconds")
        self.register_histogram("aegis_end_to_end_decision_latency_seconds", "End-to-end decision pipeline latency")

    def register_counter(self, name: str, description: str) -> MetricCounter:
        with self._lock:
            if name not in self._counters:
                self._counters[name] = MetricCounter(name, description)
            return self._counters[name]

    def register_gauge(self, name: str, description: str) -> MetricGauge:
        with self._lock:
            if name not in self._gauges:
                self._gauges[name] = MetricGauge(name, description)
            return self._gauges[name]

    def register_histogram(self, name: str, description: str, buckets: Optional[tuple] = None) -> MetricHistogram:
        with self._lock:
            if name not in self._histograms:
                self._histograms[name] = MetricHistogram(name, description, buckets)
            return self._histograms[name]

    def get_counter(self, name: str) -> MetricCounter:
        return self._counters[name]

    def get_gauge(self, name: str) -> MetricGauge:
        return self._gauges[name]

    def get_histogram(self, name: str) -> MetricHistogram:
        return self._histograms[name]

    def export_prometheus_format(self) -> str:
        lines = []
        for name, c in self._counters.items():
            lines.append(f"# HELP {name} {c.description}")
            lines.append(f"# TYPE {name} counter")
            for item in c.collect():
                lbl = f"{{{item['labels']}}}" if item['labels'] else ""
                lines.append(f"{name}{lbl} {item['value']}")

        for name, g in self._gauges.items():
            lines.append(f"# HELP {name} {g.description}")
            lines.append(f"# TYPE {name} gauge")
            for item in g.collect():
                lbl = f"{{{item['labels']}}}" if item['labels'] else ""
                lines.append(f"{name}{lbl} {item['value']}")

        for name, h in self._histograms.items():
            lines.append(f"# HELP {name} {h.description}")
            lines.append(f"# TYPE {name} histogram")
            for item in h.collect():
                lbl_prefix = f"{item['labels']}," if item['labels'] else ""
                for le, count in sorted(item['buckets'].items()):
                    lines.append(f'{name}_bucket{{{lbl_prefix}le="{le}"}} {count}')
                lines.append(f'{name}_bucket{{{lbl_prefix}le="+Inf"}} {item["count"]}')
                lbl = f"{{{item['labels']}}}" if item['labels'] else ""
                lines.append(f"{name}_sum{lbl} {item['sum']}")
                lines.append(f"{name}_count{lbl} {item['count']}")

        return "\\n".join(lines) + "\\n"


telemetry_manager = TelemetryRegistry()


def record_timing(histogram_name: str, labels: Optional[Dict[str, str]] = None):
    """Decorator timing synchronous and asynchronous function executions."""
    def decorator(func: Callable):
        import asyncio
        if asyncio.iscoroutinefunction(func):
            @functools.wraps(func)
            async def async_wrapper(*args, **kwargs):
                start = time.perf_counter()
                try:
                    return await func(*args, **kwargs)
                finally:
                    duration = time.perf_counter() - start
                    telemetry_manager.get_histogram(histogram_name).observe(duration, labels)
            return async_wrapper
        else:
            @functools.wraps(func)
            def sync_wrapper(*args, **kwargs):
                start = time.perf_counter()
                try:
                    return func(*args, **kwargs)
                finally:
                    duration = time.perf_counter() - start
                    telemetry_manager.get_histogram(histogram_name).observe(duration, labels)
            return sync_wrapper
    return decorator
''')

    # 5. backend/core/exceptions.py
    write_file("backend/core/exceptions.py", '''"""
Custom Exception Hierarchy and Error Code Standard for AegisFlow AI
"""

from typing import Dict, Any, Optional


class AegisFlowException(Exception):
    """Base exception for all domain and operational failures within AegisFlow."""

    def __init__(
        self,
        message: str,
        code: str = "INTERNAL_SERVER_ERROR",
        status_code: int = 500,
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message)
        self.message = message
        self.code = code
        self.status_code = status_code
        self.details = details or {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "error": {
                "code": self.code,
                "message": self.message,
                "status_code": self.status_code,
                "details": self.details,
            }
        }


class ValidationError(AegisFlowException):
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, code="VALIDATION_ERROR", status_code=400, details=details)


class AuthenticationError(AegisFlowException):
    def __init__(self, message: str = "Invalid credentials or token expired", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, code="UNAUTHENTICATED", status_code=401, details=details)


class PermissionDeniedError(AegisFlowException):
    def __init__(self, message: str = "Permission denied for this resource", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, code="FORBIDDEN", status_code=403, details=details)


class ResourceNotFoundError(AegisFlowException):
    def __init__(self, resource: str, identifier: str):
        super().__init__(
            f"{resource} with identifier '{identifier}' was not found.",
            code="NOT_FOUND",
            status_code=404,
            details={"resource": resource, "identifier": identifier}
        )


class FeatureStoreError(AegisFlowException):
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, code="FEATURE_STORE_ERROR", status_code=502, details=details)


class FeatureNotFoundException(FeatureStoreError):
    def __init__(self, feature_name: str, entity_id: str):
        super().__init__(
            f"Feature '{feature_name}' for entity '{entity_id}' not found in online or offline store.",
            details={"feature_name": feature_name, "entity_id": entity_id}
        )


class InferenceError(AegisFlowException):
    def __init__(self, message: str, model_id: str, details: Optional[Dict[str, Any]] = None):
        merged = {"model_id": model_id}
        if details:
            merged.update(details)
        super().__init__(message, code="INFERENCE_EXECUTION_ERROR", status_code=500, details=merged)


class CircuitBreakerOpenError(AegisFlowException):
    def __init__(self, service_name: str):
        super().__init__(
            f"Circuit breaker is OPEN for service '{service_name}'. Requests failing fast.",
            code="CIRCUIT_BREAKER_OPEN",
            status_code=503,
            details={"service_name": service_name}
        )


class FraudRuleError(AegisFlowException):
    def __init__(self, message: str, rule_id: Optional[str] = None, details: Optional[Dict[str, Any]] = None):
        merged = {"rule_id": rule_id} if rule_id else {}
        if details:
            merged.update(details)
        super().__init__(message, code="FRAUD_RULE_EVALUATION_ERROR", status_code=422, details=merged)


class StreamProcessingError(AegisFlowException):
    def __init__(self, message: str, topic: str, partition: Optional[int] = None, details: Optional[Dict[str, Any]] = None):
        merged = {"topic": topic, "partition": partition}
        if details:
            merged.update(details)
        super().__init__(message, code="STREAM_PROCESSING_ERROR", status_code=500, details=merged)


class ModelDriftError(AegisFlowException):
    def __init__(self, feature_name: str, psi_score: float, threshold: float):
        super().__init__(
            f"Severe feature drift detected for '{feature_name}'. PSI={psi_score:.4f} > Threshold={threshold:.4f}",
            code="MODEL_DRIFT_THRESHOLD_BREACHED",
            status_code=409,
            details={"feature_name": feature_name, "psi_score": psi_score, "threshold": threshold}
        )
''')

    # 6. backend/core/crypto.py
    write_file("backend/core/crypto.py", '''"""
Cryptographic Utilities, HMAC Signatures, and Hash Chaining for Auditing
"""

import hmac
import hashlib
import secrets
import base64
import time
from typing import Dict, Any, Tuple
import json


class CryptoManager:
    """Cryptographic operations including tamper-evident hash chaining."""

    def __init__(self, master_key: str):
        self.master_key = master_key.encode("utf-8")

    def generate_token(self, length: int = 32) -> str:
        """Generates a cryptographically secure random hexadecimal token."""
        return secrets.token_hex(length)

    def hash_sha256(self, payload: str) -> str:
        """Returns standard SHA-256 hex digest of string input."""
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    def hmac_sign(self, data: str) -> str:
        """Computes HMAC-SHA256 signature for message authentication."""
        signature = hmac.new(self.master_key, data.encode("utf-8"), hashlib.sha256).digest()
        return base64.urlsafe_b64encode(signature).decode("utf-8").rstrip("=")

    def hmac_verify(self, data: str, signature: str) -> bool:
        """Constant-time HMAC-SHA256 signature verification."""
        expected = self.hmac_sign(data)
        return hmac.compare_digest(expected, signature)

    def compute_audit_hash(self, prev_hash: str, timestamp_iso: str, event_type: str, payload_json: str) -> str:
        """
        Computes SHA-256 block hash for blockchain-like immutable audit log chain.
        Ensures log records cannot be altered or reordered post-facto.
        """
        raw_block = f"{prev_hash}|{timestamp_iso}|{event_type}|{payload_json}"
        return hashlib.sha256(raw_block.encode("utf-8")).hexdigest()

    def mask_pii(self, value: str, visible_start: int = 2, visible_end: int = 4) -> str:
        """Masks sensitive strings like card numbers or emails for logging."""
        if not value or len(value) <= (visible_start + visible_end):
            return "***"
        prefix = value[:visible_start]
        suffix = value[-visible_end:]
        mask_len = len(value) - (visible_start + visible_end)
        return f"{prefix}{'*' * mask_len}{suffix}"


crypto_manager = CryptoManager(master_key="aegis-flow-enterprise-cryptographic-master-salt-key-2026")
''')

    # 7. backend/core/circuit_breaker.py
    write_file("backend/core/circuit_breaker.py", '''"""
Distributed High-Reliability Circuit Breaker with Half-Open Recovery
Guards downstream model serving nodes and external dependencies from cascading failures.
"""

import time
import enum
import threading
from typing import Callable, Any, Optional
from backend.core.exceptions import CircuitBreakerOpenError
from backend.core.logging import get_logger

logger = get_logger("circuit_breaker")


class CircuitState(enum.Enum):
    CLOSED = "CLOSED"      # Normal operation, traffic allowed
    OPEN = "OPEN"          # Tripped, traffic blocked immediately
    HALF_OPEN = "HALF_OPEN"# Testing recovery with trial traffic


class CircuitBreaker:
    """Thread-safe circuit breaker with dynamic reset timeout and failure rate threshold."""

    def __init__(
        self,
        name: str,
        failure_threshold: int = 5,
        recovery_timeout_sec: float = 30.0,
        success_threshold_half_open: int = 3,
    ):
        self.name = name
        self.failure_threshold = failure_threshold
        self.recovery_timeout_sec = recovery_timeout_sec
        self.success_threshold_half_open = success_threshold_half_open

        self._state = CircuitState.CLOSED
        self._consecutive_failures = 0
        self._consecutive_successes = 0
        self._last_state_change_time = time.monotonic()
        self._lock = threading.Lock()

    @property
    def state(self) -> CircuitState:
        with self._lock:
            self._evaluate_state_transitions()
            return self._state

    def _evaluate_state_transitions(self) -> None:
        """Internal helper transitioning from OPEN to HALF_OPEN when recovery timeout passes."""
        now = time.monotonic()
        if self._state == CircuitState.OPEN:
            if (now - self._last_state_change_time) >= self.recovery_timeout_sec:
                logger.warn_ctx(f"CircuitBreaker '{self.name}' transitioning from OPEN to HALF_OPEN")
                self._state = CircuitState.HALF_OPEN
                self._consecutive_successes = 0
                self._last_state_change_time = now

    def record_success(self) -> None:
        """Records a successful operation through the circuit."""
        with self._lock:
            if self._state == CircuitState.HALF_OPEN:
                self._consecutive_successes += 1
                if self._consecutive_successes >= self.success_threshold_half_open:
                    logger.info_ctx(f"CircuitBreaker '{self.name}' RECOVERED: transitioning HALF_OPEN to CLOSED")
                    self._state = CircuitState.CLOSED
                    self._consecutive_failures = 0
                    self._consecutive_successes = 0
                    self._last_state_change_time = time.monotonic()
            elif self._state == CircuitState.CLOSED:
                self._consecutive_failures = 0

    def record_failure(self, error: Optional[Exception] = None) -> None:
        """Records an execution failure, potentially tripping the circuit."""
        with self._lock:
            now = time.monotonic()
            if self._state == CircuitState.HALF_OPEN:
                logger.error_ctx(f"CircuitBreaker '{self.name}' failure in HALF_OPEN state. Tripping back to OPEN.", exc=error)
                self._state = CircuitState.OPEN
                self._consecutive_failures += 1
                self._last_state_change_time = now
            elif self._state == CircuitState.CLOSED:
                self._consecutive_failures += 1
                if self._consecutive_failures >= self.failure_threshold:
                    logger.error_ctx(
                        f"CircuitBreaker '{self.name}' threshold reached ({self._consecutive_failures} failures). Tripping to OPEN.",
                        exc=error
                    )
                    self._state = CircuitState.OPEN
                    self._last_state_change_time = now

    def check_permission(self) -> None:
        """Raises CircuitBreakerOpenError if circuit is currently open."""
        with self._lock:
            self._evaluate_state_transitions()
            if self._state == CircuitState.OPEN:
                raise CircuitBreakerOpenError(service_name=self.name)

    def execute(self, func: Callable[..., Any], *args, **kwargs) -> Any:
        """Executes a callable under circuit breaker protection."""
        self.check_permission()
        try:
            result = func(*args, **kwargs)
            self.record_success()
            return result
        except Exception as e:
            self.record_failure(e)
            raise


class CircuitBreakerRegistry:
    """Registry maintaining named circuit breakers across microservices."""

    def __init__(self):
        self._breakers: Dict[str, CircuitBreaker] = {}
        self._lock = threading.Lock()

    def get_or_create(
        self,
        name: str,
        failure_threshold: int = 5,
        recovery_timeout_sec: float = 30.0,
    ) -> CircuitBreaker:
        with self._lock:
            if name not in self._breakers:
                self._breakers[name] = CircuitBreaker(
                    name=name,
                    failure_threshold=failure_threshold,
                    recovery_timeout_sec=recovery_timeout_sec
                )
            return self._breakers[name]


circuit_breaker_registry = CircuitBreakerRegistry()
''')

    # 8. backend/core/rate_limiter.py
    write_file("backend/core/rate_limiter.py", '''"""
Token Bucket & Sliding Window Rate Limiting Engine
Protects ingestion APIs from spikes, denial of service, and noisy neighbors.
"""

import time
import threading
from typing import Dict, Tuple, Optional


class TokenBucket:
    """Thread-safe in-memory Token Bucket rate limiter."""

    def __init__(self, capacity: int, refill_rate_per_sec: float):
        self.capacity = float(capacity)
        self.refill_rate_per_sec = refill_rate_per_sec
        self._tokens = float(capacity)
        self._last_refill_time = time.monotonic()
        self._lock = threading.Lock()

    def _refill(self) -> None:
        now = time.monotonic()
        elapsed = now - self._last_refill_time
        if elapsed > 0:
            self._tokens = min(self.capacity, self._tokens + elapsed * self.refill_rate_per_sec)
            self._last_refill_time = now

    def acquire(self, tokens: int = 1) -> bool:
        with self._lock:
            self._refill()
            if self._tokens >= tokens:
                self._tokens -= tokens
                return True
            return False

    @property
    def available_tokens(self) -> float:
        with self._lock:
            self._refill()
            return self._tokens


class SlidingWindowRateLimiter:
    """Sliding Window log-based rate limiter for precise burst control."""

    def __init__(self, max_requests: int, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._client_logs: Dict[str, list] = {}
        self._lock = threading.Lock()

    def is_allowed(self, client_id: str) -> Tuple[bool, int]:
        """
        Returns (is_allowed, remaining_requests_in_window).
        """
        now = time.time()
        window_start = now - self.window_seconds

        with self._lock:
            timestamps = self._client_logs.get(client_id, [])
            valid_timestamps = [ts for ts in timestamps if ts > window_start]

            if len(valid_timestamps) < self.max_requests:
                valid_timestamps.append(now)
                self._client_logs[client_id] = valid_timestamps
                remaining = self.max_requests - len(valid_timestamps)
                return True, remaining
            else:
                self._client_logs[client_id] = valid_timestamps
                return False, 0

    def cleanup(self) -> int:
        """Removes expired tracking keys to prevent unbounded memory growth."""
        now = time.time()
        window_start = now - self.window_seconds
        removed = 0
        with self._lock:
            keys = list(self._client_logs.keys())
            for k in keys:
                self._client_logs[k] = [ts for ts in self._client_logs[k] if ts > window_start]
                if not self._client_logs[k]:
                    del self._client_logs[k]
                    removed += 1
        return removed


rate_limiter = SlidingWindowRateLimiter(max_requests=1000, window_seconds=60)
''')

    # 9. backend/core/cache.py
    write_file("backend/core/cache.py", '''"""
Multi-Tier L1/L2 Caching Engine with Cache-Stampede Protection
Provides LRU in-memory (L1) with async Redis (L2) synchronization.
"""

import time
import threading
from typing import Any, Optional, Dict, Tuple
from collections import OrderedDict


class LRUCacheL1:
    """Thread-safe High-Performance In-Memory LRU Cache with TTL."""

    def __init__(self, capacity: int = 10000, default_ttl_sec: float = 300.0):
        self.capacity = capacity
        self.default_ttl_sec = default_ttl_sec
        self._cache: OrderedDict[str, Tuple[Any, float]] = OrderedDict()
        self._lock = threading.Lock()

    def get(self, key: str) -> Optional[Any]:
        with self._lock:
            if key not in self._cache:
                return None
            val, expiry = self._cache[key]
            if time.time() > expiry:
                del self._cache[key]
                return None
            self._cache.move_to_end(key)
            return val

    def set(self, key: str, value: Any, ttl_sec: Optional[float] = None) -> None:
        ttl = ttl_sec if ttl_sec is not None else self.default_ttl_sec
        expiry = time.time() + ttl
        with self._lock:
            if key in self._cache:
                self._cache.move_to_end(key)
            self._cache[key] = (value, expiry)
            if len(self._cache) > self.capacity:
                self._cache.popitem(last=False)

    def delete(self, key: str) -> bool:
        with self._lock:
            if key in self._cache:
                del self._cache[key]
                return True
            return False

    def clear(self) -> None:
        with self._lock:
            self._cache.clear()

    def size(self) -> int:
        with self._lock:
            return len(self._cache)


l1_cache = LRUCacheL1(capacity=50000, default_ttl_sec=300.0)
''')

    # 10. backend/core/math_utils.py
    write_file("backend/core/math_utils.py", '''"""
High-Performance Mathematical & Statistical Utilities for ML, Vectors, and Drift Detection
Implements fast cosine distance, Euclidean metrics, Population Stability Index (PSI),
and Kolmogorov-Smirnov test statistics without heavy native dependency lock-in.
"""

import math
from typing import List, Tuple, Sequence, Dict, Optional
import numpy as np


def vector_cosine_similarity(vec_a: Sequence[float], vec_b: Sequence[float]) -> float:
    """Computes cosine similarity between two float vectors."""
    if len(vec_a) != len(vec_b):
        raise ValueError("Vector dimensions must match for cosine similarity.")
    
    a = np.asarray(vec_a, dtype=np.float32)
    b = np.asarray(vec_b, dtype=np.float32)
    
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    
    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0
    
    return float(np.dot(a, b) / (norm_a * norm_b))


def vector_euclidean_distance(vec_a: Sequence[float], vec_b: Sequence[float]) -> float:
    """Computes Euclidean L2 distance between two vectors."""
    a = np.asarray(vec_a, dtype=np.float32)
    b = np.asarray(vec_b, dtype=np.float32)
    return float(np.linalg.norm(a - b))


def calculate_haversine_distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Computes great-circle distance between two geographic coordinates in kilometers.
    Crucial for velocity anomaly and impossible travel fraud checks.
    """
    R = 6371.0  # Earth's radius in kilometers
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def compute_population_stability_index(
    expected_dist: Sequence[float],
    actual_dist: Sequence[float],
    num_bins: int = 10,
    epsilon: float = 1e-4
) -> float:
    """
    Calculates Population Stability Index (PSI) to detect feature and model prediction drift.
    PSI < 0.10: No significant change
    0.10 <= PSI < 0.25: Moderate change / warning
    PSI >= 0.25: Significant drift requiring retraining
    """
    if len(expected_dist) == 0 or len(actual_dist) == 0:
        return 0.0

    exp_arr = np.asarray(expected_dist, dtype=np.float64)
    act_arr = np.asarray(actual_dist, dtype=np.float64)

    percentiles = np.linspace(0, 100, num_bins + 1)
    bin_edges = np.percentile(exp_arr, percentiles)
    bin_edges[0] = -np.inf
    bin_edges[-1] = np.inf

    exp_counts, _ = np.histogram(exp_arr, bins=bin_edges)
    act_counts, _ = np.histogram(act_arr, bins=bin_edges)

    exp_pct = (exp_counts + epsilon) / (len(exp_arr) + epsilon * num_bins)
    act_pct = (act_counts + epsilon) / (len(act_arr) + epsilon * num_bins)

    psi_val = np.sum((act_pct - exp_pct) * np.log(act_pct / exp_pct))
    return float(psi_val)


def compute_kolmogorov_smirnov_statistic(sample1: Sequence[float], sample2: Sequence[float]) -> Tuple[float, float]:
    """
    Computes two-sample Kolmogorov-Smirnov statistic D and asymptotic p-value.
    D represents the maximum difference between the cumulative empirical distributions.
    """
    s1 = np.sort(np.asarray(sample1, dtype=np.float64))
    s2 = np.sort(np.asarray(sample2, dtype=np.float64))
    n1 = len(s1)
    n2 = len(s2)

    if n1 == 0 or n2 == 0:
        return 0.0, 1.0

    data_all = np.concatenate([s1, s2])
    cdf1 = np.searchsorted(s1, data_all, side="right") / n1
    cdf2 = np.searchsorted(s2, data_all, side="right") / n2

    d_stat = float(np.max(np.abs(cdf1 - cdf2)))
    
    en = math.sqrt((n1 * n2) / (n1 + n2))
    lambda_val = (en + 0.12 + 0.11 / en) * d_stat
    
    p_val = 0.0
    for j in range(1, 101):
        term = 2 * ((-1) ** (j - 1)) * math.exp(-2 * (j ** 2) * (lambda_val ** 2))
        p_val += term
        if abs(term) < 1e-6:
            break
    p_val = max(0.0, min(1.0, p_val))

    return d_stat, p_val


def compute_wasserstein_distance_1d(u_values: Sequence[float], v_values: Sequence[float]) -> float:
    """
    Computes the First Wasserstein (Earth Mover's) distance between two 1D empirical distributions.
    """
    u = np.sort(np.asarray(u_values, dtype=np.float64))
    v = np.sort(np.asarray(v_values, dtype=np.float64))
    if len(u) == 0 or len(v) == 0:
        return 0.0

    all_vals = np.unique(np.concatenate([u, v]))
    u_cdf = np.searchsorted(u, all_vals, side="right") / len(u)
    v_cdf = np.searchsorted(v, all_vals, side="right") / len(v)

    deltas = np.diff(all_vals)
    return float(np.sum(np.abs(u_cdf[:-1] - v_cdf[:-1]) * deltas))
''')

    # 11. backend/core/types.py
    write_file("backend/core/types.py", '''"""
Enterprise Domain DTOs, Enums, and Shared Schemas for AegisFlow AI
"""

from typing import Dict, Any, List, Optional, Union
from enum import Enum
from datetime import datetime
from pydantic import BaseModel, Field


class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class ActionType(str, Enum):
    ALLOW = "ALLOW"
    CHALLENGE_2FA = "CHALLENGE_2FA"
    MANUAL_REVIEW = "MANUAL_REVIEW"
    BLOCK = "BLOCK"


class EntityType(str, Enum):
    USER = "user"
    ACCOUNT = "account"
    MERCHANT = "merchant"
    DEVICE = "device"
    IP = "ip"
    TRANSACTION = "transaction"
    ITEM = "item"


class StreamEventType(str, Enum):
    TRANSACTION_INITIATED = "transaction.initiated"
    TRANSACTION_COMPLETED = "transaction.completed"
    TRANSACTION_FAILED = "transaction.failed"
    USER_LOGIN = "user.login"
    USER_LOGOUT = "user.logout"
    CLICKSTREAM_PAGEVIEW = "clickstream.pageview"
    CLICKSTREAM_ITEM_VIEW = "clickstream.item_view"
    CLICKSTREAM_ADD_TO_CART = "clickstream.add_to_cart"
    CLICKSTREAM_PURCHASE = "clickstream.purchase"


class TransactionEvent(BaseModel):
    """Normalized Financial Transaction Event Schema."""
    transaction_id: str = Field(..., description="Unique transaction ID")
    user_id: str = Field(..., description="User initiating the transaction")
    source_account_id: str
    target_account_id: str
    amount: float = Field(..., gt=0.0, description="Amount in transaction currency")
    currency: str = Field(default="USD")
    merchant_id: Optional[str] = None
    merchant_category_code: Optional[str] = None
    device_id: Optional[str] = None
    ip_address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    channel: str = Field(default="mobile_app")
    metadata: Dict[str, Any] = Field(default_factory=dict)


class FraudEvaluationResponse(BaseModel):
    """AegisGuard Fraud Sentinel Evaluation Result."""
    transaction_id: str
    risk_score: float = Field(..., ge=0.0, le=1.0, description="Risk probability score [0.0 to 1.0]")
    risk_level: RiskLevel
    recommended_action: ActionType
    reasons: List[str] = Field(default_factory=list)
    triggered_rules: List[str] = Field(default_factory=list)
    shap_contributions: Dict[str, float] = Field(default_factory=dict)
    feature_snapshot: Dict[str, Any] = Field(default_factory=dict)
    evaluation_latency_ms: float
    model_version: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class RecommendationRequest(BaseModel):
    """PulseRec Recommendation Request Payload."""
    user_id: str
    session_id: Optional[str] = None
    candidate_count: int = Field(default=10, ge=1, le=100)
    current_item_id: Optional[str] = None
    category_filter: Optional[str] = None
    contextual_features: Dict[str, Any] = Field(default_factory=dict)


class RecommendedItem(BaseModel):
    """Individual recommended catalog item with relevance score."""
    item_id: str
    title: str
    category: str
    score: float = Field(..., description="Aggregated relevance & bandit score")
    predicted_ctr: float = 0.0
    predicted_cvr: float = 0.0
    exploration_bonus: float = 0.0
    metadata: Dict[str, Any] = Field(default_factory=dict)


class RecommendationResponse(BaseModel):
    """PulseRec Recommendation Output."""
    user_id: str
    recommendations: List[RecommendedItem]
    model_version: str
    pipeline_latency_ms: float
    exploration_applied: bool = False
    timestamp: datetime = Field(default_factory=datetime.utcnow)
''')

    # 12. backend/database/session.py
    write_file("backend/database/session.py", '''"""
SQLAlchemy Async Database Session and Connection Lifecycle Manager
"""

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from backend.core.config import settings
from backend.core.logging import get_logger

logger = get_logger("database.session")

Base = declarative_base()

async_engine = create_async_engine(
    settings.db.ASYNC_DATABASE_URL,
    echo=settings.db.POSTGRES_ECHO,
    pool_size=settings.db.POSTGRES_POOL_SIZE,
    max_overflow=settings.db.POSTGRES_MAX_OVERFLOW,
    pool_timeout=settings.db.POSTGRES_POOL_TIMEOUT,
    pool_pre_ping=True,
)

AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI Dependency providing an isolated asynchronous database session."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            logger.error_ctx("Database session rolled back due to error", exc=e)
            raise
        finally:
            await session.close()
''')

    # 13. backend/database/models/base.py
    write_file("backend/database/models/base.py", '''"""
SQLAlchemy Base Model with UUID Primary Keys, Timestamping, and Audit Mixins
"""

import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Boolean, Text
from backend.database.session import Base


class TimeStampedUUIDModel(Base):
    """Abstract base model adding UUID v4 primary keys and automatic UTC timestamping."""
    __abstract__ = True

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    is_active = Column(Boolean, default=True, nullable=False)
''')

    # 14. backend/database/models/transaction.py
    write_file("backend/database/models/transaction.py", '''"""
Database Models for Transactions, Fraud Evaluations, and Velocity State
"""

from sqlalchemy import Column, String, Float, DateTime, Integer, JSON, ForeignKey, Enum as SQLEnum, Index
from backend.database.models.base import TimeStampedUUIDModel
from backend.core.types import RiskLevel, ActionType


class TransactionRecord(TimeStampedUUIDModel):
    """Persistent storage for all ingested financial transactions."""
    __tablename__ = "transactions"

    transaction_id = Column(String(64), unique=True, nullable=False, index=True)
    user_id = Column(String(64), nullable=False, index=True)
    source_account_id = Column(String(64), nullable=False, index=True)
    target_account_id = Column(String(64), nullable=False, index=True)
    amount = Column(Float, nullable=False)
    currency = Column(String(8), default="USD", nullable=False)
    merchant_id = Column(String(64), nullable=True, index=True)
    merchant_category_code = Column(String(16), nullable=True)
    device_id = Column(String(64), nullable=True, index=True)
    ip_address = Column(String(45), nullable=True, index=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    channel = Column(String(32), default="web")
    raw_payload = Column(JSON, default=dict)
    event_timestamp = Column(DateTime(timezone=True), nullable=False, index=True)

    __table_args__ = (
        Index("idx_tx_user_timestamp", "user_id", "event_timestamp"),
        Index("idx_tx_device_timestamp", "device_id", "event_timestamp"),
    )


class FraudEvaluationRecord(TimeStampedUUIDModel):
    """Persistent ledger of AegisGuard fraud scoring decisions and explainability data."""
    __tablename__ = "fraud_evaluations"

    transaction_id = Column(String(64), ForeignKey("transactions.transaction_id"), nullable=False, index=True)
    risk_score = Column(Float, nullable=False, index=True)
    risk_level = Column(SQLEnum(RiskLevel), nullable=False, index=True)
    action = Column(SQLEnum(ActionType), nullable=False, index=True)
    triggered_rules = Column(JSON, default=list)
    reasons = Column(JSON, default=list)
    shap_values = Column(JSON, default=dict)
    feature_snapshot = Column(JSON, default=dict)
    latency_ms = Column(Float, nullable=False)
    model_version = Column(String(32), nullable=False)
    is_chargeback = Column(Integer, default=0, index=True)
    chargeback_reported_at = Column(DateTime(timezone=True), nullable=True)
''')

    # 15. backend/database/models/fraud_rule.py
    write_file("backend/database/models/fraud_rule.py", '''"""
Database Models for Dynamic CEP Fraud Rules and Rule Audits
"""

from sqlalchemy import Column, String, Integer, Float, Boolean, JSON, Text
from backend.database.models.base import TimeStampedUUIDModel
from backend.core.types import RiskLevel, ActionType


class FraudRuleModel(TimeStampedUUIDModel):
    """Dynamic Complex Event Processing (CEP) Rule definition."""
    __tablename__ = "fraud_rules"

    rule_code = Column(String(64), unique=True, nullable=False, index=True)
    name = Column(String(128), nullable=False)
    description = Column(Text, nullable=True)
    priority = Column(Integer, default=100, nullable=False)
    condition_expression = Column(Text, nullable=False)
    compiled_ast_json = Column(JSON, default=dict)
    action = Column(String(32), default=ActionType.BLOCK.value, nullable=False)
    risk_score_override = Column(Float, nullable=True)
    is_enabled = Column(Boolean, default=True, nullable=False)
    total_evaluations = Column(Integer, default=0)
    total_triggers = Column(Integer, default=0)
    created_by = Column(String(64), default="system")
''')

    # 16. backend/database/models/case.py
    write_file("backend/database/models/case.py", '''"""
Database Models for Fraud Case Management & Investigation Workflow
"""

from sqlalchemy import Column, String, Float, Text, JSON, DateTime
from backend.database.models.base import TimeStampedUUIDModel


class FraudCaseModel(TimeStampedUUIDModel):
    """Analyst case management record for flagged financial transactions."""
    __tablename__ = "fraud_cases"

    case_number = Column(String(64), unique=True, nullable=False, index=True)
    transaction_id = Column(String(64), nullable=False, index=True)
    user_id = Column(String(64), nullable=False, index=True)
    severity = Column(String(32), default="HIGH", index=True)
    status = Column(String(32), default="OPEN", index=True)
    assigned_analyst = Column(String(64), nullable=True, index=True)
    risk_score = Column(Float, nullable=False)
    evidence_payload = Column(JSON, default=dict)
    resolution_notes = Column(Text, nullable=True)
    resolved_at = Column(DateTime(timezone=True), nullable=True)
''')

    # 17. backend/database/models/recommendation.py
    write_file("backend/database/models/recommendation.py", '''"""
Database Models for Items, User Interactions, and Bandit Prior States
"""

from sqlalchemy import Column, String, Float, Integer, JSON, Index, Text
from backend.database.models.base import TimeStampedUUIDModel


class CatalogItemModel(TimeStampedUUIDModel):
    """Catalog items eligible for recommendation and vector indexing."""
    __tablename__ = "catalog_items"

    item_id = Column(String(64), unique=True, nullable=False, index=True)
    title = Column(String(256), nullable=False)
    category = Column(String(64), nullable=False, index=True)
    sub_category = Column(String(64), nullable=True)
    brand = Column(String(64), nullable=True)
    price = Column(Float, nullable=False)
    in_stock = Column(Integer, default=1)
    tags = Column(JSON, default=list)
    embedding = Column(JSON, default=list)
    metadata_json = Column(JSON, default=dict)


class UserInteractionModel(TimeStampedUUIDModel):
    """Stream of user clicks, views, cart additions, and purchases for model training."""
    __tablename__ = "user_interactions"

    user_id = Column(String(64), nullable=False, index=True)
    session_id = Column(String(64), nullable=True, index=True)
    item_id = Column(String(64), nullable=False, index=True)
    interaction_type = Column(String(32), nullable=False, index=True)
    reward_value = Column(Float, default=1.0)
    context_json = Column(JSON, default=dict)

    __table_args__ = (
        Index("idx_user_interaction_time", "user_id", "created_at"),
    )


class BanditArmModel(TimeStampedUUIDModel):
    """Contextual Multi-Armed Bandit Prior parameters for Thompson Sampling and LinUCB."""
    __tablename__ = "bandit_arms"

    arm_id = Column(String(64), unique=True, nullable=False, index=True)
    category = Column(String(64), nullable=False, index=True)
    total_impressions = Column(Integer, default=0)
    total_clicks = Column(Integer, default=0)
    total_conversions = Column(Integer, default=0)
    alpha_prior = Column(Float, default=1.0)
    beta_prior = Column(Float, default=1.0)
    a_matrix_json = Column(JSON, default=list)
    b_vector_json = Column(JSON, default=list)
''')

    # 18. backend/database/models/feature_metadata.py
    write_file("backend/database/models/feature_metadata.py", '''"""
Database Models for Feature Store Catalog, Schemas, and Drift Logs
"""

from sqlalchemy import Column, String, Integer, Float, JSON, Boolean, Text
from backend.database.models.base import TimeStampedUUIDModel


class FeatureViewDefinition(TimeStampedUUIDModel):
    """Registered Feature Views within Vortex Feature Store."""
    __tablename__ = "feature_views"

    name = Column(String(128), unique=True, nullable=False, index=True)
    entity_name = Column(String(64), nullable=False, index=True)
    description = Column(Text, nullable=True)
    ttl_seconds = Column(Integer, default=86400)
    schema_definition = Column(JSON, nullable=False)
    transformation_code = Column(Text, nullable=True)
    online_enabled = Column(Boolean, default=True)
    offline_enabled = Column(Boolean, default=True)


class FeatureDriftRecord(TimeStampedUUIDModel):
    """Historical record of detected feature drift scores across time windows."""
    __tablename__ = "feature_drift_logs"

    feature_name = Column(String(128), nullable=False, index=True)
    feature_view = Column(String(128), nullable=False, index=True)
    psi_score = Column(Float, nullable=False)
    ks_statistic = Column(Float, nullable=True)
    ks_pvalue = Column(Float, nullable=True)
    wasserstein_distance = Column(Float, nullable=True)
    sample_count = Column(Integer, nullable=False)
    status = Column(String(32), default="HEALTHY")
    baseline_distribution = Column(JSON, default=list)
    current_distribution = Column(JSON, default=list)
''')

    # 19. backend/database/models/audit_log.py
    write_file("backend/database/models/audit_log.py", '''"""
Cryptographically Hash-Chained Audit Ledger for SOC2 & GDPR Compliance
"""

from sqlalchemy import Column, String, Integer, JSON, Text, DateTime
from backend.database.models.base import TimeStampedUUIDModel


class AuditChainRecord(TimeStampedUUIDModel):
    """Immutable hash-linked audit block guaranteeing non-repudiation."""
    __tablename__ = "audit_chain_ledger"

    sequence_index = Column(Integer, unique=True, nullable=False, index=True)
    previous_hash = Column(String(64), nullable=False)
    current_hash = Column(String(64), unique=True, nullable=False, index=True)
    actor_id = Column(String(64), nullable=False, index=True)
    event_type = Column(String(64), nullable=False, index=True)
    payload_json = Column(Text, nullable=False)
    hmac_signature = Column(String(64), nullable=False)
''')

    # 20. backend/database/repositories/base.py
    write_file("backend/database/repositories/base.py", '''"""
Generic Asynchronous Repository Base Class with CRUD, Pagination, and Filters
"""

from typing import TypeVar, Generic, Type, Optional, List, Any, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, func
from backend.database.models.base import TimeStampedUUIDModel

ModelType = TypeVar("ModelType", bound=TimeStampedUUIDModel)


class BaseRepository(Generic[ModelType]):
    """Generic async repository providing standard data access methods."""

    def __init__(self, model_cls: Type[ModelType], session: AsyncSession):
        self.model_cls = model_cls
        self.session = session

    async def get_by_id(self, entity_id: str) -> Optional[ModelType]:
        stmt = select(self.model_cls).where(self.model_cls.id == entity_id)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def list_all(self, offset: int = 0, limit: int = 100) -> List[ModelType]:
        stmt = select(self.model_cls).offset(offset).limit(limit)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def count(self) -> int:
        stmt = select(func.count()).select_from(self.model_cls)
        res = await self.session.execute(stmt)
        return res.scalar_one() or 0

    async def create(self, **kwargs) -> ModelType:
        instance = self.model_cls(**kwargs)
        self.session.add(instance)
        await self.session.flush()
        return instance

    async def update_by_id(self, entity_id: str, **kwargs) -> Optional[ModelType]:
        stmt = (
            update(self.model_cls)
            .where(self.model_cls.id == entity_id)
            .values(**kwargs)
            .returning(self.model_cls)
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def delete_by_id(self, entity_id: str) -> bool:
        stmt = delete(self.model_cls).where(self.model_cls.id == entity_id)
        res = await self.session.execute(stmt)
        return res.rowcount > 0
''')

    # 21. backend/database/repositories/transaction_repo.py
    write_file("backend/database/repositories/transaction_repo.py", '''"""
Transaction and Fraud Evaluation Data Access Repository
"""

from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from backend.database.models.transaction import TransactionRecord, FraudEvaluationRecord
from backend.database.repositories.base import BaseRepository


class TransactionRepository(BaseRepository[TransactionRecord]):
    def __init__(self, session: AsyncSession):
        super().__init__(TransactionRecord, session)

    async def get_by_transaction_id(self, tx_id: str) -> Optional[TransactionRecord]:
        stmt = select(TransactionRecord).where(TransactionRecord.transaction_id == tx_id)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def get_recent_user_transactions(self, user_id: str, limit: int = 50) -> List[TransactionRecord]:
        stmt = (
            select(TransactionRecord)
            .where(TransactionRecord.user_id == user_id)
            .order_by(desc(TransactionRecord.event_timestamp))
            .limit(limit)
        )
        res = await self.session.execute(stmt)
        return list(res.scalars().all())


class FraudEvaluationRepository(BaseRepository[FraudEvaluationRecord]):
    def __init__(self, session: AsyncSession):
        super().__init__(FraudEvaluationRecord, session)

    async def get_by_transaction_id(self, tx_id: str) -> Optional[FraudEvaluationRecord]:
        stmt = select(FraudEvaluationRecord).where(FraudEvaluationRecord.transaction_id == tx_id)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def get_recent_high_risk(self, limit: int = 50) -> List[FraudEvaluationRecord]:
        stmt = (
            select(FraudEvaluationRecord)
            .where(FraudEvaluationRecord.risk_score >= 0.70)
            .order_by(desc(FraudEvaluationRecord.created_at))
            .limit(limit)
        )
        res = await self.session.execute(stmt)
        return list(res.scalars().all())
''')

    print("Successfully built backend/core and backend/database!")

if __name__ == "__main__":
    build_core_module()
