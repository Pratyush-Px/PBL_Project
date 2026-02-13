import os
import base64
import json
import re
from typing import Union

from fastapi import HTTPException
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from google.generativeai import GenerativeModel, configure

from schemas import InvoiceExtract, PurchaseOrderExtract
from models import ExtractedDocument, DocumentType
from utils.hashing import calculate_file_hash

# =========================
# ENV & MODEL SETUP
# =========================
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY not found")

configure(api_key=GEMINI_API_KEY)
model = GenerativeModel("gemini-2.5-flash")


# =========================
# PROMPTS
# =========================
def _build_extraction_prompt() -> str:
    return """
You are an intelligent finance document parser.

Your task is to extract invoice or purchase order data and return ONLY valid JSON
that strictly follows the schema below.

Schema:
{
  "invoice_number": string | null,
  "invoice_date": string | null,
  "vendor_name": string | null,
  "total_amount": number | null,
  "currency": string | null,
  "line_items": [
    {
      "description": string,
      "quantity": number | null,
      "unit_price": number | null,
      "total": number | null
    }
  ],
  "confidence_score": number (0-100)
}

Rules:
- Use EXACT field names from the schema
- Do NOT add extra fields
- Use null if a value is missing or unclear
- Prefer numeric values (no currency symbols)
- If no line items are found, return an empty array []
- confidence_score: how confident you are in the extraction (0-100)
- Output JSON ONLY
- Do NOT include explanations or markdown
"""


# =========================
# HELPERS
# =========================
def _parse_gemini_json(text: str) -> dict:
    """Safely extract JSON from Gemini response."""
    cleaned = re.sub(r"```json|```", "", text).strip()
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON returned from Gemini")


def _get_cached_document(file_hash: str, db: Session) -> ExtractedDocument | None:
    """Check if this file was already processed."""
    return (
        db.query(ExtractedDocument)
        .filter(ExtractedDocument.file_hash == file_hash)
        .first()
    )


def _save_document_to_db(
    *,
    db: Session,
    file_hash: str,
    filename: str,
    document_type: DocumentType,
    extracted_json: dict,
    model_used: str,
) -> ExtractedDocument:
    doc = ExtractedDocument(
        file_hash=file_hash,
        filename=filename,
        document_type=document_type,
        extracted_json=extracted_json,
        model_used=model_used,
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc


# =========================
# PUBLIC API
# =========================
def extract_document(
    *,
    file_bytes: bytes,
    filename: str,
    content_type: str,
    document_type: DocumentType,
    db: Session,
) -> dict:
    """
    Extract structured data from a document image/PDF.

    Returns:
        {
            "source": "cache" | "gemini",
            "duplicate": bool,
            "data": dict  (validated extraction)
        }
    """
    file_hash = calculate_file_hash(file_bytes)

    # --- Cache check ---
    cached = _get_cached_document(file_hash, db)
    if cached:
        return {
            "source": "cache",
            "duplicate": True,
            "data": cached.extracted_json,
        }

    # --- Gemini extraction ---
    encoded = base64.b64encode(file_bytes).decode("utf-8")
    prompt = _build_extraction_prompt()

    try:
        response = model.generate_content(
            [
                prompt,
                {
                    "mime_type": content_type,
                    "data": encoded,
                },
            ]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gemini API error: {str(e)}")

    # --- Parse & validate ---
    parsed = _parse_gemini_json(response.text)

    try:
        if document_type == DocumentType.purchase_order:
            validated = PurchaseOrderExtract(**parsed)
        else:
            validated = InvoiceExtract(**parsed)
    except Exception:
        raise HTTPException(
            status_code=422, detail="Gemini output failed schema validation"
        )

    validated_dict = validated.model_dump()

    # --- Store in DB ---
    _save_document_to_db(
        db=db,
        file_hash=file_hash,
        filename=filename,
        document_type=document_type,
        extracted_json=validated_dict,
        model_used="gemini-2.5-flash",
    )

    return {
        "source": "gemini",
        "duplicate": False,
        "data": validated_dict,
    }
