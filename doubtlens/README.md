# DoubtLens 🔍⚡

> **Instant Multimodal Doubt Solving & Mastery Testing Powered by Google Gemma 4**  
> *Built in 3 hours for Hacktoberfest Hack Day Delhi × SKILLOP DTU (MLH)*

[![Hackathon: MLH](https://img.shields.io/badge/Hackathon-MLH%20%C3%97%20Hacktoberfest-ff4088?style=flat-square)](https://mlh.io)
[![Model: Gemma 4](https://img.shields.io/badge/Model-Gemma%204%20(31B--IT)-4285F4?style=flat-square&logo=google)](https://ai.google.dev/gemma)
[![Python: 3.11](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Backend: Flask](https://img.shields.io/badge/Backend-Flask-000000?style=flat-square&logo=flask)](https://flask.palletsprojects.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-Welcome-brightgreen.svg?style=flat-square)](CONTRIBUTING.md)

---

## 🎯 Target Hackathon Prizes

1. **🏆 Best Use of Gemma 4**
   - **True Multimodality**: Deep visual reasoning over handwritten equations, complex physics/chemistry diagrams, and dense textbook pages via the Gemini API (`google-genai`).
   - **Bilingual Step-by-Step Pedagogy**: High-fidelity structured explanations in both **English** and **Hindi**, making STEM education accessible to millions of vernacular learners.
   - **Dual Explanation Depth**: Dynamic `simple` (intuitive conceptual grasp) and `detailed` (rigorous derivations and edge cases) modes.
   - **Interactive Mastery Loop ("Test Me")**: Synthesizes a focused 5-question diagnostic multiple-choice quiz directly from the analyzed concept, providing instant pedagogical reinforcement with rationale breakdowns.

2. **🌟 Best Open-Source AI Project**
   - **Zero Vendor Lock-in & Lightweight**: Pure Vanilla HTML/CSS/JS frontend with zero bloated npm dependencies. Highly responsive and blisteringly fast.
   - **Reproducible & Containerized**: Ready-to-deploy Docker runtime, Gunicorn production server, and frozen API specifications.
   - **Zero-Barrier Evaluation (Mock Mode)**: Integrated mock engine (`MOCK=1`) allowing offline evaluation, continuous testing, and judge demonstrations with zero API key configuration.

---

## 🏗️ System Architecture & Tech Stack

```
                     ┌───────────────────────────────────────────────┐
                     │          Browser Client (Vanilla Web)         │
                     │  - Pure HTML5 / CSS3 / Vanilla JavaScript     │
                     │  - Zero Frameworks, Zero NPM Dependencies     │
                     └───────────────────────┬───────────────────────┘
                                             │  HTTP (Same-Origin)
                                             ▼
                     ┌───────────────────────────────────────────────┐
                     │            Flask API Gateway (3.11)           │
                     │  - Input Validation (Max 5MB PNG/JPG/WebP)    │
                     │  - Language Routing (English / Hindi)         │
                     │  - Mock Fallback Engine (MOCK=1)              │
                     └───────────────────────┬───────────────────────┘
                                             │
                       ┌─────────────────────┴─────────────────────┐
                       │ (MOCK=0)                                  │ (MOCK=1)
                       ▼                                           ▼
         ┌───────────────────────────┐               ┌───────────────────────────┐
         │       Gemma 4 Client      │               │   Mock Pedagogical Data   │
         │ - google-genai SDK        │               │ - Newton's Second Law     │
         │ - Model: gemma-4-31b-it   │               │ - Deterministic 5Q Quiz   │
         │ - Multimodal Vision + Text│               │ - Offline Resilience      │
         └───────────────────────────┘               └───────────────────────────┘
```

- **Backend**: Python 3.11, Flask, `flask-cors`, `google-genai`, `python-dotenv`, `gunicorn`
- **Frontend**: Plain HTML5, CSS3, Modern ES6+ JavaScript, Google Fonts (Outfit / Inter)
- **AI Engine**: Google Gemma 4 (`gemma-4-31b-it`) via Google Gemini API
- **DevOps**: Docker (`python:3.11-slim`), Procfile (Heroku / Render / Railway)

---

## 👥 4-Person Hackathon Team Ownership

| Teammate | Focus Area | Owned Files |
| :--- | :--- | :--- |
| **Mayank** | Core Backend & AI Integration | `doubtlens/app.py`, `doubtlens/gemma_client.py` |
| **Harsh** | Frontend UI & User Experience | `doubtlens/templates/index.html`, `doubtlens/static/style.css`, `doubtlens/static/app.js` |
| **Kaushik** | DevOps, Tooling & Infrastructure | `requirements.txt`, `.env.example`, `.gitignore`, `Dockerfile`, `Procfile`, `README.md`, `LICENSE` |
| **Utkarsh** | Test Assets & Documentation | `doubtlens/samples/*`, `doubtlens/docs/*` |

---

## 📡 Frozen API Specification

Frontend and backend communicate via relative paths on the same origin.

### 1. Health Check
```http
GET /api/health
```
**Response (200 OK):**
```json
{
  "status": "ok"
}
```

---

### 2. Explain Problem / Concept
```http
POST /api/explain
Content-Type: multipart/form-data
```

**Request Parameters:**
| Field | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `image` | File | Optional* | Image file (`png`, `jpg`, `jpeg`, `webp`). Max 5 MB. |
| `question` | Text | Optional* | Typed doubt, prompt, or question context. |
| `language` | Text | Optional | `"en"` (default) or `"hi"` (Hindi). |
| `level` | Text | Optional | `"simple"` (default) or `"detailed"`. |

*\* At least one of `image` or `question` is required.*

**Success Response (200 OK):**
```json
{
  "topic": "Newton's Second Law of Motion",
  "explanation": "Newton's Second Law describes how the velocity of an object changes when it is subjected to an external force...",
  "steps": [
    "Step 1: Identify given forces and mass.",
    "Step 2: Formulate F_net = m * a.",
    "Step 3: Resolve vector components along the axis of acceleration.",
    "Step 4: Solve for the target variable."
  ],
  "key_points": [
    "Force is directly proportional to acceleration.",
    "Mass represents inertial resistance to acceleration.",
    "SI Unit of Force is the Newton (1 N = 1 kg·m/s²)."
  ]
}
```

---

### 3. Generate Mastery Quiz
```http
POST /api/quiz
Content-Type: application/json
```

**Request Body:**
```json
{
  "topic": "Newton's Second Law of Motion",
  "explanation": "Newton's Second Law describes how the velocity of an object changes...",
  "language": "en"
}
```

**Success Response (200 OK):**
```json
{
  "questions": [
    {
      "q": "What happens to the acceleration of an object if the applied net force is doubled while mass remains constant?",
      "options": [
        "Acceleration is halved",
        "Acceleration is doubled",
        "Acceleration remains unchanged",
        "Acceleration quadruples"
      ],
      "answer_index": 1,
      "why": "According to F = ma, acceleration is directly proportional to net force for a constant mass."
    }
    // Exactly 5 structured questions
  ]
}
```

---

### 4. Standardized Error Format
All endpoints return standard JSON errors:
```json
{
  "error": "Human readable description of the error"
}
```
- `400 Bad Request`: Missing both image and question, or malformed JSON payload.
- `413 Payload Too Large`: Uploaded image exceeds 5 MB.
- `500 Internal Server Error`: AI inference or server failure.

---

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.11 installed
- Git
- Google Gemini API Key ([Get one here](https://aistudio.google.com/)) *(Optional if running in Mock mode)*

### 1. Clone & Set Up Environment

```bash
# Clone the repository
git clone https://github.com/Kaushik-1609/dtu-hackathon-project.git
cd dtu-hackathon-project

# Create and activate a Python 3.11 virtual environment
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies (strictly restricted to authorized stack)
pip install -r requirements.txt
```

### 2. Configure Environment Variables

```bash
# Copy template configuration
cp .env.example .env
```

Edit `.env` to configure your settings:
```ini
GEMINI_API_KEY=your_actual_api_key_here
GEMMA_MODEL=gemma-4-31b-it
PORT=5000
MOCK=1  # Set to 0 to use live Gemma 4 model
```

### 3. Run the Application

#### Option A: Local Development Server
```bash
python app.py
```
Visit `http://localhost:5000` in your browser.

#### Option B: Production Server with Gunicorn
```bash
gunicorn --bind 0.0.0.0:5000 --workers 2 --threads 4 app:app
```

---

## 🐳 Docker Deployment

DoubtLens includes an optimized multi-stage container configuration based on `python:3.11-slim`:

```bash
# Build Docker image
docker build -t doubtlens:latest .

# Run container (Mock mode enabled by default)
docker run -d -p 5000:5000 --name doubtlens-app doubtlens:latest

# Or run with live Gemini API Key
docker run -d -p 5000:5000 \
  -e GEMINI_API_KEY="your_api_key_here" \
  -e MOCK=0 \
  --name doubtlens-live doubtlens:latest
```

Check container health:
```bash
curl http://localhost:5000/api/health
```

---

## 🧪 Mock Mode for Demos & Testing

When running with `MOCK=1`:
- `/api/explain` immediately returns a complete explanation of **Newton's Second Law** (with step-by-step breakdown and key points, automatically translated if `language=hi`).
- `/api/quiz` immediately returns 5 realistic, validated diagnostic questions with answer indices and pedagogical rationale.
- Perfect for judging environments, rapid frontend testing, and quota conservation!

---

## 🛡️ Security & Open-Source Best Practices

- **Strict Secret Management**: `.env` is explicitly ignored in `.gitignore`. Secrets are never committed or logged.
- **Payload Validation**: Strict MIME-type checking and 5 MB cap on image uploads.
- **Least-Privilege Docker**: Container executes under a dedicated non-root `doubtlens` user.
- **MIT License**: Completely open-source and permissible for community expansion.

---

## 🤝 Contributing (Hacktoberfest)

Contributions are warmly welcomed! Please adhere to our guidelines:
1. Fork the repo and create your feature branch: `git checkout -b feature/awesome-feature`
2. Follow PEP 8 guidelines for Python code.
3. Keep frontend lightweight with zero external npm dependencies.
4. Ensure all frozen API contracts remain backwards-compatible.
5. Open a Pull Request with a clear description of your changes.

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.
