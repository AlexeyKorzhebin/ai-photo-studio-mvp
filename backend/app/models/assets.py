from datetime import datetime
import uuid

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.db.base import Base


class ImageAsset(Base):
    __tablename__ = "image_assets"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    origin_type: Mapped[str] = mapped_column(String(32), default="upload")
    original_filename: Mapped[str] = mapped_column(String(255))
    stored_filename: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    mime_type: Mapped[str] = mapped_column(String(64))
    width: Mapped[int] = mapped_column(Integer)
    height: Mapped[int] = mapped_column(Integer)
    byte_size: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    metadata_entry: Mapped["ImageMetadata | None"] = relationship(back_populates="asset", uselist=False, cascade="all, delete-orphan")


class ImageMetadata(Base):
    __tablename__ = "image_metadata"

    asset_id: Mapped[str] = mapped_column(ForeignKey("image_assets.id"), primary_key=True)
    tags: Mapped[str] = mapped_column(Text, default="")
    notes: Mapped[str] = mapped_column(Text, default="")
    search_text_normalized: Mapped[str] = mapped_column(Text, default="")
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    asset: Mapped[ImageAsset] = relationship(back_populates="metadata_entry")
