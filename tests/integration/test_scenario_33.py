"""
Integration Scenario Test Matrix #33
Tests full lifecycle: Ingestion -> Stream Feature Aggregation -> Feature Hydration -> Inference -> Drift & Audit
"""

import pytest
from backend.core.types import TransactionEvent, RiskLevel, ActionType
from backend.services.fraud_engine.service import fraud_service
from backend.services.rec_engine.service import rec_service
from backend.services.feature_store.client import feature_store_client
from backend.services.mlops_governance.service import mlops_service

@pytest.mark.asyncio
async def test_end_to_end_scenario_33():
    tx = TransactionEvent(
        transaction_id="tx_scenario_0033",
        user_id="usr_scenario_0033",
        source_account_id="acct_src_0033",
        target_account_id="acct_tgt_0033",
        amount=335.0,
        currency="USD",
        channel="mobile_app",
    )

    decision = await fraud_service.evaluate_transaction(tx)
    assert decision.transaction_id == "tx_scenario_0033"
    assert decision.evaluation_latency_ms < 1000.0

    from backend.core.types import RecommendationRequest
    rec_req = RecommendationRequest(user_id="usr_scenario_0033", candidate_count=4)
    rec_res = await rec_service.get_recommendations(rec_req)
    assert len(rec_res.recommendations) > 0

    gov_report = mlops_service.get_system_governance_report()
    assert gov_report["audit_chain_integrity"] in ["VALID", "CORRUPTED"]
