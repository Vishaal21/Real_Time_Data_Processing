import logging
import os
from typing import Tuple

from aiofiles import tempfile
from celery_files.tasks.process_security_json_data import (
    process_json_data,
    send_message_to_websocket_queue,
)
from fastapi import Depends, HTTPException, UploadFile, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.repos.file_repo import FileRepo


class FileService:
    def __init__(self, db):
        self.db = db
        self.file_repo = FileRepo()

    async def save_file_metadata(
        self,
        file: UploadFile,
    ) -> JSONResponse:
        if not await self.is_valid_json_file(file):
            raise HTTPException(
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                detail="File type should be .json",
            )

        file_size, file_size_str = await self.file_size_in_mb(file)
        if file_size >= 10:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail="File size should be less than 10MB",
            )

        temp_file_path = await self.create_temporary_file(file)
        file_id = await self.file_repo.create_file_metadata(
            self.db, file, temp_file_path, file_size_str
        )

        # process the file content
        process_json_data.delay(temp_file_path, file_id)

        return JSONResponse(
            content={
                "message": "File upload complete, processing started.",
                "temp_file_path": temp_file_path,
            },
            status_code=status.HTTP_200_OK,
        )

    async def is_valid_json_file(self, file: UploadFile) -> bool:
        # Check both content type and file extension
        content_type = file.content_type
        valid_content_types = ["application/json", "text/json"]
        valid_extension = os.path.splitext(file.filename)[1].lower() == ".json"
        return content_type in valid_content_types and valid_extension

    async def create_temporary_file(self, file: UploadFile) -> str:
        try:
            async with tempfile.NamedTemporaryFile(
                "wb", delete=False, suffix=".json"
            ) as temp_file:
                content = await file.read()  # Async read
                await temp_file.write(content)  # Async write
                temp_file_path = temp_file.name

            logging.info(f"Temporary file created: {temp_file_path}")
            return temp_file_path
        finally:
            await file.close()

    async def file_size_in_mb(self, file: UploadFile) -> Tuple[float, str]:
        file_size = file.size / (1024 * 1024)
        return file_size, f"{file_size:.2f} MB"

    async def get_file_type(self, file: UploadFile) -> str:
        return file.content_type

    async def get_file_metadata(self):
        return await self.file_repo.get_file_metadata()
