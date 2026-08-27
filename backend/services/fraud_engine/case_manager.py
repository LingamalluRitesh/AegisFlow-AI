"""
Fraud Case Management Workflow Subsystem
Tracks suspicious alerts, investigator assignments, and resolution notes.
"""

import time
import uuid
from typing import Dict, Any, List, Optional
import threading
from backend.core.logging import get_logger

logger = get_logger("fraud.case_manager")


class CaseManager:
    def __init__(self):
        self._cases: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.Lock()

    def create_case(
        self,
        transaction_id: str,
        user_id: str,
        risk_score: float,
        severity: str,
        evidence: Dict[str, Any],
    ) -> Dict[str, Any]:
        case_id = f"CASE-{str(uuid.uuid4())[:8].upper()}"
        case_entry = {
            "case_id": case_id,
            "transaction_id": transaction_id,
            "user_id": user_id,
            "risk_score": risk_score,
            "severity": severity,
            "status": "OPEN",
            "assigned_analyst": None,
            "evidence": evidence,
            "created_at": time.time(),
            "resolved_at": None,
            "resolution_notes": None,
        }
        with self._lock:
            self._cases[case_id] = case_entry

        logger.info_ctx(f"Created Fraud Case [{case_id}] for transaction {transaction_id} (Risk: {risk_score:.2f})")
        return case_entry

    def list_open_cases(self, limit: int = 50) -> List[Dict[str, Any]]:
        with self._lock:
            return [c for c in self._cases.values() if c["status"] == "OPEN"][:limit]

    def resolve_case(self, case_id: str, analyst_id: str, resolution: str, notes: str) -> Optional[Dict[str, Any]]:
        with self._lock:
            if case_id in self._cases:
                self._cases[case_id]["status"] = resolution
                self._cases[case_id]["assigned_analyst"] = analyst_id
                self._cases[case_id]["resolved_at"] = time.time()
                self._cases[case_id]["resolution_notes"] = notes
                return self._cases[case_id]
            return None


fraud_case_manager = CaseManager()
