from celery import Celery
import os, json
from dotenv import load_dotenv
from sqlalchemy import insert
from app import models
from app.database import SessionLocal
from app.utils import handle_exception

load_dotenv()

file_keys = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']

print("os.getenv('CELERY_BACKEND')")
celery_app = Celery(
    "celery_tasks",
    broker=f"{os.getenv('CELERY_BROKER')}",
    backend=f"{os.getenv('CELERY_BACKEND')}",
)

@celery_app.task
def process_file(temp_file_path, file_metadata_id):
    print("temp_file_path:", temp_file_path)
    
    try:
        db = SessionLocal()
        with open(temp_file_path, 'rb') as file:
            file_content = file.read().decode('utf-8')
            
        # Process the file content as needed
        security_ohlc_prices_dict = json.loads(file_content)
        
        for security_ohlc_price_dict in security_ohlc_prices_dict:
            security_ohlc_price_dict['file_metadata_id'] = file_metadata_id
        
        # bulk insert security data   
        query = insert(models.Security).values(
            security_ohlc_prices_dict
        )
        db.execute(query)
        db.commit()

    except Exception as e:
        handle_exception(e)
    finally:
        # Clean up the temporary file
        db.close()
        os.unlink(temp_file_path)
        print("temp_file_path deleted")
        print("db session closed")
    
    
    

            
            

import os
import json

# @celery_app.task
# def process_file(temp_file_path):
#     print("temp_file_path:", temp_file_path)
    
#     try:
#         if not os.path.exists(temp_file_path):
#             print(f"File does not exist: {temp_file_path}")
#             return
        
#         file_size = os.path.getsize(temp_file_path)
#         print(f"File size in Celery task: {file_size} bytes")
        
#         with open(temp_file_path, 'rb') as file:
#             file_content = file.read()
        
#         print(f"Read {len(file_content)} bytes from the file")
        
#         # Try to decode and parse as JSON
#         try:
#             decoded_content = file_content.decode('utf-8')
#             latest_file_content = json.loads(decoded_content)
#             print("Successfully parsed JSON content")
#             print(f"Number of top-level items in JSON: {len(latest_file_content)}")
#         except json.JSONDecodeError as json_error:
#             print(f"Error decoding JSON: {json_error}")
#             print(f"First 100 characters of content: {decoded_content[:100]}")
        
#         # Your processing logic here
#         for item in latest_file_content:
#             print(item)
        
#         # Clean up the temporary file
#         os.unlink(temp_file_path)

#     except Exception as e:
#         print(f"Error processing file: {e}")


