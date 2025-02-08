import asyncio
import json
import os

from celery_files.config import celery_app
from dotenv import load_dotenv
from kombu import Connection, Exchange, Producer, Queue

from app.database import get_sync_db
from app.utils import handle_exception
from app.validations import SecurityDictListValidation

file_keys = ["Date", "Open", "High", "Low", "Close", "Volume"]

load_dotenv()


@celery_app.task(name="process_json_data")
def process_json_data(temp_file_path, file_metadata_id):
    try:
        with open(temp_file_path, "rb") as file:
            file_content = file.read().decode("utf-8")

        security_ohlc_prices_dict_list = json.loads(file_content)

        # Process the security ohlc json
        security_dict_list_validation = SecurityDictListValidation(
            security_ohlc_prices_dict_list, file_metadata_id
        )
        security_dict_list_validation.is_security_data_valid()

        # update the file metadata status to processed
        from app.repos.file_repo import FileRepo
        from app.repos.security_repo import insert_security_ohlc_prices

        with get_sync_db() as db:
            file_repo = FileRepo()
            file_repo.update_file_metadata(db, file_metadata_id, temp_file_path, True)
            insert_security_ohlc_prices(db, security_ohlc_prices_dict_list)

        # send message to websocket queue
        send_message_to_websocket_queue.delay(
            json.dumps({"message": "File Processed", "is_valid": True})
        )

    except Exception as e:
        handle_exception(e)
    finally:
        # Clean up the temporary file
        os.unlink(temp_file_path)
        print("temp_file_path deleted")
        print("db session closed")


@celery_app.task(name="send_message_to_websocket_queue")
def send_message_to_websocket_queue(message):
    try:
        print("Sending message:", message)

        with Connection("pyamqp://guest:guest@localhost//") as conn:
            channel = conn.channel()
            producer = Producer(channel)
            producer.publish(
                message,
                exchange=Exchange(""),
                routing_key="websocket_queue",
                serializer="json",
                delivery_mode=2,
            )

        print("Message sent successfully!")

    except Exception as e:
        print("Error sending WebSocket message:", e)
        raise e
