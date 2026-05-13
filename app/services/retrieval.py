from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os
import json
import uuid

model = SentenceTransformer('all-MiniLM-L6-v2')

index_path = "./data/vector_store/index.faiss"
metadata_path = "./data/vector_store/metadata.json"

dimension = 384
if os.path.exists(index_path):
    index = faiss.read_index(index_path)
    with open(metadata_path, 'r') as f:
        chunk_metadata = json.load(f)
else:
    index = faiss.IndexFlatL2(dimension)
    chunk_metadata = {}

def save_index():
    faiss.write_index(index, index_path)
    with open(metadata_path, 'w') as f:
        json.dump(chunk_metadata, f)

def chunk_text(text: str, document_id: str, chunk_size=200, overlap=50):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk_text = " ".join(words[i:i+chunk_size])
        chunks.append({
            "chunk_id": str(uuid.uuid4()),
            "text": chunk_text,
            "document_id": document_id,
            "page_number": 1 # Simplified, could be parsed from text
        })
    return chunks

def index_document(text: str, document_id: str):
    chunks = chunk_text(text, document_id)
    if not chunks:
        return
        
    texts = [c["text"] for c in chunks]
    embeddings = model.encode(texts)
    
    start_idx = index.ntotal
    index.add(np.array(embeddings).astype('float32'))
    
    for i, chunk in enumerate(chunks):
        chunk_metadata[str(start_idx + i)] = chunk
        
    save_index()

def retrieve_evidence(query: str, top_k: int = 5):
    if index.ntotal == 0:
        return []
        
    query_emb = model.encode([query]).astype('float32')
    distances, indices = index.search(query_emb, top_k)
    
    results = []
    for dist, idx in zip(distances[0], indices[0]):
        if idx != -1:
            meta = chunk_metadata[str(idx)]
            results.append({
                "chunk_id": meta["chunk_id"],
                "text": meta["text"],
                "source_document": meta["document_id"],
                "page_number": meta.get("page_number", 1),
                "score": float(dist)
            })
    return results
