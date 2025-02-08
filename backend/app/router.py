# import logging
# import os
# import shutil
# from tempfile import NamedTemporaryFile

# from fastapi import APIRouter, Depends, HTTPException, UploadFile, status
# from sqlalchemy import insert, select
# from sqlalchemy.orm import Session

# from app import models
# from app.database import get_db
# from app.tasks.celery_tasks import process_file
# from app.utils import (
#     add_file_metadata,
#     convert_date_format,
#     handle_exception,
#     handle_http_exception,
# )

# router = APIRouter(prefix="/api/v1")


# # @router.post("/upload_file")
# # def create_file_metadata(file: UploadFile, db: Session = Depends(get_db)):
# #     try:

# #         # Create a named temporary file
# #         with NamedTemporaryFile(delete=False, suffix=".json") as temp_file:

# #             # Copy the file content to the temporary file
# #             shutil.copyfileobj(file.file, temp_file)
# #             temp_file_path = temp_file.name

# #         logging.info(f"Temporary file created at: {temp_file_path}")
# #         logging.info(
# #             f"Temporary file size: {os.path.getsize(temp_file_path) / 1024 / 1024:.2f} MB"
# #         )

# #         file_metadata_id = add_file_metadata(file, db, temp_file_path)

# #         # Send the path of the temporary file to the Celery task
# #         process_file.delay(temp_file_path, file_metadata_id)

# #         return {
# #             "message": "File upload complete, processing started.",
# #             "temp_file_path": temp_file_path,
# #         }

# #     except HTTPException as e:
# #         return handle_http_exception(e)
# #     except Exception as e:
# #         return handle_exception(e)


# @router.get("/get_file_metadata")
# def get_file_metadata(db: Session = Depends(get_db)):
#     try:
#         query = select(models.FileMetadata)
#         result = db.execute(query)
#         file_metadata = result.scalars().fetchall()

#         if not file_metadata:
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND, detail="File metadata not found"
#             )

#         return file_metadata
#     except HTTPException as e:
#         return handle_http_exception(e)
#     except Exception as e:
#         return handle_exception(e)


# @router.get("/get_security_data")
# def get_security_data(file_metadata_id: int, db: Session = Depends(get_db)):
#     try:
#         query = select(models.Security).where(
#             models.Security.file_metadata_id == file_metadata_id
#         )
#         result = db.execute(query)
#         security_data = result.scalars().fetchall()

#         modified_data = [
#             {
#                 "c": security.Close,
#                 "o": security.Open,
#                 "h": security.High,
#                 "l": security.Low,
#                 "x": convert_date_format(security.Date),
#             }
#             for security in security_data
#         ]

#         if not security_data:
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND, detail="Security data not found"
#             )

#         return modified_data
#     except HTTPException as e:
#         return handle_http_exception(e)
#     except Exception as e:
#         return handle_exception(e)
