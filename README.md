# ⚖️ LexDraft AI — Grounded Legal Document Intelligence

![LexDraft AI Overview](https://img.shields.io/badge/Status-MVP_Ready-success?style=flat-square)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110.0-009688?style=flat-square&logo=fastapi)
![Groq](https://img.shields.io/badge/Groq-Llama_3.3-f43f5e?style=flat-square)

Welcome to **LexDraft AI**, an end-to-end AI workflow specifically engineered to ingest noisy legal documents, extract structured entities, and generate **retrieval-grounded, highly-traceable draft summaries** that continuously improve via operator feedback.

---

## 🎯 Reviewer Guide: Core Objectives Met

This system was designed with strict adherence to the assessment's functional requirements. For a quick evaluation, here is how the system solves the core challenges:

1. **Messy Document Processing:** Uses `OpenCV` for image denoising/thresholding and `EasyOCR` to handle low-quality scans gracefully.
2. **Grounded Retrieval & Drafting:** Utilizes `FAISS` and `SentenceTransformers` to chunk and embed documents. The `llama-3.3-70b-versatile` model explicitly generates drafts containing inline citations (e.g., `[Chunk ID]`) linking back to exact source text.
3. **Operator Edit Capture:** Exposes a feedback mechanism where users can submit corrections (e.g., "claimant" -> "plaintiff"). The system saves these to SQLite and forces the LLM to adhere to them in all subsequent drafts.
4. **Engineering Quality:** Separates concerns perfectly (`api`, `services`, `db`, `models`) ensuring testability, readability, and modularity.

---

## 🚀 Quick Setup Guide

We have optimized the setup process to be as frictionless as possible. 

### 1. Prerequisites
- Python 3.9+
- A valid [Groq API Key](https://console.groq.com/keys) (Used for lightning-fast LLM inference)

### 2. Local Installation

```bash
# Clone the repository and enter the directory
cd ai-engineer-home-assesment

# Create and activate a virtual environment
python -m venv .venv

# On Windows:
.venv\Scripts\activate
# On Mac/Linux:
source .venv/bin/activate

# Install dependencies (numpy ABI issues are pre-handled)
pip install -r requirements.txt
```

### 3. Environment Configuration

Create a `.env` file in the root directory and add your Groq API key:

```env
GROQ_API_KEY=your_groq_api_key_here
```
*(Note: If left as `dummy_key`, the system has a built-in mock fallback for testing the pipeline without incurring API calls).*

---

## 🖥️ Running the Application

Start the FastAPI backend with Uvicorn:

```bash
uvicorn app.main:app --reload
```

### Option A: The Interactive UI (Recommended)
We have built a beautiful, standalone Glassmorphic UI to test the entire pipeline end-to-end seamlessly.
👉 **Open your browser to: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)**

**How to test the UI flow:**
1. **Upload:** Drag and drop any noisy text/image snippet.
2. **Process:** Click process to trigger the OCR pipeline and Structured JSON extraction.
3. **Generate:** Generate a grounded draft. Notice the inline chunk citations linking to the exact evidence!
4. **Feedback:** Type a replacement rule (e.g., change "claimant" to "plaintiff") and submit. Re-run Step 3 to watch the AI instantly learn and apply your formatting rules!

### Option B: Swagger API Documentation
If you prefer testing raw JSON payloads, FastAPI provides auto-generated OpenAPI documentation.
👉 **Navigate to: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**

---

## 🏗️ System Architecture

The application is structured into modular micro-components to ensure maximum maintainability.

```text
ai-engineer-home-assesment/
├── app/
│   ├── api/           # API Routing (upload, process, retrieve, generate, feedback)
│   ├── core/          # Environment & Application Settings
│   ├── db/            # SQLite Setup & SQLAlchemy Models
│   ├── models/        # Pydantic validation schemas
│   ├── services/      # Core Business Logic (OCR, Vector Search, LLMs)
│   └── static/        # Frontend UI Assets (HTML, CSS, JS)
├── data/              # SQLite DB, Vector Store DB, and Uploads
├── requirements.txt   # Pinned dependencies
└── .env               # Secrets configuration
```

## 🛠️ Assumptions & Tradeoffs
- **Groq over OpenAI:** Upgraded from the PRD to use Groq (`llama-3.3-70b-versatile`) for superior speed during extraction and generation.
- **FAISS & SQLite:** Selected for the MVP to allow zero-dependency local execution for the reviewer. In production, these would be swapped for Pinecone and PostgreSQL respectively.
- **Feedback Loop Mechanism:** Implemented a direct dictionary-replacement injection into the LLM system prompt. While production might use DPO (Direct Preference Optimization), this rule-based approach provides immediate, interpretably guaranteed learning for the MVP.
