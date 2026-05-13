# LexDraft AI — Grounded Legal Document Intelligence System

LexDraft AI is an AI-powered legal document intelligence workflow designed to process messy legal-style documents, retrieve grounded evidence, generate structured first-pass draft outputs, and continuously improve through operator feedback.

## Features

- **Robust Document Processing**: OCR and text extraction from noisy PDFs and images using EasyOCR and OpenCV.
- **Structured Data Extraction**: Extracted unstructured data into structured formats (parties, dates, case numbers) using LLMs.
- **Semantic Retrieval**: Uses SentenceTransformers and FAISS for vector similarity search over document chunks.
- **Evidence-Grounded Drafting**: Generates case fact summaries grounded in retrieved chunks to minimize hallucinations.
- **Evidence Traceability**: Links every generated statement back to the source document and page/chunk.
- **Operator Edit Capture**: Learns reusable drafting preferences from operator edits (e.g., terminology replacement).

## Project Structure

- `app/` - FastAPI backend application
  - `api/` - REST API routes
  - `services/` - Core business logic (OCR, Retrieval, LLM generation, etc.)
  - `models/` - Pydantic and SQLAlchemy models
  - `db/` - SQLite database setup
- `data/` - Uploaded files, vector store, and SQLite database
- `Dockerfile` & `docker-compose.yml` - Containerization configurations

## Prerequisites

- Python 3.9+
- Groq API Key for structured extraction and drafting (Set in `.env`)

## Local Setup

1. Navigate to the project directory:
   ```bash
   cd ai-engineer-home-assesment
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```

4. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```

5. Access the API documentation at `http://127.0.0.1:8000/docs`

## Docker Setup

1. Run the application using Docker Compose:
   ```bash
   docker-compose up --build
   ```

## Assumptions and Tradeoffs

- **FAISS over Cloud Vector DB**: Selected for simplicity and local execution without external dependencies.
- **EasyOCR over Tesseract**: EasyOCR handles noisy inputs well and doesn't require complex system-level installations beyond pip.
- **Mock LLM Fallback**: If an invalid Groq API key is provided, the system falls back to mock responses to allow testing of the API flow without incurring costs.
- **Rule-based feedback learning**: Direct search and replace based on user feedback is used for transparency and immediate effect.

## API Endpoints

- `POST /api/v1/upload` - Upload a document
- `POST /api/v1/process` - Run OCR and extraction
- `POST /api/v1/retrieve` - Retrieve relevant evidence
- `POST /api/v1/generate` - Generate grounded draft
- `POST /api/v1/feedback` - Submit operator edits
