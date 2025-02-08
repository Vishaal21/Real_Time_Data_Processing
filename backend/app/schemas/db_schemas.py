from datetime import datetime

from sqlalchemy import Boolean, Column, Date, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Security(Base):
    __tablename__ = "security"
    id = Column(Integer, primary_key=True)
    Name = Column(String, index=True)
    Open = Column(String, index=True)
    Close = Column(String, index=True)
    High = Column(String, index=True)
    Low = Column(String, index=True)
    Volume = Column(String, index=True)
    Date = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # Foreign key to FileMetadata
    file_metadata_id = Column(
        Integer, ForeignKey("file_metadata.id", ondelete="CASCADE")
    )

    # Relationship to FileMetadata
    file_metadata = relationship("FileMetadata", back_populates="securities")


class FileMetadata(Base):
    __tablename__ = "file_metadata"
    id = Column(Integer, primary_key=True, autoincrement=True)
    file_name = Column(String)
    file_path = Column(String)
    file_size = Column(String)
    file_type = Column(String)
    upload_date = Column(Date)
    is_valid = Column(Boolean, default=False)
    validation_message = Column(String)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # Relationship to Security
    securities = relationship(
        "Security", back_populates="file_metadata", cascade="all, delete-orphan"
    )
