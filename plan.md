# Project Plan: Study-Buddy

## Phase 0: Foundation (Do Once, Before Any Code)

### Step 1 — Lock Requirements & Scope MVP
- [ ] Define exactly what the MVP includes and explicitly list what is out of scope.
- [ ] MVP scope: student submits answer → system classifies gap → system returns structured feedback. Professor can upload course material and view analytics.
- [ ] Out of scope for MVP: OCR, video generation, flashcards, adaptive difficulty, study planner.

### Step 2 — Finalize Tech Stack
- Locked. See ai-context.md.

### Step 3 — Set Up Dev Environment
- [ ] Initialize Git repository with branching convention (`feature/`, `fix/`).
- [ ] Create `docker-compose.yml` with Postgres and backend services.
- [ ] Set up Python virtual environment and `requirements.txt`.
- [ ] Configure environment variables (`.env` file, never committed to Git).
- [ ] Confirm all services start cleanly with `docker compose up`.

### Step 4 — High-Level API Contract (Endpoint Map)
- [ ] Write a rough map of all endpoints and their purpose (not detailed shapes yet).
- [ ] This is the shared agreement so frontend and backend stay aligned throughout the project.
- [ ] Detailed Pydantic request/response models are written per feature, right before building that feature.

### Step 5 — Define Architecture Pattern
- Locked. Layered architecture. See ai-context.md.

---

## Sprint 1: Walking Skeleton (Infrastructure Proof)

### Step 6 — Walking Skeleton
- [ ] Build one minimal end-to-end flow: button on frontend → FastAPI endpoint → Postgres read → response displayed.
- [ ] No real logic. Goal is to prove Docker, CORS, DB connection, and environment config all work together.
- [ ] Do not move to Sprint 2 until this works cleanly.

### Step 7 — Authentication & Role System
- [ ] Implement JWT-based auth (register, login, token validation).
- [ ] Enforce role separation: `student` vs `professor` on all protected routes.
- [ ] This must be in place before building any feature that depends on identity.

---

## Sprint 2: Core Intelligence (Highest Risk — Build First)

> This is the riskiest component. If the RAG + classification pipeline cannot produce reliable structured output, the project scope must be adjusted before anything else is built around it.

### Step 8 — RAG + Gap Classification Spike
- [ ] In isolation (Jupyter notebook or throwaway script), prove the pipeline works end-to-end:
  - Upload a PDF → chunk it → embed it → store in vector DB → retrieve relevant chunks for a query.
  - Pass chunks + student answer to Claude API → receive structured JSON output matching the gap taxonomy.
- [ ] Validate structured output enforces the Pydantic `Diagnosis` model.
- [ ] If this spike fails or produces unreliable output, adjust project scope before proceeding.

### Step 9 — Feature: Answer Submission & Gap Diagnosis
- [ ] Design DB schema for this feature only (`answers`, `diagnoses` tables) → write Alembic migration → apply.
- [ ] Write detailed Pydantic contracts for `POST /answers` and `GET /answers/:id/diagnosis`.
- [ ] Backend: implement gap classification service (taxonomy-constrained, RAG-grounded).
- [ ] Backend: implement consistency-based confidence scoring (multiple generations, measure agreement).
- [ ] API: expose endpoints, enforce Pydantic contracts.
- [ ] Frontend: student answer submission form + structured feedback display.
- [ ] Tests: unit test classification logic, integration test the endpoint.

### Step 10 — Feature: Course Material Upload
- [ ] Design DB schema (`courses`, `course_chunks` tables) → Alembic migration → apply.
- [ ] Write Pydantic contracts for `POST /courses`.
- [ ] Backend: PDF ingestion → chunking → embedding → vector DB storage.
- [ ] API: expose upload endpoint.
- [ ] Frontend: professor upload form.
- [ ] Tests: test chunking and retrieval pipeline.

---

## Sprint 3: Remaining MVP Features

> Each feature follows the same loop: schema → Pydantic contract → backend → API → frontend → tests.

### Step 11 — Feature: Question Generation
- [ ] Schema, contracts, backend, API, frontend, tests.

### Step 12 — Feature: Professor Analytics Dashboard
- [ ] Schema (aggregation queries, no new tables likely needed), contracts, backend, API, frontend, tests.

### Step 13 — Feature: Student Practice Mode
- [ ] Schema, contracts, backend, API, frontend, tests.

---

## Sprint 4: Validation & Evaluation

### Step 14 — Evaluation Pipeline
- [ ] Build evaluation script: run system on a fixed set of student answers.
- [ ] Calculate Cohen's Kappa between system output and two-professor ground truth baseline.
- [ ] Benchmark: system agreement with ground truth must match or exceed inter-professor agreement.

---

## Sprint 5: Hardening & Launch

### Step 15 — CI/CD
- [ ] Set up GitHub Actions: run tests on every push, auto-deploy to staging on merge to main.
- [ ] This should be configured early (ideally after Sprint 1) but listed here as a checkpoint.

### Step 16 — UI Polish
- [ ] Upgrade minimal functional UI to final visual design.
- [ ] Component library used from day one (shadcn/ui or equivalent) — this sprint is for customization and polish only.

### Step 17 — Final Deployment & Hardening
- [ ] Production environment setup (env vars, secrets, DB backups).
- [ ] Load test critical endpoints (answer submission, RAG retrieval).
- [ ] Final security review (auth, input validation, rate limiting).

---

## Post-MVP (Same Loop as Above)

- OCR adapter for handwritten answers.
- Adaptive question difficulty based on gap history.
- Flashcard generation from course materials.
- Concept mind maps.
- Study schedule planner.
