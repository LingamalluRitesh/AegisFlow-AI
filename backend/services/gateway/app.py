"""
FastAPI Application Entrypoint
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from backend.core.config import settings
from backend.core.logging import configure_logging
from backend.services.gateway.routes import router
from backend.services.gateway.websocket import ws_manager


def create_app() -> FastAPI:
    configure_logging(level="INFO", service_name="AegisFlow-Gateway")

    application = FastAPI(
        title=settings.app.APP_NAME,
        version=settings.app.APP_VERSION,
        docs_url=settings.app.DOCS_URL,
        redoc_url=settings.app.REDOC_URL,
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.include_router(router, prefix=settings.app.API_PREFIX)

    @application.websocket("/ws/telemetry")
    async def websocket_telemetry_endpoint(websocket: WebSocket):
        await ws_manager.connect(websocket)
        try:
            while True:
                data = await websocket.receive_text()
                await websocket.send_text(f'{"type":"pong","received":{data}}')
        except WebSocketDisconnect:
            ws_manager.disconnect(websocket)

    @application.get("/health")
    async def health_check():
        return {"status": "HEALTHY", "service": settings.app.APP_NAME, "version": settings.app.APP_VERSION}

    return application


app = create_app()
