import logging, traceback
from fastapi import HTTPException
from app import models
from sqlalchemy import insert
from fastapi import status
from datetime import datetime


def handle_http_exception(e: HTTPException):
    traceback.print_exc()
    logging.error(f"HTTPException: {e}")
    return {"message": f"{e.detail}", "status_code": e.status_code}

def handle_exception(e: Exception):
    traceback.print_exc()
    logging.error(f"Exception: {e}")
    return {"message": f"{str(e)}", "status_code": 500}


def add_file_metadata(file, db, temp_file_path) -> str:
    
    try:
        
        if file.content_type != "application/json":
            raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail="File type should be .json")
        
        file_size_in_mb = file.size / 1024 / 1024
        
        if file_size_in_mb >= 10:
            raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail="File size should be less than 10MB")
        
        file_size = f"{file_size_in_mb:.2f} MB"
        query = insert(models.FileMetadata).values(file_name=file.filename, file_size=file_size, file_type=file.content_type, upload_date=datetime.now(), file_path=temp_file_path).returning(models.FileMetadata.id)
        result = db.execute(query)
        file_metadata_id = result.fetchone()[0]
        db.commit()
        return file_metadata_id
    
    except HTTPException as e:
        raise e
    except Exception as e:
        handle_exception(e)
        raise e


