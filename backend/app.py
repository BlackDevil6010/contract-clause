# backend/app.py
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import fitz  # PyMuPDF
import logging
from typing import List, Dict

app = FastAPI(title="Contract Risk Analyzer – MVP")

# Allow frontend (localhost:5500 or any origin during dev)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Very simple keyword-based clause detection (expand later with ML)
CLAUSE_PATTERNS = {
    "Limitation of Liability": ["limit", "liability", "damages", "consequential", "indirect"],
    "Indemnification": ["indemnify", "indemnification", "hold harmless"],
    "Termination": ["terminate", "termination", "cancel", "end this agreement"],
    "Governing Law": ["governed by", "governing law", "laws of", "jurisdiction"],
    "Confidentiality": ["confidential", "nda", "non-disclosure"],
    "Payment Terms": ["payment", "fee", "invoice", "due date", "consideration"],
}

def detect_clause_type(text: str) -> tuple[str, int]:
    text_lower = text.lower()
    best_type = "General / Other"
    best_score = 0

    for clause_type, keywords in CLAUSE_PATTERNS.items():
        matches = sum(1 for kw in keywords if kw in text_lower)
        if matches > best_score:
            best_score = matches
            best_type = clause_type

    confidence = min(40 + best_score * 12, 92)
    return best_type, confidence

def get_risk_info(clause_type: str, text: str) -> tuple[int, str]:
    text_lower = text.lower()
    score = 30
    reason = "Standard clause – low concern"

    if "liability" in text_lower or "indemnif" in text_lower:
        score = 85
        reason = "High risk – broad liability or indemnity exposure"
    elif clause_type in ["Termination", "Confidentiality"]:
        score = 65
        reason = "Medium risk – important commercial terms"
    elif "payment" in text_lower:
        score = 55
        reason = "Payment terms – check for penalties or delays"

    return score, reason

def extract_text_from_pdf(content: bytes) -> str:
    try:
        doc = fitz.open(stream=content, filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text("text") + "\n\n"
        doc.close()
        return text.strip()
    except Exception as e:
        logger.error(f"PDF extraction failed: {e}")
        raise HTTPException(400, f"Invalid or corrupted PDF: {str(e)}")

@app.post("/analyze")
async def analyze_contract(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(400, "Only PDF files are allowed")

    try:
        content = await file.read()

        if len(content) > 12 * 1024 * 1024:  # ~12 MB limit
            raise HTTPException(400, "File too large (max 12 MB)")

        raw_text = extract_text_from_pdf(content)

        # Very basic paragraph splitting
        paragraphs = [
            p.strip() for p in raw_text.split("\n\n")
            if p.strip() and len(p.strip()) > 25
        ]

        if not paragraphs:
            return {
                "status": "warning",
                "message": "No readable content found. Document may be scanned or image-only.",
                "clauses": []
            }

        clauses = []
        for i, para in enumerate(paragraphs):
            clause_type, confidence = detect_clause_type(para)
            risk_score, risk_reason = get_risk_info(clause_type, para)

            clauses.append({
                "id": i + 1,
                "clause_type": clause_type,
                "confidence_score": confidence,
                "risk_score": risk_score,
                "risk_flag_reason": risk_reason,
                "extracted_text": para[:450] + ("..." if len(para) > 450 else ""),
                "text_length": len(para)
            })

        return {"clauses": clauses}

    except HTTPException as e:
        raise e
    except Exception as e:
        logger.exception("Unexpected error")
        raise HTTPException(500, "Internal server error")

@app.get("/")
async def root():
    return {"message": "Contract Risk Analyzer API – MVP is running"}