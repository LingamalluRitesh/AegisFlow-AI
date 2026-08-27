"""
AegisFlow API Gateway & Ingestion Mesh
FastAPI routing, JWT authentication, rate limiting, and real-time WebSockets.
"""

from backend.services.gateway.app import create_app, app

__all__ = ["create_app", "app"]
