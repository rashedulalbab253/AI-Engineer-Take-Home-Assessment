from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class DocumentResponse(BaseModel):
    document_id: str
    filename: str
    status: str
    
class ProcessResponse(BaseModel):
    document_id: str
    extracted_text: str
    confidence_score: float
    structured_data: Dict[str, Any]

class RetrieveRequest(BaseModel):
    query: str
    document_id: Optional[str] = None
    top_k: int = 5

class EvidenceChunk(BaseModel):
    chunk_id: str
    text: str
    page_number: int
    source_document: str
    score: float

class RetrieveResponse(BaseModel):
    evidence: List[EvidenceChunk]

class GenerateRequest(BaseModel):
    document_ids: List[str]
    draft_type: str = "case_summary"

class GeneratedDraft(BaseModel):
    draft_id: str
    content: str
    evidence_links: List[Dict[str, str]]

class FeedbackRequest(BaseModel):
    draft_id: str
    context: str
    replace: Dict[str, str]

class FeedbackResponse(BaseModel):
    status: str
    learned_signals: int
