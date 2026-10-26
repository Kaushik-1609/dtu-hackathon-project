# DoubtLens — 2-Minute Live Demo Script & Contingency Protocol

**Hackathon:** Hacktoberfest Hack Day Delhi x SKILLOP DTU (MLH)  
**Total Target Duration:** 2 minutes (120 seconds)  
**Presenter Setup Checklist:**
- Open browser tab: `http://localhost:5000` (or deployed staging URL).
- Open Finder folder with sample test images: [`samples/physics_newton_law.jpg`](../samples/physics_newton_law.jpg).
- Have pre-recorded fallback video ready in another window minimized.

---

## ⏱️ Timeline & Stage Script

| Time | Phase | On-Screen Action | Spoken Words / Voiceover |
|---|---|---|---|
| **0:00 - 0:15** (15s) | **Hook** | Presenter stands confident, points to a textbook / slides with a tough problem. | *"Raise your hand if you’ve ever stared at a physics diagram or calculus equation at 1 AM, completely stuck, with no tutor around to help. General chatbots dump long text walls or jump straight to answers without explaining the core intuition. Meet **DoubtLens**."* |
| **0:15 - 0:30** (15s) | **The Problem & Setup** | Show DoubtLens clean landing interface. Zero clutter. | *"Students don't just type doubts — they read textbook pages, draw circuit diagrams, and scribble formulas in notebooks. And millions study in Hindi, where quality STEM help is nearly nonexistent. DoubtLens bridges this using Google's **Gemma 4** multimodal model."* |
| **0:30 - 0:50** (20s) | **Upload Photo & Instant Explanation** | Drag-and-drop `physics_newton_law.jpg` (Newton's 2nd Law block diagram with friction). Click **Explain**. | *"Watch this. I drag-and-drop a photo of this physics problem with force vectors. In seconds, Gemma 4 parses the image natively. Look at this structure: Topic identified, intuition explained, 4 clear pedagogical steps, and key pitfalls to avoid with SI units."* |
| **0:50 - 1:10** (20s) | **Bilingual Toggle (Hindi)** | Select language toggle to **Hindi (`hi`)**, click **Explain** (or show instantaneous Hindi breakdown). | *"Here’s the game-changer: millions of students in Delhi and across India study in Hindi medium. One click, and Gemma 4 outputs in natural Devanagari Hindi—not robotic translation, but real technical terminology like 'त्वरण' and 'परिणामी बल'. True educational equity."* |
| **1:10 - 1:35** (25s) | **"Test Me" Quiz & Active Recall** | Click **"Test me"** button. 5 multiple-choice questions load. Click answers (3 right, 2 wrong). | *"Reading isn't learning; testing is. I hit 'Test Me', and Gemma 4 synthesizes a customized 5-question diagnostic quiz directly on this topic. I answer question 1... correct! I pick a wrong option on question 2... instant feedback with a one-line explanation of why."* |
| **1:35 - 1:45** (10s) | **Final Score & Mastery** | Complete question 5. Score summary displays (e.g. `4/5 Mastered`). | *"Boom! 4 out of 5. The student gets instant reinforcement, identifying exact knowledge gaps in under two minutes."* |
| **1:45 - 2:00** (15s) | **Impact & Closing Line** | Show GitHub open-source badge / MIT License slide. | *"DoubtLens is 100% open-source, runs on open-weights Gemma 4, has zero frontend framework bloat, and can be self-hosted by schools. Stop doubting, start mastering. Thank you!"* |

---

## 🛡️ Emergency Contingency Plan (When Wi-Fi or API Fails)

Conference Wi-Fi and live LLM endpoints are notoriously unpredictable during hackathon judging. Follow this strict protocol if latency spikes or network drops:

### Level 1: Immediate Graceful Degrade (< 5 seconds)
1. **Enable Mock Engine**: If API keys or network fails, relaunch Flask with `MOCK=1`:
   ```bash
   MOCK=1 python app.py
   ```
2. The UI will instantly return the realistic Newton's Second Law explanation and 5-question quiz offline with zero lag.
3. *Presenter Transition Line:* *"We designed DoubtLens with an offline simulation engine for zero-cost testing and edge reliability — let me show you the offline response pipeline!"*

### Level 2: Complete Network Blackout (Local Video Fallback)
1. Keep `docs/demo_backup_recording.mp4` queued in QuickTime/VLC in full-screen on Space 2 of macOS.
2. If the browser freezes, smoothly switch desktops (`Ctrl + Right Arrow`) and voiceover the high-definition recording live.
3. Keep high-resolution static screenshots ready in `docs/screenshots/`:
   - `01_landing_page.png`
   - `02_multimodal_explanation_en.png`
   - `03_hindi_bilingual_explanation.png`
   - `04_interactive_quiz_flow.png`
   - `05_final_score_breakdown.png`
