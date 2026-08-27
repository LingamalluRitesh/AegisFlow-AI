"""
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
