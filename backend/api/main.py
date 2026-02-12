"""
FastAPI backend for Invoice vs Purchase Order Validation System.
Wraps existing OCR modules without duplicating or modifying them.
"""

import sys
import os
import io

import cv2
import numpy as np
from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

# ---------------------------------------------------------------------------
# Ensure project root is on sys.path so `src.*` imports work when running
# from the api/ subdirectory or via `uvicorn api.main:app`.
# ---------------------------------------------------------------------------
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.preprocessing import ImagePreprocessor
from src.ocr_engine import OCREngine
from src.utils import clean_text
from src.extractor import DocumentExtractor
from src.comparator import DocumentComparator

# ---------------------------------------------------------------------------
# Pydantic Models
# ---------------------------------------------------------------------------


class LineItem(BaseModel):
    name: str
    quantity: float
    unit_price: float
    total: float


class ExtractionResult(BaseModel):
    document_type: str
    vendor: Optional[str] = None
    invoice_number: Optional[str] = None
    date: Optional[str] = None
    items: list[LineItem] = []
    total_amount: Optional[float] = None


class Difference(BaseModel):
    field: str
    order_value: Optional[str] = None
    invoice_value: Optional[str] = None


class ComparisonResult(BaseModel):
    status: str
    match_percentage: float
    differences: list[Difference] = []


class FullComparisonResponse(BaseModel):
    order_data: ExtractionResult
    invoice_data: ExtractionResult
    comparison: ComparisonResult


# ---------------------------------------------------------------------------
# App Setup
# ---------------------------------------------------------------------------

app = FastAPI(
    title="Invoice & PO Validation API",
    description="OCR-powered document extraction and order-vs-invoice comparison.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Shared instances (stateless, safe to reuse)
_preprocessor = ImagePreprocessor()
_ocr_engine = OCREngine()
_extractor = DocumentExtractor()
_comparator = DocumentComparator()

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _bytes_to_cv2(file_bytes: bytes) -> np.ndarray:
    """Decode raw file bytes into an OpenCV image array (in-memory, no disk I/O)."""
    arr = np.frombuffer(file_bytes, dtype=np.uint8)
    image = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    if image is None:
        raise HTTPException(status_code=400, detail="Could not decode the uploaded image.")
    return image


def _run_pipeline(image: np.ndarray, document_type: Optional[str] = None) -> dict:
    """
    Full extraction pipeline: preprocess → OCR → clean → extract.
    Uses existing OCR modules without modification.
    """
    # 1. Preprocess (in-memory: grayscale → noise reduction)
    gray = _preprocessor.to_grayscale(image)
    processed = _preprocessor.remove_noise(gray)

    # 2. OCR
    raw_text = _ocr_engine.extract_text(processed, psm=6)

    # 3. Clean text
    cleaned = clean_text(raw_text)

    # 4. Structured extraction
    result = _extractor.extract(cleaned, document_type=document_type)
    return result


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@app.post("/extract", response_model=ExtractionResult)
async def extract_document(
    file: UploadFile = File(..., description="Image file (PNG, JPG, TIFF, etc.)"),
    document_type: Optional[str] = Form(None, description="'invoice' or 'order'. Auto-detected if omitted."),
):
    """
    Upload a document image → get structured JSON with extracted fields.
    """
    contents = await file.read()
    image = _bytes_to_cv2(contents)
    result = _run_pipeline(image, document_type=document_type)
    return ExtractionResult(**result)


@app.post("/compare", response_model=FullComparisonResponse)
async def compare_documents(
    order_file: UploadFile = File(..., description="Purchase Order image"),
    invoice_file: UploadFile = File(..., description="Invoice image"),
):
    """
    Upload an order image and an invoice image → get a comparison result.
    """
    order_bytes = await order_file.read()
    invoice_bytes = await invoice_file.read()

    order_image = _bytes_to_cv2(order_bytes)
    invoice_image = _bytes_to_cv2(invoice_bytes)

    order_result = _run_pipeline(order_image, document_type="order")
    invoice_result = _run_pipeline(invoice_image, document_type="invoice")

    comparison = _comparator.compare(order_result, invoice_result)
    
    return FullComparisonResponse(
        order_data=ExtractionResult(**order_result),
        invoice_data=ExtractionResult(**invoice_result),
        comparison=ComparisonResult(**comparison)
    )


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------


@app.get("/health")
async def health():
    return {"status": "ok"}
