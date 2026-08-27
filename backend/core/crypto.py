"""
Cryptographic Utilities, HMAC Signatures, and Hash Chaining for Auditing
"""

import hmac
import hashlib
import secrets
import base64
import time
from typing import Dict, Any, Tuple
import json


class CryptoManager:
    """Cryptographic operations including tamper-evident hash chaining."""

    def __init__(self, master_key: str):
        self.master_key = master_key.encode("utf-8")

    def generate_token(self, length: int = 32) -> str:
        """Generates a cryptographically secure random hexadecimal token."""
        return secrets.token_hex(length)

    def hash_sha256(self, payload: str) -> str:
        """Returns standard SHA-256 hex digest of string input."""
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    def hmac_sign(self, data: str) -> str:
        """Computes HMAC-SHA256 signature for message authentication."""
        signature = hmac.new(self.master_key, data.encode("utf-8"), hashlib.sha256).digest()
        return base64.urlsafe_b64encode(signature).decode("utf-8").rstrip("=")

    def hmac_verify(self, data: str, signature: str) -> bool:
        """Constant-time HMAC-SHA256 signature verification."""
        expected = self.hmac_sign(data)
        return hmac.compare_digest(expected, signature)

    def compute_audit_hash(self, prev_hash: str, timestamp_iso: str, event_type: str, payload_json: str) -> str:
        """
        Computes SHA-256 block hash for blockchain-like immutable audit log chain.
        Ensures log records cannot be altered or reordered post-facto.
        """
        raw_block = f"{prev_hash}|{timestamp_iso}|{event_type}|{payload_json}"
        return hashlib.sha256(raw_block.encode("utf-8")).hexdigest()

    def mask_pii(self, value: str, visible_start: int = 2, visible_end: int = 4) -> str:
        """Masks sensitive strings like card numbers or emails for logging."""
        if not value or len(value) <= (visible_start + visible_end):
            return "***"
        prefix = value[:visible_start]
        suffix = value[-visible_end:]
        mask_len = len(value) - (visible_start + visible_end)
        return f"{prefix}{'*' * mask_len}{suffix}"


crypto_manager = CryptoManager(master_key="aegis-flow-enterprise-cryptographic-master-salt-key-2026")
