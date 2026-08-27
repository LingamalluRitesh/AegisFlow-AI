"""
AegisFlow AI Top-Level Application Ingress
Direct ASGI entry point for production deployments (Uvicorn, Gunicorn, Hypercorn).
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.services.gateway.app import app

# Export application for ASGI web servers
__all__ = ["app"]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
