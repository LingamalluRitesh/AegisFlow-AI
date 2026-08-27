import pytest
from backend.services.mlops_governance.drift_detector import drift_detector
from backend.services.mlops_governance.explainability import shap_explainer
from backend.services.mlops_governance.audit_ledger import audit_ledger


def test_audit_ledger_hash_chain():
    b1 = audit_ledger.append_event("admin", "CONFIG_CHANGE", {"key": "threshold", "val": 0.85})
    assert b1["sequence_index"] > 0
    assert audit_ledger.verify_integrity() is True


def test_streaming_shap_values():
    shap_dict = shap_explainer.compute_local_shap_values({"amount": 1500.0, "tx_count_5m": 6})
    assert "amount" in shap_dict
    assert "tx_count_5m" in shap_dict
    assert shap_dict["amount"] > 0.0
