# DoubtLens — MLH Hackathon Submission

**Project Name:** DoubtLens  
**Tagline:** Snap your doubt, master the concept — Bilingual multimodal STEM tutor with instant active-recall quizzes powered by Gemma 4.

---

## 🚀 Description

### Inspiration
Every student has experienced the frustration of getting stuck on a textbook problem, circuit diagram, or handwritten math derivation late at night with no tutor around. While modern LLMs can chat, general conversational bots either hallucinate arithmetic, skip foundational steps, or drown students in text walls without testing if they actually grasped the concept. Furthermore, millions of students across India learn in vernacular languages, yet high-quality STEM tutoring is overwhelmingly restricted to English. We built **DoubtLens** to bridge this gap: an open, accessible, bilingual AI companion that turns passive confusion into active conceptual mastery in seconds.

### What It Does
1. **Multimodal Doubt Ingestion**: Students snap or upload a photo of a printed textbook page, messy handwritten math problem, or complex diagram (or type a query).
2. **Pedagogical Step-by-Step Breakdown**: Powered by `gemma-4-31b-it`, DoubtLens delivers a Socratic explanation: core principle overview, step-by-step reasoning/derivation, and key conceptual takeaways with units and common traps to avoid.
3. **Bilingual Vernacular Tutoring**: Seamlessly switches between simple English and natural Devanagari Hindi with accurate scientific and mathematical terminology.
4. **Active Recall "Test Me" Quiz**: Generates an instant, topic-specific 5-question multiple-choice diagnostic quiz with immediate feedback and pedagogical explanations for every option.

### How We Built It
- **AI & Multimodal Core**: Integrated Google's `gemma-4-31b-it` via the new `google-genai` SDK, passing raw image bytes alongside structured pedagogical prompts with `response_mime_type="application/json"` for deterministic parsing.
- **Backend**: Lightweight Python 3.11 Flask service with strict input sanitization, multipart/form-data image processing, and a built-in mock engine (`MOCK=1`) for robust zero-cost testing.
- **Frontend**: Clean, lightning-fast vanilla HTML5, CSS3, and modern JavaScript without framework bloat or third-party runtime dependencies.
- **Resilience Engineering**: Offline fallback modes, strict contract validation, and high-DPI multimodal test datasets.

### Challenges We Ran Into
- **Prompting for True Pedagogy vs. Direct Answers**: Raw LLMs tend to blurt out $x = 5$ immediately. We carefully engineered prompts with strict step hierarchies (Identify Given $\to$ Principle Formula $\to$ Step Derivation $\to$ Physical Units) to cultivate genuine understanding.
- **Vernacular STEM Terminology in Hindi**: Standard machine translations often transliterate or butcher technical physics concepts. We leveraged Gemma 4's native multilingual fluency to generate authentic Hindi Devanagari explanations retaining precise terms (e.g., त्वरण for acceleration, परिणामी बल for net force).
- **Enforcing Strict JSON Output**: Ensuring the quiz endpoint consistently yielded exactly 5 questions with 4 options and valid integer answer indices under hackathon latency constraints.

### Accomplishments That We're Proud Of
- Delivered a functional, end-to-end multimodal AI application in under 3 hours.
- Zero external CSS/JS framework dependencies — sub-second client-side load times.
- Native bilingual support (English and Hindi) with zero translation latency.
- Full offline developer resilience: `MOCK=1` mode allows anyone in the open-source community to build and test DoubtLens without an API key or incurring cloud costs.

### What We Learned
- How to harness Google's latest `google-genai` SDK for multimodal image-and-text reasoning.
- The power of Socratic prompt constraints for pedagogical applications versus standard chatbots.
- Streamlined team modularity under high-pressure hackathon time constraints through frozen API contracts.

### What's Next for DoubtLens
- **Voice-First Vernacular Q&A**: Speech-to-text input and audio explanations in regional Indian dialects.
- **Edge Deployment**: Running distilled Gemma open-weights models directly on low-cost devices or classroom Raspberry Pis via llama.cpp or Ollama.
- **Spaced Repetition & Weakness Tracking**: Local browser-persisted flashcards based on quiz questions students answered incorrectly.

---

## 🛠️ Technologies
Gemma 4, Gemini API, Python, Flask, HTML, CSS, JavaScript

---

## 🏆 Category Nominations

### Best Use of Gemma 4
DoubtLens exemplifies a **focused AI tool for learning** built through **rapid prototyping** on Google's open-weights model family. Instead of an unconstrained generic chat interface, DoubtLens uses `gemma-4-31b-it` for deep **multimodal** comprehension across printed textbook pages, handwritten student derivations, and circuit schematics. Gemma 4's native bilingual capabilities allow instantaneous switching between English and Devanagari Hindi without losing scientific rigor. Furthermore, Gemma 4 reliably emits structured JSON for a 5-question active recall diagnostic quiz, turning visual doubts into comprehensive learning loops.

### Best Open-Source AI Project
Open-source accessibility is in DoubtLens's DNA. Powered by Google's open-weights Gemma 4 model and distributed under the permissive **MIT License**, DoubtLens is architected to prevent vendor lock-in. The backend model identifier is fully configurable (`GEMMA_MODEL`), allowing students, teachers, and schools to run DoubtLens against self-hosted local Gemma instances (via Ollama or vLLM) with zero ongoing API costs. The codebase is thoroughly documented, modular, features an offline development mode (`MOCK=1`), and includes curated `good-first-issue` roadmaps for Hacktoberfest contributors.

---

## 🤖 AI Coding Tools Used
<!-- NOTE FOR UTKARSH: Fill in the specific tools used below (e.g., Antigravity IDE, Gemini Code Assist, GitHub Copilot, Claude, Cursor, etc.) -->
- [Fill in your tools here, e.g., Antigravity IDE with Gemini 3.8 Flash]
