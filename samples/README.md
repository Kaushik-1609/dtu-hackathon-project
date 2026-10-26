# DoubtLens Test Samples Directory

This directory contains curated multimodal inputs, test payloads, sample doubt images, and validation scripts designed for testing and demonstrating **DoubtLens** during the Hacktoberfest Hack Day Delhi x SKILLOP DTU hackathon.

---

## 📸 Multimodal Sample Images

The following realistic sample images are provided to test the multimodal capabilities of **Gemma 4** (`gemma-4-31b-it`) via the Gemini API:

| File Name | Subject | Description | File Size | Format |
|---|---|---|---|---|
| [`physics_newton_law.jpg`](./physics_newton_law.jpg) | Physics | Textbook page with a Free Body Diagram ($F_{pull} = 20\text{ N}$, $f = 5\text{ N}$, $m = 5.0\text{ kg}$) and Problem 4.2 text. Matches the default mock scenario! | ~703 KB | JPEG |
| [`handwritten_calculus.jpg`](./handwritten_calculus.jpg) | Mathematics | Handwritten student notebook showing an integration-by-parts calculus doubt: $\int x e^{2x} dx$ with $u$ and $dv$ substitutions. | ~828 KB | JPEG |
| [`circuit_resistors.jpg`](./circuit_resistors.jpg) | Electrical Eng. | Exam problem diagram of a 12V DC circuit with series and parallel resistors asking for equivalent resistance and total current. | ~738 KB | JPEG |

> [!NOTE]
> All sample images are well within the strict **5 MB file size limit** enforced by `/api/explain` and are formatted as standard JPEG files supported by the multimodal API.

---

## 📁 JSON Data Files

- **[`questions.json`](./questions.json)**: A diverse set of student questions across Physics, Chemistry, Math, Biology, and Computer Science in both English (`en`) and Hindi (`hi`).
- **[`quiz_request.json`](./quiz_request.json)**: Sample JSON payload for `POST /api/quiz`.
- **[`mock_explain_response.json`](./mock_explain_response.json)**: The exact schema and mock response returned by `POST /api/explain` when `MOCK=1` (English and Hindi).
- **[`mock_quiz_response.json`](./mock_quiz_response.json)**: The exact 5-question multiple choice schema returned by `POST /api/quiz` when `MOCK=1`.

---

## 🚀 Running Verification & Demo Tests

### 1. Bash / cURL Test Suite (`test_api.sh`)
Run comprehensive endpoint tests against your running server (`http://localhost:5000` or custom port):

```bash
chmod +x samples/test_api.sh
./samples/test_api.sh
```

To test against a custom port:
```bash
PORT=8000 ./samples/test_api.sh
```

### 2. Standalone Python Test Runner (`test_runner.py`)
Run automated schema validation without needing any third-party Python packages (uses standard library `urllib`):

```bash
python3 samples/test_runner.py
```

### 3. Individual cURL Examples

#### Health Check
```bash
curl -X GET http://localhost:5000/api/health
```

#### Multimodal Image Upload (Physics Doubt)
```bash
curl -X POST http://localhost:5000/api/explain \
  -F "image=@samples/physics_newton_law.jpg" \
  -F "question=Find the acceleration of the block" \
  -F "language=en" \
  -F "level=simple"
```

#### Text-Only Question (Hindi)
```bash
curl -X POST http://localhost:5000/api/explain \
  -F "question=न्यूटन का दूसरा नियम क्या है और इसका सूत्र क्या है?" \
  -F "language=hi" \
  -F "level=simple"
```

#### Generate 5-Question Quiz
```bash
curl -X POST http://localhost:5000/api/quiz \
  -H "Content-Type: application/json" \
  -d @samples/quiz_request.json
```
