"""
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
