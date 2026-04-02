# Study-Buddy — Cognitive Gap Detection System

This project is developed as a senior capstone project in Computer Science. It is an end-to-end AI system that analyzes student answers, identifies **why** they are wrong (not just whether), classifies cognitive gaps using a **universal gap taxonomy**, and delivers targeted, course-grounded remediation.

The same core reasoning engine supports both **students** and **professors**, with role-specific interfaces and aggregated analytics.

---

## Problem Statement

Most educational tools focus on **grading correctness** or **content generation**.  
They fail at the hardest and most valuable problem:

> Diagnosing reasoning gaps and explaining what is missing in a student's understanding.

As a result:
- Students repeat mistakes without understanding the root cause
- Professors lack visibility into systemic misconceptions
- Feedback is shallow, generic, or purely score-based

This project addresses that gap.

---

## Why Study-Buddy is Novel

Existing AI tutors (Khanmigo, ChatGPT) guide students toward answers but do not diagnose **why reasoning fails**. They are course-agnostic — they reason from general training data, not from what was actually taught.

Study-Buddy addresses a different problem: given a student's answer to an exam question, grounded in their **specific course material**, classify the cognitive gap type and deliver feedback that teaches the thinking process that fills **that exact gap** — not just the correct answer.

| | Existing Tools | Study-Buddy |
|---|---|---|
| Feedback style | Answer-oriented | Process-oriented |
| Knowledge source | General training data | Course-specific materials |
| Gap diagnosis | None | Structured gap taxonomy |
| Analytics | None | Class-level concept breakdowns |

---

## Core Idea

The system is built around a **gap taxonomy that acts as a routing system**. the system:

1. **Classifies the gap type** from a structured taxonomy given the student's answer
2. **Routes to concept-specific feedback** grounded in the actual course material covering that exact gap
3. **Aggregates results** across students to surface class-level weaknesses at the concept level

This two-step approach — classify first, then retrieve and generate — keeps the LLM strictly constrained and makes feedback highly targeted.

---

## Universal Gap Taxonomy

All analyses are expressed using a domain-agnostic taxonomy. The taxonomy serves as a **routing system**: each gap type maps to a specialized feedback strategy.

### Conceptual Confusion → Clarify via Contrast and Analogy
The student confuses related concepts within a domain.
- Examples: Heap vs BST, TCP vs UDP, normalization forms

### Procedural Application Gap → Walk Through the Process Step by Step
The student knows the concept but cannot apply it correctly.
- Examples: Incorrect algorithm steps, failure to trace execution, inability to translate a concept into a procedure

### Intuition / "Why" Gap → Force Justification, Expose the Reasoning
The student gives a correct answer without correct reasoning — memorization without understanding.
- Examples: Cannot justify a design decision, cannot explain why an algorithm works

### Incomplete Understanding → Identify Where Reasoning Stopped, Push From There
Partial reasoning with missing steps or unhandled edge cases. Can co-exist with other gap types.

Multiple gap types may apply to a single answer.

---

## Concept-Level Tagging

Each chapter in the course material is decomposed into **underlying concepts** (e.g., heap property, pointer arithmetic, normal forms). When a student submits an answer, the system identifies:

1. The **concept** the question is testing
2. The **gap type** the student's answer reveals

This combination gives the LLM tightly scoped, optimized guidelines for feedback generation, and enables far more precise analytics.

**Example:** Instead of reporting "60% of students have intuition gaps," the professor dashboard reports "60% of students have intuition gaps **on heaps**."

---

## System Architecture

```
flowchart TD
    A[Student / Professor Interface] --> B[API Layer - FastAPI]
    B --> C[Gap Classification Engine]

    C --> D[Concept Identifier]
    C --> E[Student Answer Analysis]

    E --> F[OCR Adapter if handwritten]
    F --> E

    D --> G[RAG Retrieval - concept-scoped course material]
    G --> H[LLM Feedback Generator - gap-type constrained]

    H --> I[Structured Diagnosis Output]
    I --> J[Feedback and Remediation - Student]
    I --> K[Analytics and Aggregation - Professor]

    J --> A
    K --> A
```

The system follows a clean, layered architecture:

```
Frontend (Student / Professor)
        |
        v
   API Layer (FastAPI)
        |
        v
Gap Classification Engine (LLM-based, taxonomy-constrained)
        |
        v
  RAG Retrieval (concept-scoped, course-grounded)
        |
        v
   Data Layer (Courses, Answers, Gaps, Concepts)
```

OCR is treated as a **lossy input adapter**, not part of the core intelligence.

---

## LLM Validation System

To prevent Study-Buddy from becoming a simple LLM wrapper, the system enforces three layers of validation:

### 1. RAG-Grounded Generation
Feedback is generated strictly from retrieved course material relevant to the identified concept. The LLM cannot reason from general training data, it is constrained to the uploaded slides and materials.

### 2. Consistency-Based Confidence Scoring
For each diagnosis, the system generates multiple independent answers and measures their agreement. High agreement → high confidence output. Low agreement → flagged as low confidence, surfaced for review.

### 3. Loud Failure by Design
Hallucinations are inevitable. The system is designed so that when they occur, they **fail loudly** flagged, labeled, and surfaced rather than silently producing confident-sounding wrong feedback. Low-confidence outputs are never silently passed to students.

---

## Evaluation Methodology

To validate system performance rigorously, Study-Buddy will be evaluated against human performance using inter-rater agreement.

**Protocol:**
1. Two professors independently classify a set of student answers using the gap taxonomy
2. Inter-rater agreement between the two professors is measured (e.g., Cohen's Kappa)
3. Study-Buddy's classifications are compared against the agreed ground truth
4. System accuracy is benchmarked against human-level agreement

If Study-Buddy's agreement with the ground truth matches or exceeds the inter-professor agreement, this constitutes evidence of human-level diagnostic performance.

---

## Key Features

### Professor Features
- Upload course materials (PDFs / slides)
- Generate practice questions
- Generate exams
- View aggregated analytics:
  - Most frequent misconceptions by concept
  - Concept-level failure rates
  - Distribution of gap types per topic
  - Low-confidence diagnoses flagged for review

### Student Features
- Request practice questions or mock exams
- Submit answers (typed text or handwritten images)
- Receive structured feedback explaining:
  - The gap type identified in their reasoning
  - What is missing and where their reasoning stopped
  - Which concept to revisit and how
  - How to fill the specific gap (contrast, justification, step-by-step walkthrough, etc.)

---

## OCR Support (Scoped)

Handwritten answers are supported under explicit constraints:

- Text-only handwriting
- Single language
- No diagrams
- No complex mathematical notation

OCR output is treated as **best-effort text**. Uncertainty is tolerated and handled downstream by the reasoning engine.

---

## Core Intelligence: Gap Classification and Feedback Engine

### Inputs
- Question
- Student answer (typed or OCR output)
- Identified concept (from concept tagging)
- Relevant course material (retrieved via RAG, scoped to concept)

### Step 1 — Gap Classification
The LLM is constrained to classify the student's answer into one or more gap types from the taxonomy. No free-form reasoning at this stage.

### Step 2 — Targeted Feedback Generation
The LLM generates feedback using:
- The classified gap type (determines the feedback strategy)
- The retrieved course material (grounds the feedback in what was actually taught)
- The identified concept (scopes the retrieval and the feedback)

### Output (Structured JSON)
```json
{
  "concept": "heap property",
  "correctness": "incorrect",
  "gap_types": ["Conceptual Confusion", "Procedural Application Gap"],
  "confidence": "high",
  "missing_concepts": ["heap property vs BST ordering"],
  "misconceptions": [
    {
      "concept": "heap vs BST",
      "explanation": "The student assumes ordering guarantees across siblings, which applies to BSTs but not heaps."
    }
  ],
  "incomplete": true,
  "feedback_strategy": "Clarify distinction via contrast and analogy, then walk through insertion step by step."
}
```

---

## Future Improvements

The following features are out of scope for the current capstone but represent promising directions for future development:

**On-Demand Video Generation**  
For visual learners, short explanatory video clips could be generated on the spot for each diagnosed gap. This would require significant infrastructure (video synthesis pipeline, storage, delivery) and would likely be offered as a paid subscription feature.

**Dynamic Practice Question Difficulty**  
The system could adaptively adjust the difficulty of practice questions based on a student's gap history and performance trends. As gaps are resolved, harder questions targeting deeper understanding of the same concept would be introduced automatically.

**General Study Assistant Features**
Beyond gap diagnosis, Study-Buddy could expand into broader study support utilities:

- **Summarization** — generate concise summaries of uploaded course materials, broken down by chapter or concept
- **Flashcard Generation** — automatically produce flashcard sets from slides, targeting key definitions, distinctions, and concept relationships
- **Concept Mind Maps** — visualize how concepts within a chapter relate to each other, helping students see the bigger picture before drilling into details
- **Study Schedule Planner** — given an exam date and a set of concepts, generate a personalized revision plan weighted by the student's known gap history
- **Question Bank Browser** — let students browse and filter past practice questions by concept, gap type, or difficulty

---

## Dependencies

- **FastAPI** — API layer
- **LLM API** — Gap classification and feedback generation
- **Vector database** — RAG retrieval (e.g., Pinecone, Chroma)
- **OCR engine** — Handwritten answer preprocessing (e.g., Tesseract, Google Vision)
- **PostgreSQL / equivalent** — Courses, answers, gap records, concept tags