# DoubtLens — Manual QA Test Matrix & Bug Filing Protocol

**Hackathon:** Hacktoberfest Hack Day Delhi x SKILLOP DTU (MLH)  
**Lead Tester:** Utkarsh  
**Component Owners for Triage:**
- **Mayank** (`AI / Backend`): `app.py`, `gemma_client.py`, `/api/*` endpoints, JSON parsing, prompt engineering, Gemma 4 errors.
- **Harsh** (`UI / Frontend`): `templates/index.html`, `static/style.css`, `static/app.js`, mobile responsiveness, form validation, animations.

---

## 🧪 Comprehensive Manual Test Matrix

| # | Test Scenario | Test Input / Action | Expected Result | Pass/Fail | Bug Owner if Failed |
|---|---|---|---|---|---|
| **1** | **Clear Textbook Photo** | Upload `samples/physics_newton_law.jpg`, click "Explain". | HTTP 200. Clear topic "Newton's Second Law", intuition paragraph, 4 steps, 3 key points. | [ ] | Mayank (AI/Backend) |
| **2** | **Blurry / Low-Light Photo** | Upload out-of-focus or dimly lit handwritten snippet. | Model handles gracefully, extracts whatever legible or returns polite message requesting clearer photo without crashing (no 500). | [ ] | Mayank (AI/Backend) |
| **3** | **Text-Only Question** | Clear file input; type: *"State Ohm's Law and explain its limitations"* with level=simple. | HTTP 200. Explains Ohm's law with resistance formula, steps, and temperature limitations. | [ ] | Mayank (AI/Backend) |
| **4** | **No Input (Empty Form)** | Clear both file upload and text query; click "Explain". | HTTP 400. Client shows clean toast/alert: *"Please provide an image or enter a question."* No crash or blank screen. | [ ] | Harsh (UI validation) / Mayank (API 400) |
| **5** | **10 MB Oversized Image** | Upload image file > 5 MB (e.g., 10 MB high-res uncompressed image). | HTTP 413 or instant frontend client-side warning: *"File size exceeds 5 MB limit"*. | [ ] | Harsh (UI check) / Mayank (Flask limit) |
| **6** | **Unsupported File Format (PDF)** | Try uploading `.pdf`, `.docx`, or `.zip` file. | File picker restricts to `image/*` or UI shows *"Only PNG, JPG, or WEBP allowed"*. | [ ] | Harsh (UI `accept` attribute & validation) |
| **7** | **Hindi Vernacular Mode** | Upload `samples/physics_newton_law.jpg`, select language `"hi"`, click "Explain". | HTTP 200. Output is rendered entirely in valid Devanagari script with scientific words (बल, त्वरण, द्रव्यमान). | [ ] | Mayank (Prompt/Backend) |
| **8** | **Detailed Pedagogical Level** | Select level `"detailed"` for a calculus integration problem. | Step-by-step mathematical rigor increases (shows intermediate limits, formal theorems). | [ ] | Mayank (AI/Backend) |
| **9** | **Quiz: Correct & Incorrect Answers** | Click "Test me". Click a known right option (turns green, counter increments), then a wrong option (turns red, reveals correct answer + explanation). | Quiz UI highlights state dynamically, displays one-line "why", and updates live tally. | [ ] | Harsh (UI/app.js) |
| **10** | **"Try Again" / Retake Quiz** | Finish quiz; click "Try again" or reset button. | Quiz resets smoothly to question 1 with clean score state without page reload. | [ ] | Harsh (UI/app.js) |
| **11** | **Mobile Viewport (375px & 414px)** | Open Chrome DevTools in iPhone SE / iPhone 14 Pro emulation mode. | Responsive layout: single column, camera button accessible, quiz buttons easily tappable, no horizontal overflow. | [ ] | Harsh (CSS/style.css) |
| **12** | **Slow Network / High Latency** | DevTools Network tab set to "Slow 3G". Click "Explain". | Loading spinner / pulsing skeleton appears immediately, submit button disabled to prevent double clicks. | [ ] | Harsh (UI loading state) |

---

## 🐞 Bug Report Template

When a test fails, copy-paste this template into your team Slack/WhatsApp/issue tracker:

```markdown
### 🐞 Bug Report

**Title**: [Brief description of the bug]
**Test Case #**: [e.g., Test 5 - Oversized Image]
**Severity**: [Blocker / High / Medium / Low]
**Assignee**: [Mayank (AI/Backend) OR Harsh (UI)]

#### Steps to Reproduce:
1. Navigate to DoubtLens UI.
2. [Input action taken, e.g., uploaded 10MB image]
3. Clicked "Explain".

#### Expected Result:
[What should happen according to the API contract / design]

#### Actual Result:
[What actually happened, e.g., UI hung indefinitely, HTTP 500 error in console]

#### Screenshots / Console Logs:
- Console error: `...`
- Network tab status: `...`
```
