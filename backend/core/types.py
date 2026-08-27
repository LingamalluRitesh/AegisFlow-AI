"""
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
