from fastapi import APIRouter, WebSocket
from app.websocket.websocket_manager import websocket_manager

router = APIRouter()

print("websocket_router connected")

# @router.websocket("/analyze")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket_manager.connect(websocket)
#     try:
#         while True:
#             await websocket.receive_text()  # Keep the connection alive
#     except Exception:
#         websocket_manager.disconnect(websocket)

from fastapi import WebSocket
from starlette.websockets import WebSocketDisconnect

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            # Process the received data
            await websocket.send_text(f"You said: {data}")
    except WebSocketDisconnect:
        print("Client disconnected")
    finally:
        # Perform any cleanup if necessary
        print("WebSocket connection closed")