import asyncio
import json
import logging

from aio_pika import connect_robust
from fastapi import APIRouter, WebSocket
from starlette.websockets import WebSocketDisconnect

from app.websocket.websocket_manager import websocket_manager

router = APIRouter()


async def consume_rabbitmq():
    try:
        connection = await connect_robust("amqp://guest:guest@localhost//")
        async with connection:
            channel = await connection.channel()
            queue = await channel.declare_queue("websocket_queue", durable=True)
            async with queue.iterator() as queue_iter:
                async for message in queue_iter:
                    async with message.process():
                        try:
                            data = json.loads(message.body.decode("utf-8"))
                            print("Received message:", data)
                            await websocket_manager.broadcast(json.dumps(data))
                        except json.JSONDecodeError:
                            print("Received invalid JSON:", message.body)
                        except Exception as e:
                            print(f"Error processing message: {e}")
    except Exception as e:
        logging.error(f"RabbitMQ connection error: {e}")


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    # connect to websocket
    await websocket_manager.connect(websocket)

    # consume from rabbitmq
    rabbitmq_task = asyncio.create_task(consume_rabbitmq())

    # receive data from websocket
    try:
        while True:
            try:
                data = await websocket.receive_text()
                # Process the WebSocket data if needed
                print(f"Received WebSocket message: {data}")
            except WebSocketDisconnect:
                break
    except Exception as e:
        logging.error(f"WebSocket error: {e}")
    finally:
        rabbitmq_task.cancel()
        await websocket_manager.disconnect(websocket)
        print(f"WebSocket connection closed for client")


# @router.post("/testing_websocket")
# def websocket_testing_route(input: dict):
#     try:
#         send_error_message_to_websocket.delay("Hello from Celery!")
#         return {"message": input}
#     except Exception as e:
#         logging.error("Error occurred in websocket_testing_route: %s", e)
# raise HTTPException(status_code=500, detail="Internal Server Error")
