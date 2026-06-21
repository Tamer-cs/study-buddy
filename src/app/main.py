from fastapi import FastAPI
from src.app.schemas import StudentAnswer, Diagnosis

app = FastAPI(title="Study-Buddy API")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/analyze", response_model=Diagnosis)
def analyze(answer: StudentAnswer):
    # Placeholder implementation; real logic will call the gap classifier and RAG retrieval
    return Diagnosis(
        concept="",
        correctness="unknown",
        gap_types=[],
        confidence="low",
        missing_concepts=[],
        misconceptions=[],
        incomplete=True,
        feedback_strategy=""
    )
