from app.services.retrieval import retrieve_evidence
from app.services.feedback import get_learned_preferences
from app.core.config import settings
import uuid
from groq import Groq

client = Groq(api_key=settings.GROQ_API_KEY)

def generate_draft(document_ids: list, draft_type: str):
    # Retrieve evidence
    query = "key facts, parties, dates, main issues"
    evidence_chunks = retrieve_evidence(query, top_k=10)
    
    # Filter by document_ids if needed
    if document_ids:
        evidence_chunks = [c for c in evidence_chunks if c["source_document"] in document_ids]
        
    if not evidence_chunks:
        return "Insufficient evidence found in retrieved documents.", []
        
    context = "\n".join([f"[Chunk {c['chunk_id']}] {c['text']}" for c in evidence_chunks])
    
    preferences = get_learned_preferences()
    prefs_str = "\n".join([f"- Replace '{k}' with '{v}'" for k, v in preferences.items()])
    
    if settings.GROQ_API_KEY == "dummy_key":
        # Mock response
        draft_content = "This is a mock draft summary based on the following evidence."
        for k, v in preferences.items():
            draft_content = draft_content.replace(k, v)
        return draft_content, evidence_chunks
        
    prompt = f"""
    You are a legal document assistant. Create a {draft_type} based strictly on the provided evidence.
    If information is missing, state 'Missing Information'.
    Cite evidence using [Chunk ID] inline.
    
    Apply the following terminology preferences learned from operators:
    {prefs_str}
    
    Evidence:
    {context}
    """
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": prompt}]
        )
        draft_content = response.choices[0].message.content
        return draft_content, evidence_chunks
    except Exception as e:
        return f"Error generating draft: {str(e)}", evidence_chunks
