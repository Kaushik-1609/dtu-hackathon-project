# DoubtLens Documentation Hub

Welcome to the **DoubtLens** documentation repository. Built for **Hacktoberfest Hack Day Delhi x SKILLOP DTU (MLH)**, this documentation suite details the multimodal architecture, Gemma 4 integration, API contract, testing suites, and pitch strategy.

---

## 📚 Documentation Index

| Document | Purpose & Highlights |
|---|---|
| **[`ARCHITECTURE.md`](./ARCHITECTURE.md)** | System architecture diagram (Mermaid), end-to-end data flow, frontend-backend contract separation, and `MOCK=1` resilience engineering. |
| **[`API.md`](./API.md)** | Frozen API contract reference (`/api/health`, `/api/explain`, `/api/quiz`), request/response schemas, error code matrix (400, 413, 500), and cURL/JS code snippets. |
| **[`GEMMA4_INTEGRATION.md`](./GEMMA4_INTEGRATION.md)** | Deep-dive for judges on **"Best Use of Gemma 4"**: multimodal image+text prompt engineering, `google-genai` SDK usage, Hindi Devanagari localization, and structured JSON parsing. |
| **[`PITCH_AND_DEMO.md`](./PITCH_AND_DEMO.md)** | Complete 3-minute hackathon pitch script, live demo walkthrough checklist, prize criteria alignment matrix, and judge Q&A preparation. |
| **[`TESTING.md`](./TESTING.md)** | Quality assurance guide, automated test suite documentation (`test_api.sh`, `test_runner.py`), edge case matrix, and manual acceptance checklist. |
| **[`CONTRIBUTING.md`](./CONTRIBUTING.md)** | Hacktoberfest guidelines, zero-cost development using `MOCK=1`, git workflow, code of conduct, and roadmap / good-first-issues. |

---

## ⚡ Quick Test Commands

Test the DoubtLens server from your command line:

```bash
# 1. Bash cURL Test Suite
chmod +x ../samples/test_api.sh
../samples/test_api.sh

# 2. Python Schema Test Runner
python3 ../samples/test_runner.py
```
