from celery import Celery
import os, json
from dotenv import load_dotenv
from sqlalchemy import insert, update
from app import models
from app.database import SessionLocal
from app.utils import handle_exception
# from app.websocket.websocket_manager import websocket_manager
from celery import Celery
import os, json
from dotenv import load_dotenv
from sqlalchemy import insert
from app import models
from app.database import SessionLocal
from app.utils import handle_exception
from aio_pika import connect_robust, Message
import logging
from datetime import datetime
from app.validations import Validation
import asyncio, time

# from backend.app.websocket import websocket_manager

load_dotenv()

file_keys = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']

print("os.getenv('CELERY_BACKEND')")



load_dotenv()

celery_app = Celery(
    "celery_tasks",
    broker=f"{os.getenv('CELERY_BROKER')}",
    backend=f"{os.getenv('CELERY_BACKEND')}",
)

@celery_app.task
def process_file(temp_file_path, file_metadata_id):
    
    try:
        db = SessionLocal()
        with open(temp_file_path, 'rb') as file:
            file_content = file.read().decode('utf-8')
        
        # Process the file content as needed
        security_ohlc_prices_dict = json.loads(file_content)
        
        # check if each object is of type json
        for security_ohlc_price_dict in security_ohlc_prices_dict:
            
            validation = Validation(security_ohlc_price_dict)
            validation_result = validation.is_valid(security_ohlc_price_dict)
            
            if not validation_result['valid']:
                logging.error(validation_result['errors'])
                
                for error in validation_result['errors']:
                    send_message_to_websocket_queue.delay(json.dumps({"message":error, "is_valid": False}))
                
                return
            
            else:
                security_ohlc_price_dict['file_metadata_id'] = file_metadata_id
                
        # update the file metadata status to processed
        file_metadata = update(models.FileMetadata).where(models.FileMetadata.id == file_metadata_id).values(is_valid=True)
        db.execute(file_metadata)
        db.commit()
        
        # bulk insert security data   
        query = insert(models.Security).values(security_ohlc_prices_dict)
        db.execute(query)
        db.commit()
        
        send_message_to_websocket_queue.delay(json.dumps({"message":"File Processed", "is_valid": True}))


    except Exception as e:
        handle_exception(e)
    finally:
        # Clean up the temporary file
        db.close()
        os.unlink(temp_file_path)
        print("temp_file_path deleted")
        print("db session closed")
        

async def async_send_message_to_websocket_queue(message):
    try:
        print("Sending message:", message)
        
        # creates a connection to rabbit mq
        connection = await connect_robust("amqp://guest:guest@localhost//")
        async with connection:
            channel = await connection.channel()
            await channel.default_exchange.publish(
                Message(body=message.encode()),
                routing_key='websocket_queue'
            )
    except Exception as e:
        print("Error sending WebSocket message:", e)
        raise e

@celery_app.task
def send_message_to_websocket_queue(message):
    asyncio.run(async_send_message_to_websocket_queue(message))
