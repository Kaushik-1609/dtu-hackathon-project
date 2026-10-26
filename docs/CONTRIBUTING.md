# Contributing to DoubtLens

Welcome to **DoubtLens**! We are thrilled that you want to contribute. This project was created during **Hacktoberfest Hack Day Delhi x SKILLOP DTU (MLH)** with a mission to make multimodal STEM tutoring open, accessible, and multilingual.

Whether you are fixing a bug, adding a new language, improving accessibility, or adding test cases, your contributions are welcome!

---

## 🎃 Hacktoberfest Participation

DoubtLens is 100% committed to open source. We tag issues suitable for new contributors with the `good-first-issue` and `hacktoberfest` labels.

### Zero-Cost Development: Hack Without an API Key!
You **do not need a Google Gemini API key** to contribute to DoubtLens! Simply set the environment variable:
```bash
export MOCK=1
```
In mock mode, the backend returns realistic pre-canned data for all endpoints (`/api/explain` and `/api/quiz`), allowing you to develop the frontend, write unit tests, or test deployments locally at zero cost.

---

## 🛠️ Local Development Setup

### 1. Clone the Repository
```bash
git clone https://github.com/Kaushik-1609/dtu-hackathon-project.git
cd dtu-hackathon-project
```

### 2. Create and Activate a Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy the template configuration:
```bash
cp .env.example .env
```

Edit `.env`:
```ini
# Required for live AI calls (leave blank if running with MOCK=1)
GEMINI_API_KEY=your_gemini_api_key_here

# Default model
GEMMA_MODEL=gemma-4-31b-it

# Server port
PORT=5000

# Set MOCK=1 for offline/local testing without API keys
MOCK=1
```

### 5. Run the Application
```bash
python app.py
```
Open your browser to [http://localhost:5000](http://localhost:5000).

---

## 🧪 Running Tests

Before submitting a Pull Request, verify your changes against the frozen API contract:

### Run Bash API Tests
```bash
./samples/test_api.sh
```

### Run Python Schema Validator
```bash
python3 samples/test_runner.py
```

All 5 tests must pass before submitting your PR.

---

## 🌿 Git Branch & PR Workflow

1. **Fork & Branch**: Create a branch with a descriptive name:
   ```bash
   git checkout -b feature/your-feature-name
   # Team members use assigned branches: hkg-<name>
   ```
2. **Adhere to Code Ownership**:
   - `app.py`, `gemma_client.py` $\rightarrow$ Backend & Gemma logic
   - `templates/index.html`, `static/*` $\rightarrow$ Frontend UI & Vanilla JS
   - `requirements.txt`, `Dockerfile`, `Procfile`, `README.md` $\rightarrow$ Packaging & Config
   - `samples/*`, `docs/*` $\rightarrow$ Documentation & Datasets
3. **Keep Commits Clean & Descriptive**:
   ```bash
   git commit -m "feat(docs): add testing instructions and quiz contract specs"
   ```
4. **Push & Open a Pull Request**:
   - Provide a clear summary of changes in the PR description.
   - Link the relevant issue number.
   - Confirm that `test_runner.py` passed locally.

---

## 💡 Future Roadmap & Good First Issues

Interested in contributing? Here are features on our roadmap:

- [ ] **Indic Language Expansion**: Add support for Tamil (`ta`), Telugu (`te`), and Bengali (`bn`).
- [ ] **Voice Input / TTS**: Allow students to speak their doubts and listen to the explanation.
- [ ] **LaTeX Math Rendering**: Render mathematical formulas with client-side MathJax or KaTeX.
- [ ] **PDF Support**: Allow uploading multi-page PDF homework sheets.
- [ ] **Dark Mode Toggle**: Add a high-contrast dark theme in `static/style.css`.

---

## 📜 Code of Conduct

DoubtLens adheres to the [Contributor Covenant](https://www.contributor-covenant.org/). We are dedicated to providing a welcoming, harassment-free environment for everyone. Please be respectful, constructive, and kind.
