from pydantic import BaseModel
from typing import List


class StudentAnswer(BaseModel):
    question_id: str
    student_id: str
    answer_text: str


class Misconception(BaseModel):
    concept: str
    explanation: str   


class Diagnosis(BaseModel):
    concept: str
    correctness: str
    gap_types: List[str]
    confidence: str
    missing_concepts: List[str]
    misconceptions: List[Misconception]
    incomplete: bool
    feedback_strategy: str
