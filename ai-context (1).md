# AI Context: Study-Buddy Capstone Project

## Project Overview
Study-Buddy is an end-to-end AI system that analyzes student answers, identifies why they are wrong, and delivers targeted remediation based on a universal gap taxonomy[cite: 2]. The taxonomy serves as a routing system for specialized problem-specific feedback[cite: 3]. 

## Tech Stack
- **Backend:** Python, FastAPI.
- **Data Persistence:** PostgreSQL (managed via SQLAlchemy ORM + Alembic migrations).
- **AI/Retrieval:** Anthropic Claude API (gap classification + feedback generation), Vector database for RAG (e.g., Pinecone or Chroma — TBD during RAG spike).
- **Adapters:** OCR engine for handwritten input (e.g., Tesseract or Google Vision — TBD during adapter sprint).
- **Dev Environment:** Docker Compose (Postgres + backend services), Python virtual environment.
- **CI/CD:** GitHub Actions → staging auto-deploy on every merge to main.

## Architecture Patterns
- **Layered Architecture:** Frontend → API Layer → Gap Classification Engine → RAG Retrieval → Data Layer.
- **Dependency Injection:** Constructor injection only; explicit dependencies.
- **Data Contracts:** Strict Pydantic models for all API requests/responses and LLM JSON outputs. Contracts are designed at two levels: a high-level endpoint map upfront for the whole project, and detailed request/response shapes per feature right before building that feature.
- **Schema Management:** Database tables are designed and created per feature using Alembic migrations — never designed for the whole app upfront. Each migration is committed to Git alongside the feature that needs it.
- **Vertical Feature Delivery:** Each feature is built backend → API endpoint → frontend. No layer is built in bulk ahead of others.

## Hard Constraints & Rules
- **Taxonomy First:** The LLM is constrained to classify the gap type before generating any feedback.
- **Course-Grounded RAG:** Feedback is generated strictly from retrieved course material; no general training data reasoning.
- **Loud Failures:** Hallucinations must fail loudly and be noticed. Low-confidence outputs must be flagged for review, never silently passed to students.
- **OCR Limitations:** OCR output is treated as best-effort, lossy text. It only supports text-only handwriting, no diagrams, and no complex mathematical notation.
- **Banned Patterns:**
  - No field injection.
  - No silent exception swallowing.
  - No unstructured LLM text outputs (must use structured JSON).
  - No bulk schema design upfront — Alembic migrations only, per feature.
  - No deferred testing — tests are written per feature before moving on.

## Development Principles
- **Risk First:** The RAG + gap classification pipeline is the highest-risk component. It is spiked and validated in isolation before any UI or database schema is built. If the core intelligence fails, the project scope is adjusted early.
- **Walking Skeleton Before Features:** Before any real feature is built, a single end-to-end connection (button → endpoint → DB read) is established to prove the infrastructure works.
- **Auth Before Features:** Authentication and role separation (student vs professor) are implemented before any feature that depends on knowing who is logged in.
- **CI/CD From Day One:** GitHub Actions is configured early. Deployment is automatic on every merge — not a manual step per feature.