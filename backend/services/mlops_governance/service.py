"""
MLOps Governance Facade Service
Unifies real-time drift detection, explainability analysis, and cryptographic audit records.
"""

from typing import Dict, Any
from backend.services.mlops_governance.drift_detector import drift_detector
from backend.services.mlops_governance.explainability import shap_explainer
from backend.services.mlops_governance.audit_ledger import audit_ledger


class MLOpsGovernanceService:
    def __init__(self):
        self.drift_detector = drift_detector
        self.shap_explainer = shap_explainer
        self.audit_ledger = audit_ledger

    def get_system_governance_report(self) -> Dict[str, Any]:
        drift_summaries = self.drift_detector.evaluate_all_features()
        integrity = self.audit_ledger.verify_integrity()
        recent_audits = self.audit_ledger.get_recent_blocks(limit=10)

        return {
            "audit_chain_integrity": "VALID" if integrity else "CORRUPTED",
            "total_audit_blocks": len(self.audit_ledger.get_recent_blocks(1000)),
            "feature_drift_reports": [d.model_dump() for d in drift_summaries],
            "recent_audit_events": recent_audits,
        }


mlops_service = MLOpsGovernanceService()
