from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Body
from sqlalchemy.orm import Session
import shutil
import uuid
import os
from typing import List

from app.db.database import get_db
from app.db.models import DocumentRecord
from app.core.config import settings
from app.models.schemas import *
from app.services.document_processor import process_document
from app.services.extraction import extract_structured_data
from app.services.retrieval import index_document, retrieve_evidence
from app.services.generation import generate_draft
from app.services.feedback import process_feedback

router = APIRouter()

@router.post("/upload", response_model=DocumentResponse)
async def upload_document(file: UploadFile = File(...), db: Session = Depends(get_db)):
    doc_id = str(uuid.uuid4())
    filepath = os.path.join(settings.UPLOAD_DIR, f"{doc_id}_{file.filename}")
    
    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    db_doc = DocumentRecord(
        id=doc_id,
        filename=file.filename,
        filepath=filepath,
        status="uploaded"
    )
    db.add(db_doc)
    db.commit()
    db.refresh(db_doc)
    
    return DocumentResponse(document_id=doc_id, filename=file.filename, status="uploaded")

@router.post("/process", response_model=ProcessResponse)
async def process_doc(document_id: str = Body(..., embed=True), db: Session = Depends(get_db)):
    db_doc = db.query(DocumentRecord).filter(DocumentRecord.id == document_id).first()
    if not db_doc:
        raise HTTPException(status_code=404, detail="Document not found")
        
    try:
        # OCR and Image preprocessing
        extracted_text, conf = process_document(db_doc.filepath)
        
        # Structured Data Extraction
        structured_data = extract_structured_data(extracted_text)
        
        # Indexing / Chunking
        index_document(extracted_text, document_id)
        
        db_doc.raw_text = extracted_text
        db_doc.structured_data = structured_data
        db_doc.status = "processed"
        db.commit()
        
        return ProcessResponse(
            document_id=document_id,
            extracted_text=extracted_text,
            confidence_score=conf,
            structured_data=structured_data
        )
    except Exception as e:
        db_doc.status = "failed"
        db.commit()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/retrieve", response_model=RetrieveResponse)
async def retrieve_docs(request: RetrieveRequest):
    evidence = retrieve_evidence(request.query, request.top_k)
    return RetrieveResponse(evidence=[EvidenceChunk(**e) for e in evidence])

@router.post("/generate", response_model=GeneratedDraft)
async def generate_document(request: GenerateRequest):
    draft_content, evidence = generate_draft(request.document_ids, request.draft_type)
    
    return GeneratedDraft(
        draft_id=str(uuid.uuid4()),
        content=draft_content,
        evidence_links=[{"chunk_id": e["chunk_id"], "text": e["text"]} for e in evidence]
    )

@router.post("/feedback", response_model=FeedbackResponse)
async def submit_feedback(request: FeedbackRequest):
    learned_count = process_feedback(request.draft_id, request.context, request.replace)
    return FeedbackResponse(status="success", learned_signals=learned_count)
