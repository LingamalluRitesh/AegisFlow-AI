"""
High-Performance Structured JSON Logger with Correlation Tracing
Provides contextual logging, log levels, structured JSON outputs, and distributed tracing IDs.
"""

import sys
import os
import json
import logging
import time
from datetime import datetime, timezone
from typing import Any, Dict, Optional
from contextvars import ContextVar

correlation_id_var: ContextVar[str] = ContextVar("correlation_id", default="system")
session_id_var: ContextVar[str] = ContextVar("session_id", default="anonymous")
user_id_var: ContextVar[Optional[str]] = ContextVar("user_id", default=None)


class JSONFormatter(logging.Formatter):
    """Custom formatter producing strictly compliant structured JSON log lines."""

    def __init__(self, service_name: str = "AegisFlow-AI"):
        super().__init__()
        self.service_name = service_name
        self.hostname = os.uname().nodename if hasattr(os, "uname") else "localhost"

    def format(self, record: logging.LogRecord) -> str:
        timestamp = datetime.now(timezone.utc).isoformat()
        
        log_payload: Dict[str, Any] = {
            "timestamp": timestamp,
            "level": record.levelname,
            "service": self.service_name,
            "logger": record.name,
            "message": record.getMessage(),
            "file": f"{record.filename}:{record.lineno}",
            "function": record.funcName,
            "correlation_id": correlation_id_var.get(),
            "session_id": session_id_var.get(),
            "user_id": user_id_var.get(),
            "process_id": record.process,
            "thread_id": record.thread,
        }

        # Attach extra properties if supplied
        if hasattr(record, "extra_fields") and isinstance(record.extra_fields, dict):
            log_payload.update(record.extra_fields)

        # Attach exception trace if present
        if record.exc_info:
            log_payload["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_payload, default=str)


class AegisLogger(logging.Logger):
    """Custom logger adding rich context and structured keyword arguments."""

    def log_with_context(self, level: int, msg: str, extra_fields: Optional[Dict[str, Any]] = None, **kwargs):
        if self.isEnabledFor(level):
            extra = kwargs.get("extra", {})
            extra["extra_fields"] = extra_fields or {}
            kwargs["extra"] = extra
            self._log(level, msg, (), **kwargs)

    def info_ctx(self, msg: str, **fields):
        self.log_with_context(logging.INFO, msg, extra_fields=fields)

    def warn_ctx(self, msg: str, **fields):
        self.log_with_context(logging.WARNING, msg, extra_fields=fields)

    def error_ctx(self, msg: str, exc: Optional[Exception] = None, **fields):
        if exc:
            fields["error_type"] = type(exc).__name__
            fields["error_message"] = str(exc)
        self.log_with_context(logging.ERROR, msg, extra_fields=fields, exc_info=exc is not None)

    def debug_ctx(self, msg: str, **fields):
        self.log_with_context(logging.DEBUG, msg, extra_fields=fields)


logging.setLoggerClass(AegisLogger)


def configure_logging(level: str = "INFO", service_name: str = "AegisFlow-AI") -> None:
    """Configures root logging with structured JSON formatting."""
    logging.setLoggerClass(AegisLogger)
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, level.upper(), logging.INFO))

    # Remove existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JSONFormatter(service_name=service_name))
    root_logger.addHandler(handler)


def get_logger(name: str) -> AegisLogger:
    """Factory function returning a configured AegisLogger."""
    logging.setLoggerClass(AegisLogger)
    return logging.getLogger(name)  # type: ignore

