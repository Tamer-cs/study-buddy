# MVP API Contract

This file is the birds-eye endpoint map for the MVP only. Field-level request and response shapes will be defined later, per feature, with Pydantic models.

## Auth

- `POST /auth/register` -> `RegisterRequest`, `RegisterResponse`
- `POST /auth/login` -> `LoginRequest`, `LoginResponse`
- `GET /auth/me` -> `CurrentUserResponse`

## Answers

- `POST /answers` -> `AnswerSubmitRequest`, `AnswerSubmitResponse`
- `GET /answers/{answer_id}/diagnosis` -> `DiagnosisResponse`

## Courses

- `POST /courses` -> `CourseCreateRequest`, `CourseCreateResponse`
- `GET /courses/{course_id}` -> `CourseDetailResponse`

## Analytics

- `GET /analytics/courses/{course_id}` -> `CourseAnalyticsResponse`

## Shared Pydantic Models

- `UserSummary`
- `CourseSummary`
- `AnswerSummary`
- `DiagnosisSummary`
- `ErrorResponse`

## MVP Scope Note

- No question generation, practice mode, or OCR endpoints are included in this MVP contract.