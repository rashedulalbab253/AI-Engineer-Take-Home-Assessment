import json
import os
from groq import Groq
from app.core.config import settings

client = Groq(api_key=settings.GROQ_API_KEY)

def extract_structured_data(text: str):
    if settings.GROQ_API_KEY == "dummy_key":
        # Mock response for testing
        return {
            "document_id": "doc_mock",
            "parties": ["John Doe", "ABC Holdings"],
            "dates": ["2024-03-12"],
            "case_number": "CV-2024-002"
        }
        
    prompt = f"""
    Extract structured information from the following legal text.
    Return JSON format with fields: parties (list), dates (list), case_number (string), document_title (string).
    
    Text: {text[:2000]}
    """
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            response_format={ "type": "json_object" }
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        return {"error": str(e)}
