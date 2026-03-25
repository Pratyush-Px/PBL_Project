from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from database import engine, get_db
from models import Base, DocumentType, ComparisonResult
from services.gemini_service import extract_document
from services.comparison_service import compare_documents
from services.risk_service import calculate_risk
from utils.timing import timer

# =========================
# AUTO-CREATE TABLES
# =========================
Base.metadata.create_all(bind=engine)

# =========================
# FASTAPI APP
# =========================
app = FastAPI(
    title="Invoice & PO Validator",
    description="Gemini-powered document extraction, comparison, and risk scoring API",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================
# GET /health
# =========================
@app.get("/health")
def health_check():
    return {"status": "healthy"}


# =========================
# POST /extract
# =========================
@app.post("/extract")
async def extract(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """
    Extract structured data from an invoice or purchase order.
    Returns extracted fields, source (cache/gemini), duplicate flag, and timing.
    """
    file_bytes = await file.read()
    content_type = file.content_type or "application/octet-stream"
    filename = file.filename or "unknown"

    # Determine document type from filename hint
    doc_type = DocumentType.purchase_order if "po" in filename.lower() or "purchase" in filename.lower() else DocumentType.invoice

    with timer() as t:
        result = extract_document(
            file_bytes=file_bytes,
            filename=filename,
            content_type=content_type,
            document_type=doc_type,
            db=db,
        )

    return {
        "status": "success",
        "source": result["source"],
        "duplicate": result["duplicate"],
        "extracted_data": result["data"],
        "extraction_time_ms": t["elapsed_ms"],
    }


# =========================
# POST /compare
# =========================
@app.post("/compare")
async def compare(
    invoice: UploadFile = File(...),
    purchase_order: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """
    Extract both documents, compare totals and line items,
    and return a structured comparison with risk scoring.
    """
    with timer() as total_timer:
        # --- Extract invoice ---
        inv_bytes = await invoice.read()
        inv_result = extract_document(
            file_bytes=inv_bytes,
            filename=invoice.filename or "invoice",
            content_type=invoice.content_type or "application/octet-stream",
            document_type=DocumentType.invoice,
            db=db,
        )

        # --- Extract purchase order ---
        po_bytes = await purchase_order.read()
        po_result = extract_document(
            file_bytes=po_bytes,
            filename=purchase_order.filename or "purchase_order",
            content_type=purchase_order.content_type or "application/octet-stream",
            document_type=DocumentType.purchase_order,
            db=db,
        )

        # --- Compare ---
        comparison = compare_documents(inv_result["data"], po_result["data"])

        # --- Risk scoring ---
        risk = calculate_risk(
            summary=comparison["summary"],
            line_item_analysis=comparison["line_item_analysis"],
            invoice_currency=inv_result["data"].get("currency"),
            po_currency=po_result["data"].get("currency"),
        )

    return {
        "summary": comparison["summary"].model_dump(),
        "line_item_analysis": [item.model_dump() for item in comparison["line_item_analysis"]],
        "confidence_score": comparison["confidence_score"],
        "risk_score": risk.risk_score,
        "risk_reason": risk.risk_reason,
        "processing_time_ms": total_timer["elapsed_ms"],
    }


# =========================
# GET /results
# =========================
@app.get("/results")
def get_results(db: Session = Depends(get_db)):
    """Return all stored comparison results (newest first)."""
    rows = (
        db.query(ComparisonResult)
        .order_by(ComparisonResult.created_at.desc())
        .all()
    )
    return [
        {
            "id": str(r.id),
            "order_id": r.order_id,
            "match_status": r.match_status,
            "risk_score": r.risk_score,
            "confidence_score": r.confidence_score,
            "created_at": r.created_at.isoformat() if r.created_at else None,
        }
        for r in rows
    ]


# =========================
# GET /results/{result_id}
# =========================
@app.get("/results/{result_id}")
def get_result_detail(result_id: str, db: Session = Depends(get_db)):
    """Return full details for a single comparison result."""
    row = (
        db.query(ComparisonResult)
        .filter(ComparisonResult.id == result_id)
        .first()
    )
    if not row:
        raise HTTPException(status_code=404, detail="Result not found")
    return {
        "id": str(row.id),
        "order_id": row.order_id,
        "match_status": row.match_status,
        "risk_score": row.risk_score,
        "confidence_score": row.confidence_score,
        "created_at": row.created_at.isoformat() if row.created_at else None,
        "result_json": row.result_json,
    }
