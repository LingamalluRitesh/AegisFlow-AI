"""
HydraServe Model Registry & Artifact Catalog
Tracks active model versions, target input/output signatures, metrics, and deployment status.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from backend.core.logging import get_logger

logger = get_logger("serving.registry")


class ModelMetadata(BaseModel):
    model_id: str
    version: str
    framework: str
    input_schema: Dict[str, str]
    output_schema: Dict[str, str]
    artifact_path: str
    is_active: bool = True
    canary_weight: float = 0.0
    created_at: datetime = Field(default_factory=datetime.utcnow)
    performance_metrics: Dict[str, float] = Field(default_factory=dict)


class ModelRegistry:
    def __init__(self):
        self._models: Dict[str, Dict[str, ModelMetadata]] = {}
        self._init_default_models()

    def _init_default_models(self):
        fraud_meta = ModelMetadata(
            model_id="aegisguard-fraud-detector",
            version="v2.4.0",
            framework="onnx",
            input_schema={"features": "float32[batch, 15]"},
            output_schema={"probabilities": "float32[batch, 2]"},
            artifact_path="./ml_models/artifacts/fraud_gnn_v2_4.onnx",
            performance_metrics={"auc_roc": 0.984, "latency_p99_ms": 3.2},
        )
        rec_meta = ModelMetadata(
            model_id="pulserec-dlrm-ranker",
            version="v2.4.0",
            framework="onnx",
            input_schema={"user_embedding": "float32[batch, 128]", "item_embedding": "float32[batch, 128]"},
            output_schema={"score": "float32[batch, 1]"},
            artifact_path="./ml_models/artifacts/pulserec_dlrm_v2_4.onnx",
            performance_metrics={"ndcg_at_10": 0.892, "latency_p99_ms": 4.1},
        )
        self.register_model(fraud_meta)
        self.register_model(rec_meta)

    def register_model(self, meta: ModelMetadata) -> None:
        if meta.model_id not in self._models:
            self._models[meta.model_id] = {}
        self._models[meta.model_id][meta.version] = meta
        logger.info_ctx(f"Registered Model [{meta.model_id}:{meta.version}] ({meta.framework})")

    def get_latest_version(self, model_id: str) -> Optional[ModelMetadata]:
        if model_id in self._models and self._models[model_id]:
            versions = sorted(self._models[model_id].keys())
            return self._models[model_id][versions[-1]]
        return None

    def get_model(self, model_id: str, version: str) -> Optional[ModelMetadata]:
        return self._models.get(model_id, {}).get(version)


model_registry = ModelRegistry()
