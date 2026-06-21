# Current State

## Working
- Project documentation and AI context files initialized.
- Project workflow and development methodology locked (see plan.md).

## In Progress
- Sprint 1, Step 3: Setting up dev environment (Docker, Git, virtual environment).

## Up Next
- Step 4: Write high-level API endpoint map.
- Step 6: Build walking skeleton (button → endpoint → DB read).
- Step 7: Authentication and role system (student vs professor).
- Step 8: RAG + gap classification spike — highest risk, must be validated before any feature is built around it.

## Known Issues
- None yet. Monitor LLM API latency when implementing consistency-based confidence scoring.

## Locked Decisions
- **Evaluation Metric:** Inter-rater agreement (Cohen's Kappa) against a two-professor baseline to prove human-level diagnostic performance.
- **Core Engine Flow:** Gap taxonomy is a strict routing system. No free-form LLM reasoning — classification happens before feedback generation.
- **Validation Design:** Loud failure via multiple LLM generations. Low-confidence outputs are flagged, never silently passed to students.
- **Schema Strategy:** Database tables designed per feature via Alembic migrations. No upfront full-schema design.
- **API Contract Strategy:** High-level endpoint map designed once upfront. Detailed Pydantic models written per feature right before building it.
- **Risk Strategy:** RAG + classification pipeline is spiked in isolation before any surrounding infrastructure is built. If it fails, scope is adjusted early.
