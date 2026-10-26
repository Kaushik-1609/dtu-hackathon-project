# DoubtLens Frozen API Contract Specification

> [!IMPORTANT]
> **Contract Version**: 1.0.0 (Frozen)  
> All frontend and backend components communicate over same-origin relative URLs (`/api/...`). No parameter names, payload keys, or endpoint routes may be altered.

---

## 🧭 Endpoints Overview

| Method | Endpoint | Content-Type | Purpose | Auth |
|---|---|---|---|---|
| `GET` | [`/api/health`](#1-get-apihealth) | N/A | Service liveness probe | None |
| `POST` | [`/api/explain`](#2-post-apiexplain) | `multipart/form-data` | Multimodal doubt breakdown (image and/or text) | None |
| `POST` | [`/api/quiz`](#3-post-apiquiz) | `application/json` | Generate 5-question comprehension quiz | None |

---

## 1. GET `/api/health`

Verifies that the Flask web application is alive and ready to process requests.

### Request
```http
GET /api/health HTTP/1.1
Host: localhost:5000
```

### Response (200 OK)
```json
{
  "status": "ok"
}
```

---

## 2. POST `/api/explain`

Submits an educational doubt via image file, text question, or both. Gemma 4 processes the multimodal input and returns a structured step-by-step breakdown.

### Request Headers
```http
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary...
```

### Form Fields

| Field Name | Type | Mandatory? | Valid Values / Constraints | Default |
|---|---|---|---|---|
| `image` | File Binary | Optional* | Formats: `.png`, `.jpg`, `.jpeg`, `.webp`. Maximum size: **5 MB (5,242,880 bytes)**. | `None` |
| `question` | Text String | Optional* | Free text doubt or question prompt. | `""` |
| `language` | Text String | Optional | `"en"` (English) or `"hi"` (Hindi). | `"en"` |
| `level` | Text String | Optional | `"simple"` (layman/foundational) or `"detailed"` (in-depth/rigorous). | `"simple"` |

*\* **Requirement**: At least one of `image` or `question` MUST be provided. If both are omitted, the server returns HTTP 400.*

### Success Response (200 OK)
```json
{
  "topic": "Newton's Second Law of Motion",
  "explanation": "Newton's Second Law states that the acceleration of an object is directly proportional to the net force acting upon it and inversely proportional to its mass (F_net = m * a).",
  "steps": [
    "Identify forces acting on the body: applied pulling force and opposing kinetic friction.",
    "Calculate net horizontal force: F_net = F_pull - f_friction = 20 N - 5 N = 15 N.",
    "Apply Newton's Second Law formula: F_net = m * a.",
    "Solve for acceleration: a = 15 N / 5 kg = 3.0 m/s²."
  ],
  "key_points": [
    "Net force is the vector sum of all forces.",
    "Acceleration direction always aligns with net force.",
    "SI unit of force is the Newton (N = kg·m/s²)."
  ]
}
```

### Hindi Success Response (200 OK)
When `language="hi"`, all output strings are localized into natural Hindi:
```json
{
  "topic": "न्यूटन का गति का दूसरा नियम",
  "explanation": "न्यूटन का दूसरा नियम बताता है कि किसी वस्तु पर लगने वाला कुल बल उसके द्रव्यमान और त्वरण के गुणनफल के बराबर होता है (F_net = m * a)।",
  "steps": [
    "चरण 1: वस्तु पर लग रहे क्षैतिज बलों की पहचान करें (खींचने वाला बल 20 N और घर्षण 5 N)।",
    "चरण 2: कुल परिणामी बल ज्ञात करें: 20 N - 5 N = 15 N।",
    "चरण 3: सूत्र लागू करें: F_net = m * a।",
    "चरण 4: त्वरण ज्ञात करें: 15 N / 5 kg = 3.0 m/s²।"
  ],
  "key_points": [
    "परिणामी बल सभी व्यक्तिगत बलों का सदिश योग होता है।",
    "त्वरण की दिशा हमेशा परिणामी बल की दिशा में होती है।",
    "बल का मानक मात्रक न्यूटन (N) है।"
  ]
}
```

---

## 3. POST `/api/quiz`

Generates an interactive 5-question multiple-choice comprehension quiz strictly based on the generated explanation and topic.

### Request Headers
```http
Content-Type: application/json
```

### Request Body Schema
```json
{
  "topic": "string (required)",
  "explanation": "string (required)",
  "language": "en" | "hi" (optional, default: "en")
}
```

### Success Response (200 OK)
Returns **exactly 5 questions**. Each question contains exactly 4 options, a 0-indexed answer pointer (`answer_index` between 0 and 3), and a concise pedagogical explanation (`why`).

```json
{
  "questions": [
    {
      "q": "What is the formula representing Newton's Second Law of Motion?",
      "options": [
        "F = m / a",
        "F_net = m * a",
        "F = m * v",
        "F = m * a²"
      ],
      "answer_index": 1,
      "why": "Newton's Second Law defines net force as mass multiplied by acceleration (F = m * a)."
    },
    {
      "q": "If a 10 kg box experiences a net force of 50 N, what is its acceleration?",
      "options": [
        "0.2 m/s²",
        "500 m/s²",
        "5 m/s²",
        "25 m/s²"
      ],
      "answer_index": 2,
      "why": "Using a = F / m gives 50 N / 10 kg = 5 m/s²."
    },
    {
      "q": "What direction does an accelerated body move under net force?",
      "options": [
        "Opposite to applied force",
        "In the direction of the net force",
        "Perpendicular to velocity",
        "Always downward"
      ],
      "answer_index": 1,
      "why": "Acceleration vector always points in the same direction as the net force vector."
    },
    {
      "q": "Which of the following is the standard SI unit of force?",
      "options": [
        "Joule",
        "Pascal",
        "Newton",
        "Watt"
      ],
      "answer_index": 2,
      "why": "The Newton (N) is the derived SI unit of force."
    },
    {
      "q": "A forward force is 30 N and friction is 10 N. What is the net force?",
      "options": [
        "40 N",
        "20 N",
        "300 N",
        "3 N"
      ],
      "answer_index": 1,
      "why": "Net force is forward force minus opposing friction: 30 N - 10 N = 20 N."
    }
  ]
}
```

---

## ⚠️ Standardized Error Contract

All error responses across all endpoints adhere to the single unified schema:

```json
{
  "error": "human readable explanation of the failure"
}
```

| HTTP Status | Condition | Example Response Body |
|---|---|---|
| **400 Bad Request** | Neither `image` nor `question` provided in `/api/explain` | `{"error": "At least one of image or question is required."}` |
| **400 Bad Request** | Missing `topic` or `explanation` in `/api/quiz` | `{"error": "Fields 'topic' and 'explanation' are required."}` |
| **400 Bad Request** | Unsupported image file format (not `.png`, `.jpg`, `.jpeg`, `.webp`) | `{"error": "Unsupported file format. Please upload PNG, JPG, or WEBP."}` |
| **413 Payload Too Large** | Uploaded image exceeds 5 MB | `{"error": "Image file exceeds maximum allowable size of 5 MB."}` |
| **500 Server Error** | AI model generation or upstream API failure | `{"error": "Failed to generate explanation. Please try again."}` |

---

## 💻 Invocation Code Snippets

### cURL
```bash
# 1. Multimodal explanation
curl -X POST http://localhost:5000/api/explain \
  -F "image=@samples/physics_newton_law.jpg" \
  -F "question=Explain how to solve this" \
  -F "language=en"

# 2. Quiz generation
curl -X POST http://localhost:5000/api/quiz \
  -H "Content-Type: application/json" \
  -d '{"topic":"Newton Law","explanation":"F=ma","language":"en"}'
```

### JavaScript (`fetch` from Frontend)
```javascript
// Step 1: Explain
const formData = new FormData();
formData.append('image', fileInput.files[0]);
formData.append('question', questionInput.value);
formData.append('language', 'en');
formData.append('level', 'simple');

const explainRes = await fetch('/api/explain', {
  method: 'POST',
  body: formData
});
const explainData = await explainRes.json();

// Step 2: Generate Quiz
const quizRes = await fetch('/api/quiz', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    topic: explainData.topic,
    explanation: explainData.explanation,
    language: 'en'
  })
});
const quizData = await quizRes.json();
```
