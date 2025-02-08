from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.services.file_service import FileService

file_router = APIRouter(prefix="/api/v1")


@file_router.post("/upload_file")
async def create_file_metadata(
    file: UploadFile,
    db: AsyncSession = Depends(get_db),
):
    file_service = FileService(db)
    return await file_service.save_file_metadata(file)


@file_router.get("/get_file_metadata")
async def get_file_metadata(
    file_service: FileService = Depends(FileService),
):
    return await file_service.get_file_metadata()
