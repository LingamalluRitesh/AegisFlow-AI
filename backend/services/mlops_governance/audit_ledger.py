"""
Immutable Hash-Chained Audit Ledger
Provides cryptographically verifiable audit trails for SOC2, Basel III, and GDPR compliance.
"""

import time
import json
from typing import Dict, Any, List
import threading
from backend.core.crypto import crypto_manager
from backend.core.logging import get_logger

logger = get_logger("mlops.audit")


class CryptographicAuditLedger:
    def __init__(self):
        self._blocks: List[Dict[str, Any]] = []
        self._lock = threading.Lock()
        self._init_genesis_block()

    def _init_genesis_block(self):
        genesis_block = {
            "sequence_index": 0,
            "previous_hash": "0" * 64,
            "timestamp": "2026-01-01T00:00:00Z",
            "event_type": "GENESIS",
            "payload": {"message": "AegisFlow Audit Ledger Initialized"},
            "current_hash": "00000000000000000000aegisflowgenesisrootblockhash20260101000000",
            "signature": crypto_manager.hmac_sign("GENESIS"),
        }
        self._blocks.append(genesis_block)

    def append_event(self, actor_id: str, event_type: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        with self._lock:
            prev_block = self._blocks[-1]
            seq = len(self._blocks)
            ts = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            payload_str = json.dumps(payload, sort_keys=True)

            curr_hash = crypto_manager.compute_audit_hash(
                prev_hash=prev_block["current_hash"],
                timestamp_iso=ts,
                event_type=event_type,
                payload_json=payload_str,
            )
            sig = crypto_manager.hmac_sign(curr_hash)

            block = {
                "sequence_index": seq,
                "previous_hash": prev_block["current_hash"],
                "timestamp": ts,
                "actor_id": actor_id,
                "event_type": event_type,
                "payload": payload,
                "current_hash": curr_hash,
                "signature": sig,
            }
            self._blocks.append(block)
            logger.info_ctx(f"Appended Audit Block #{seq} [{event_type}] Hash: {curr_hash[:12]}...")
            return block

    def verify_integrity(self) -> bool:
        with self._lock:
            for i in range(1, len(self._blocks)):
                curr = self._blocks[i]
                prev = self._blocks[i - 1]

                if curr["previous_hash"] != prev["current_hash"]:
                    return False

                calc_hash = crypto_manager.compute_audit_hash(
                    prev_hash=curr["previous_hash"],
                    timestamp_iso=curr["timestamp"],
                    event_type=curr["event_type"],
                    payload_json=json.dumps(curr["payload"], sort_keys=True),
                )
                if calc_hash != curr["current_hash"]:
                    return False

                if not crypto_manager.hmac_verify(curr["current_hash"], curr["signature"]):
                    return False

            return True

    def get_recent_blocks(self, limit: int = 50) -> List[Dict[str, Any]]:
        with self._lock:
            return list(self._blocks[-limit:])


audit_ledger = CryptographicAuditLedger()
