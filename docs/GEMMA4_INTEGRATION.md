# Gemma 4 Integration Guide (`gemma-4-31b-it`)

Targeting the **"Best Use of Gemma 4"** prize category at **Hacktoberfest Hack Day Delhi x SKILLOP DTU (MLH)**, this document details how DoubtLens harnesses Google's state-of-the-art open-weights model family through the new **`google-genai`** SDK.

---

## 🌟 Why Gemma 4 for Multimodal STEM Learning?

DoubtLens uses `gemma-4-31b-it` (Google Gemma 4, 31 Billion Parameter Instruction-Tuned Multimodal Model) as its primary intelligence engine:

1. **Multimodal Native Processing**: Directly processes image pixels alongside text in a unified transformer backbone. It interprets complex free-body diagrams, circuit schematics, and handwritten mathematical symbols without requiring a separate fragile OCR step.
2. **STEM & Mathematical Reasoning**: Excels at chain-of-thought mathematical derivation, vector analysis, and formula applications.
3. **True Bilingual Competence (English & Hindi)**: Generates high-fidelity native Devanagari Hindi explanations rather than mechanical literal translations.
4. **Open-Weights Spirit**: Gemma embodies the open-source AI movement, making DoubtLens 100% aligned with the hackathon's "Best Open-Source AI Project" theme.

---

## 🛠️ SDK & Client Architecture (`google-genai`)

DoubtLens utilizes the official Google GenAI Python SDK (`from google import genai`):

```python
from google import genai
from google.genai import types
import os

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
model_name = os.environ.get("GEMMA_MODEL", "gemma-4-31b-it")
```

### Multimodal Call Pattern
```python
# Ingest image bytes and student query
parts = []
if image_bytes:
    parts.append(
        types.Part.from_bytes(
            data=image_bytes,
            mime_type=image_mime_type  # "image/jpeg", "image/png", etc.
        )
    )

if student_question:
    parts.append(student_question)

# Generate structured pedagogical explanation
response = client.models.generate_content(
    model=model_name,
    contents=parts,
    config=types.GenerateContentConfig(
        system_instruction=SYSTEM_PROMPT,
        temperature=0.2,       # Low temperature ensures deterministic JSON formatting
        response_mime_type="application/json"
    )
)
```

---

## 🧠 Prompt Engineering for Socratic Pedagogy

### 1. Explanation System Instruction
To prevent Gemma 4 from jumping straight to the final answer (which hinders student learning), our prompt enforces a structured, step-by-step pedagogical breakdown:

```text
You are DoubtLens, an expert, patient STEM tutor powered by Gemma 4.
Your goal is to help students truly master concepts by breaking down problems step by step.

INPUT REQUIREMENTS:
- You may receive an image (textbook photo, handwritten notes, or diagram), a text question, or both.
- If an image is provided, carefully read any text, formulas, diagrams, and force vectors.
- Target language: {language} ("en" for English, "hi" for Hindi).
- Target pedagogical depth: {level} ("simple" for high-school/foundational, "detailed" for university/rigorous).

STRICT OUTPUT FORMAT:
You MUST respond with a single valid JSON object with EXACTLY these keys:
{
  "topic": "Concise topic title",
  "explanation": "Clear, intuitive 2-3 sentence overview of the core principle",
  "steps": [
    "Step 1: Identify given variables and context",
    "Step 2: Formula and principle application",
    "Step 3: Step-by-step arithmetic / derivation",
    "Step 4: Final answer with units and physical intuition"
  ],
  "key_points": [
    "Bullet 1: Fundamental takeaway",
    "Bullet 2: Common student misconception to avoid",
    "Bullet 3: SI units or critical rule"
  ]
}

BILINGUAL INSTRUCTION (When language is 'hi'):
- Output entirely in natural, fluent Hindi written in standard Devanagari script.
- Maintain accurate scientific terminology (e.g., 'त्वरण' for acceleration, 'परिणामी बल' for net force, 'द्रव्यमान' for mass).
```

### 2. Quiz Generation System Instruction
After understanding the doubt, students reinforce their memory using the "Test me" button. We instruct Gemma 4 to formulate **exactly 5 diagnostic questions**:

```text
You are DoubtLens Quiz Master powered by Gemma 4.
Generate a 5-question multiple choice diagnostic quiz based STRICTLY on this topic and explanation:
Topic: {topic}
Explanation: {explanation}
Language: {language} ("en" or "hi")

CRITICAL CONSTRAINTS:
1. Exactly 5 questions.
2. Exactly 4 plausible options per question (no silly distractors; simulate realistic student errors).
3. "answer_index" must be an integer between 0 and 3 pointing to the correct choice.
4. "why" must be a concise, one-sentence explanation of why that choice is correct.

JSON OUTPUT SCHEMA:
{
  "questions": [
    {
      "q": "Question text?",
      "options": ["Option A", "Option B", "Option C", "Option D"],
      "answer_index": 0,
      "why": "Clear explanation of the correct choice."
    }
  ]
}
```

---

## 🛡️ Defensive JSON Extraction & Resilience

While Gemma 4 natively supports structured outputs, real-world network clients must defensively handle potential markdown wrapper fences (` ```json `):

```python
import json
import re

def sanitize_and_parse_json(raw_text: str) -> dict:
    """Robustly strips markdown fences and parses JSON payload."""
    text = raw_text.strip()
    
    # Remove markdown code fences if present
    match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text)
    if match:
        text = match.group(1).strip()
        
    try:
        return json.loads(text)
    except json.JSONDecodeError as err:
        # Fallback or normalized error response
        raise ValueError(f"Model response was not valid JSON: {err}")
```

---

## ⚡ Performance & Hackathon Optimization

1. **Deterministic Mock Fallback (`MOCK=1`)**:
   During judging, if the live Gemini API is rate-limited or Wi-Fi drops, DoubtLens instantly switches to `MOCK=1` without altering any endpoint contract, guaranteeing an uninterrupted demo.
2. **Zero Overhead Preprocessing**:
   Images are streamed directly as binary buffers to Gemma 4 via `types.Part.from_bytes()`, avoiding disk I/O bottlenecks.
3. **Low Temperature Tuning (`temperature=0.2`)**:
   Ensures consistent JSON schema compliance, high factual accuracy in mathematics, and minimizes hallucinated steps.
