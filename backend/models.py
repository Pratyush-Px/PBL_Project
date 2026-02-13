# models.py
import uuid
from sqlalchemy import Column, String, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
import enum

from database import Base


# -------------------------
# ENUM: Document Type
# -------------------------
class DocumentType(enum.Enum):
    invoice = "invoice"
    purchase_order = "purchase_order"


# -------------------------
# TABLE: extracted_documents
# -------------------------
class ExtractedDocument(Base):
    __tablename__ = "extracted_documents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # What kind of document this is
    document_type = Column(Enum(DocumentType), nullable=False)

    # Original filename (for debugging / traceability)
    filename = Column(String, nullable=True)

    # SHA256 hash of file bytes (for caching / deduplication)
    file_hash = Column(String, unique=True, index=True, nullable=False)

    # Gemini-extracted JSON (schema-aligned)
    extracted_json = Column(JSONB, nullable=False)

    # Which model produced this output
    model_used = Column(String, nullable=False)

    # Audit timestamp
    created_at = Column(DateTime(timezone=True), server_default=func.now())
