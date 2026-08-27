"""
FastAPI Route Handlers for AegisFlow Subsystems
"""

from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException
from backend.core.types import (
    TransactionEvent,
    FraudEvaluationResponse,
    RecommendationRequest,
    RecommendationResponse,
)
from backend.services.fraud_engine.service import fraud_service
from backend.services.fraud_engine.case_manager import fraud_case_manager
from backend.services.rec_engine.service import rec_service
from backend.services.rec_engine.feedback_loop import rec_feedback_processor
from backend.services.feature_store.client import feature_store_client
from backend.services.feature_store.registry import registry
from backend.services.mlops_governance.service import mlops_service
from backend.services.gateway.auth import get_current_user, AuthUser
from backend.core.telemetry import telemetry_manager

router = APIRouter()


@router.post("/fraud/evaluate", response_model=FraudEvaluationResponse, tags=["Fraud Sentinel"])
async def evaluate_fraud(tx: TransactionEvent, user: AuthUser = Depends(get_current_user)):
    return await fraud_service.evaluate_transaction(tx)


@router.get("/fraud/cases", tags=["Fraud Sentinel"])
async def list_fraud_cases(limit: int = 50, user: AuthUser = Depends(get_current_user)):
    return fraud_case_manager.list_open_cases(limit=limit)


@router.post("/fraud/cases/{case_id}/resolve", tags=["Fraud Sentinel"])
async def resolve_fraud_case(
    case_id: str,
    resolution: str,
    notes: str,
    user: AuthUser = Depends(get_current_user),
):
    updated = fraud_case_manager.resolve_case(case_id, user.user_id, resolution, notes)
    if not updated:
        raise HTTPException(status_code=404, detail="Case not found")
    return updated


@router.post("/recommendations/serve", response_model=RecommendationResponse, tags=["Recommendation Engine"])
async def serve_recommendations(req: RecommendationRequest, user: AuthUser = Depends(get_current_user)):
    return await rec_service.get_recommendations(req)


@router.post("/recommendations/feedback", tags=["Recommendation Engine"])
async def record_recommendation_feedback(
    event_type: str,
    item_id: str,
    category: str,
    context: Dict[str, Any] = None,
    user: AuthUser = Depends(get_current_user),
):
    rec_feedback_processor.process_feedback_event(event_type, item_id, category, context or {})
    return {"status": "SUCCESS", "message": "Feedback recorded"}


@router.get("/feature-store/views", tags=["Vortex Feature Store"])
async def list_feature_views(user: AuthUser = Depends(get_current_user)):
    return [fv.model_dump() for fv in registry.list_feature_views()]


@router.post("/feature-store/online-lookup", tags=["Vortex Feature Store"])
async def online_feature_lookup(
    view_name: str,
    entity_keys: List[str],
    user: AuthUser = Depends(get_current_user),
):
    return await feature_store_client.get_online_features(view_name, entity_keys)


@router.get("/mlops/governance-report", tags=["MLOps Governance"])
async def get_governance_report(user: AuthUser = Depends(get_current_user)):
    return mlops_service.get_system_governance_report()


@router.get("/metrics", tags=["Telemetry"])
async def prometheus_metrics():
    return telemetry_manager.export_prometheus_format()
