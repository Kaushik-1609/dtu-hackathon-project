# DoubtLens Quality Assurance & Testing Guide

This guide details the testing procedures for **DoubtLens** to ensure high reliability, contract compliance, and smooth live demonstrations during **Hacktoberfest Hack Day Delhi x SKILLOP DTU (MLH)**.

---

## 🎯 Testing Objectives

1. **Frozen API Contract Compliance**: Guarantee all request/response keys, types, and HTTP status codes match the frozen specification.
2. **Multimodal Payload Ingestion**: Verify image handling (`.png`, `.jpg`, `.webp`), boundary limits (5 MB limit), and text-only queries.
3. **Bilingual Delivery**: Ensure correct localization in English (`en`) and Hindi (`hi`).
4. **Quiz Engine Integrity**: Verify exactly 5 multiple choice questions with valid answer pointers (`0-3`) and explanatory rationales.
5. **Mock Mode Parity**: Ensure `MOCK=1` replicates live AI responses deterministically.

---

## 🧪 Automated Test Suites

### 1. Bash / cURL Test Suite (`samples/test_api.sh`)
Quick smoke tests designed for Linux/macOS terminals and CI pipelines.

```bash
# Make script executable
chmod +x samples/test_api.sh

# Run against default port 5000
./samples/test_api.sh

# Or run against custom port
PORT=8000 ./samples/test_api.sh
```

**Coverage**:
- `GET /api/health` $\rightarrow$ Checks for `{"status":"ok"}` (HTTP 200).
- `POST /api/explain` (Text only, English) $\rightarrow$ Verifies topic, explanation, steps, key points.
- `POST /api/explain` (Image upload) $\rightarrow$ Verifies multimodal ingestion of `physics_newton_law.jpg`.
- `POST /api/explain` (Hindi) $\rightarrow$ Verifies Devanagari output generation.
- `POST /api/quiz` $\rightarrow$ Verifies quiz generation schema.
- `POST /api/explain` (Empty input) $\rightarrow$ Verifies HTTP 400 Bad Request error handling.

---

### 2. Python Contract Schema Validator (`samples/test_runner.py`)
A rigorous schema validation script using only Python's standard library:

```bash
python3 samples/test_runner.py
```

**Validations Performed**:
| Test Case | Method & Route | Validation Rule |
|---|---|---|
| **Health Probe** | `GET /api/health` | Returns status 200 and JSON `{"status": "ok"}` |
| **Text-only Explain** | `POST /api/explain` | Returns `topic` (str), `explanation` (str), `steps` (list), `key_points` (list) |
| **Multimodal Explain** | `POST /api/explain` | Binary multipart stream of JPEG file succeeds with status 200 |
| **Quiz Generation** | `POST /api/quiz` | Returns **exactly 5 questions**; each has `q` (str), `options` (array of length 4), `answer_index` (int between 0 and 3), and `why` (str) |
| **Empty Input Check** | `POST /api/explain` | Returns status 400 and JSON `{"error": ...}` |

---

## 🔍 Edge Case & Error Handling Scenarios

| Scenario | Input | Expected Status | Expected Behavior |
|---|---|---|---|
| **Empty Submission** | Form data with neither `image` nor `question` | `400 Bad Request` | Returns `{"error": "At least one of image or question is required."}` |
| **Oversized Image** | Image file $> 5\text{ MB}$ | `413 Payload Too Large` | Returns `{"error": "Image file exceeds maximum allowable size of 5 MB."}` |
| **Unsupported Extension** | File ending in `.exe`, `.pdf`, or `.txt` in `image` field | `400 Bad Request` | Returns `{"error": "Unsupported file format..."}` |
| **Missing Quiz Field** | JSON body without `explanation` | `400 Bad Request` | Returns `{"error": "Fields 'topic' and 'explanation' are required."}` |
| **Upstream API Failure** | Invalid API key or network timeout | `500 Server Error` | Returns graceful JSON `{"error": "Failed to generate explanation. Please try again."}` |

---

## 🖥️ Manual Frontend Acceptance Checklist

Before presenting to hackathon judges, verify the following user interactions:

1. [ ] **Page Load**: Open `http://localhost:5000/`. Confirm clean layout, Google Fonts loaded, and responsive styling.
2. [ ] **Drag & Drop / Image Selection**: Select [`samples/physics_newton_law.jpg`](../samples/physics_newton_law.jpg). Confirm thumbnail preview displays cleanly.
3. [ ] **Language Selection**: Toggle between English and Hindi.
4. [ ] **Level Selection**: Toggle between Simple and Detailed.
5. [ ] **Loading State**: Submit a doubt. Confirm loading spinner or progress text appears during inference.
6. [ ] **Step Breakdown Rendering**: Confirm steps appear in orderly sequence with clear numbered cards.
7. [ ] **Key Points Section**: Confirm highlighted takeaway bullet points render clearly.
8. [ ] **Quiz Activation**: Click "Test me". Confirm 5 multiple-choice questions render with 4 distinct options each.
9. [ ] **Instant Feedback**: Click an answer option. Confirm immediate color feedback (green for correct, red for incorrect) and explanation disclosure.
10. [ ] **Score Display**: Answer all 5 questions and confirm summary score (e.g., "Score: 4/5") is calculated.
