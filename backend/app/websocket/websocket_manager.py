from fastapi import WebSocket
import aio_pika
import os

from fastapi import WebSocket
from typing import List

class WebsocketManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    async def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        await websocket.close()

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)
            
    

websocket_manager = WebsocketManager()