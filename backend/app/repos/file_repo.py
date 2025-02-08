from datetime import datetime

from fastapi import Depends, UploadFile
from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.db_schemas import FileMetadata


class FileRepo:
    async def create_file_metadata(
        self, db, file: UploadFile, temp_file_path: str, file_size_str: str
    ):
        insert_query = (
            insert(FileMetadata)
            .values(
                file_name=file.filename,
                file_size=file_size_str,
                file_type=file.content_type,
                upload_date=datetime.now().date(),
                file_path=temp_file_path,
            )
            .returning(FileMetadata.id)
        )

        result = await db.execute(insert_query)
        await db.commit()
        return result.scalar()

    async def get_file_metadata(self, db, file_metadata_id):
        query = select(FileMetadata).where(FileMetadata.id == file_metadata_id)
        result = await db.execute(query)
        return result.scalar()

    def update_file_metadata(
        self, db, file_metadata_id: int, file_path: str, is_valid: bool
    ):
        update_query = (
            update(FileMetadata)
            .where(FileMetadata.id == file_metadata_id)
            .values(is_valid=is_valid, file_path=file_path)
        )

        db.execute(update_query, execution_options={"synchronize_session": False})
        db.commit()
