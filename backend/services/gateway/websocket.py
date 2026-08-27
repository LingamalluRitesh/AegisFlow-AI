"""
Real-Time WebSocket Hub for Live Transaction Feeds and Topology Graphs
"""

from typing import List
from fastapi import WebSocket
import json
from backend.core.logging import get_logger

logger = get_logger("gateway.websocket")


class WebSocketConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info_ctx("WebSocket client connected")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            logger.info_ctx("WebSocket client disconnected")

    async def broadcast(self, message_dict: dict):
        payload = json.dumps(message_dict)
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_text(payload)
            except Exception:
                disconnected.append(connection)
        for d in disconnected:
            self.disconnect(d)


ws_manager = WebSocketConnectionManager()
