/**
 * DOUBTLENS — Minimalist Developer-Platform Frontend Controller
 * Strict Compliance with Frozen API Contract & Optimus Style
 * Plain Vanilla JS | Zero External Libraries | Strict textContent Usage
 */

'use strict';

(function () {
  // ---------------------------------------------------------------------------
  // 1. STATE MANAGEMENT
  // ---------------------------------------------------------------------------
  const state = {
    selectedFile: null,
    topic: '',
    explanation: '',
    steps: [],
    keyPoints: [],
    language: 'en',
    level: 'simple',
    quizQuestions: [],
    currentQuizIndex: 0,
    quizScore: 0,
    quizAnswers: {}
  };

  // Sample doubts for quick testing
  const SAMPLE_DOUBTS = {
    newton: "A 5 kg wooden block is pulled across a rough horizontal surface with a force of 25 N. The coefficient of friction is 0.2. Calculate the acceleration of the block and state Newton's Second Law.",
    quadratic: "Solve the quadratic equation 3x² - 5x + 2 = 0 using the quadratic formula. State the value of the discriminant (b² - 4ac) and describe the nature of the roots.",
    photosynthesis: "Explain the light-dependent reactions of photosynthesis in the chloroplast thylakoid membrane, including photolysis of water, electron transport chain, and ATP synthesis."
  };

  const MAX_FILE_SIZE = 5 * 1024 * 1024; // 5 MB
  const ALLOWED_MIME_TYPES = ['image/png', 'image/jpeg', 'image/webp'];

  // ---------------------------------------------------------------------------
  // 2. DOM CACHE
  // ---------------------------------------------------------------------------
  const DOM = {
    // Navigation
    navToggle: document.getElementById('nav-toggle'),
    mobileMenu: document.getElementById('mobile-menu'),
    mobileNavLinks: document.querySelectorAll('.mobile-nav-link'),

    // Error Box
    errorBox: document.getElementById('error-box'),
    errorMessage: document.getElementById('error-message'),

    // App Inputs
    form: document.getElementById('doubt-form'),
    dropzone: document.getElementById('dropzone'),
    imageInput: document.getElementById('image-input'),
    dropzoneEmpty: document.getElementById('dropzone-empty'),
    dropzonePreview: document.getElementById('dropzone-preview'),
    previewImg: document.getElementById('preview-img'),
    previewFilename: document.getElementById('preview-filename'),
    previewFilesize: document.getElementById('preview-filesize'),
    removeImageBtn: document.getElementById('remove-image-btn'),
    questionInput: document.getElementById('question-input'),
    sampleButtons: document.querySelectorAll('.sample-btn'),
    submitBtn: document.getElementById('submit-btn'),

    // Loading State
    loadingState: document.getElementById('loading-state'),

    // Explanation Section
    resultSection: document.getElementById('result-section'),
    resultTopic: document.getElementById('result-topic'),
    resultExplanation: document.getElementById('result-explanation'),
    stepsList: document.getElementById('steps-list'),
    keyPointsGrid: document.getElementById('key-points-grid'),
    copyBtn: document.getElementById('copy-btn'),
    copyBtnText: document.getElementById('copy-btn-text'),
    startQuizBtn: document.getElementById('start-quiz-btn'),

    // Quiz Section
    quizSection: document.getElementById('quiz-section'),
    quizLoading: document.getElementById('quiz-loading'),
    quizCard: document.getElementById('quiz-card'),
    quizCounter: document.getElementById('quiz-counter'),
    quizProgressFill: document.getElementById('quiz-progress-fill'),
    quizQuestionText: document.getElementById('quiz-question-text'),
    quizOptionsList: document.getElementById('quiz-options-list'),
    quizFeedbackBox: document.getElementById('quiz-feedback-box'),
    feedbackBadge: document.getElementById('feedback-badge'),
    feedbackWhyText: document.getElementById('feedback-why-text'),
    quizNextRow: document.getElementById('quiz-next-row'),
    quizNextBtn: document.getElementById('quiz-next-btn'),

    // Final Score Card
    quizScoreCard: document.getElementById('quiz-score-card'),
    quizScoreTitle: document.getElementById('quiz-score-title'),
    quizScoreMessage: document.getElementById('quiz-score-message'),
    quizRetryBtn: document.getElementById('quiz-retry-btn'),
    quizNewDoubtBtn: document.getElementById('quiz-new-doubt-btn'),

    // Terminal Copy
    copyTerminalBtn: document.getElementById('copy-terminal-btn'),
    terminalCode: document.getElementById('terminal-code')
  };

  // ---------------------------------------------------------------------------
  // 3. ERROR BOX UTILITIES
  // ---------------------------------------------------------------------------
  function showError(msg) {
    if (!DOM.errorBox || !DOM.errorMessage) return;
    DOM.errorMessage.textContent = msg; // Strict textContent
    DOM.errorBox.style.display = 'flex';
    DOM.errorBox.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }

  function hideError() {
    if (!DOM.errorBox) return;
    DOM.errorBox.style.display = 'none';
    if (DOM.errorMessage) {
      DOM.errorMessage.textContent = '';
    }
  }

  function formatBytes(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  }

  // ---------------------------------------------------------------------------
  // 4. MOBILE NAVIGATION DRAWER
  // ---------------------------------------------------------------------------
  function initMobileMenu() {
    if (!DOM.navToggle || !DOM.mobileMenu) return;

    function openMenu() {
      DOM.navToggle.setAttribute('aria-expanded', 'true');
      DOM.mobileMenu.classList.add('active');
      DOM.mobileMenu.setAttribute('aria-hidden', 'false');
    }

    function closeMenu() {
      DOM.navToggle.setAttribute('aria-expanded', 'false');
      DOM.mobileMenu.classList.remove('active');
      DOM.mobileMenu.setAttribute('aria-hidden', 'true');
    }

    DOM.navToggle.addEventListener('click', () => {
      const isExpanded = DOM.navToggle.getAttribute('aria-expanded') === 'true';
      if (isExpanded) {
        closeMenu();
      } else {
        openMenu();
      }
    });

    // Close on any mobile link click
    DOM.mobileNavLinks.forEach(link => {
      link.addEventListener('click', () => {
        closeMenu();
      });
    });

    // Close on Escape key
    window.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && DOM.mobileMenu.classList.contains('active')) {
        closeMenu();
      }
    });
  }

  // ---------------------------------------------------------------------------
  // 5. IMAGE UPLOAD & DROPZONE HANDLING
  // ---------------------------------------------------------------------------
  function setFile(file) {
    hideError();

    if (!file) return;

    if (!ALLOWED_MIME_TYPES.includes(file.type)) {
      showError('Please upload a PNG, JPG, or WEBP image file.');
      return;
    }

    if (file.size > MAX_FILE_SIZE) {
      showError('The image exceeds the 5 MB limit. Please choose a smaller image.');
      return;
    }

    state.selectedFile = file;

    const reader = new FileReader();
    reader.onload = (e) => {
      DOM.previewImg.src = e.target.result;
      DOM.previewFilename.textContent = file.name; // Strict textContent
      DOM.previewFilesize.textContent = formatBytes(file.size); // Strict textContent
      DOM.dropzoneEmpty.style.display = 'none';
      DOM.dropzonePreview.style.display = 'flex';
    };
    reader.readAsDataURL(file);
  }

  function clearFile() {
    state.selectedFile = null;
    DOM.imageInput.value = '';
    DOM.previewImg.src = '';
    DOM.previewFilename.textContent = '';
    DOM.previewFilesize.textContent = '';
    DOM.dropzonePreview.style.display = 'none';
    DOM.dropzoneEmpty.style.display = 'flex';
  }

  function initDropzone() {
    if (!DOM.dropzone || !DOM.imageInput) return;

    DOM.dropzone.addEventListener('click', (e) => {
      if (e.target.closest('#remove-image-btn')) return;
      DOM.imageInput.click();
    });

    DOM.dropzone.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        DOM.imageInput.click();
      }
    });

    DOM.imageInput.addEventListener('change', (e) => {
      if (e.target.files && e.target.files[0]) {
        setFile(e.target.files[0]);
      }
    });

    if (DOM.removeImageBtn) {
      DOM.removeImageBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        clearFile();
      });
    }

    ['dragenter', 'dragover'].forEach(name => {
      DOM.dropzone.addEventListener(name, (e) => {
        e.preventDefault();
        e.stopPropagation();
        DOM.dropzone.classList.add('drag-active');
      });
    });

    ['dragleave', 'drop'].forEach(name => {
      DOM.dropzone.addEventListener(name, (e) => {
        e.preventDefault();
        e.stopPropagation();
        DOM.dropzone.classList.remove('drag-active');
      });
    });

    DOM.dropzone.addEventListener('drop', (e) => {
      const files = e.dataTransfer.files;
      if (files && files.length > 0) {
        setFile(files[0]);
      }
    });

    // Clipboard Paste Support (Ctrl+V / Cmd+V)
    window.addEventListener('paste', (e) => {
      const items = (e.clipboardData || e.originalEvent.clipboardData).items;
      for (const item of items) {
        if (item.type.indexOf('image') === 0) {
          const file = item.getAsFile();
          if (file) {
            setFile(file);
            break;
          }
        }
      }
    });
  }

  // ---------------------------------------------------------------------------
  // 6. SAMPLE DOUBTS
  // ---------------------------------------------------------------------------
  function initSamples() {
    DOM.sampleButtons.forEach(btn => {
      btn.addEventListener('click', () => {
        const key = btn.getAttribute('data-sample');
        if (SAMPLE_DOUBTS[key]) {
          DOM.questionInput.value = SAMPLE_DOUBTS[key];
          hideError();
          DOM.questionInput.focus();
        }
      });
    });
  }

  // ---------------------------------------------------------------------------
  // 7. EXPLAIN DOUBT FLOW (/api/explain)
  // ---------------------------------------------------------------------------
  async function handleExplainSubmit(e) {
    e.preventDefault();
    hideError();

    const question = DOM.questionInput.value.trim();
    const hasImage = Boolean(state.selectedFile);

    // Client-side check: at least one of image or question is required
    if (!hasImage && !question) {
      showError('Please upload an image or type a question to get an explanation.');
      DOM.questionInput.focus();
      return;
    }

    const langRadio = DOM.form.querySelector('input[name="language"]:checked');
    const levelRadio = DOM.form.querySelector('input[name="level"]:checked');

    const language = langRadio ? langRadio.value : 'en';
    const level = levelRadio ? levelRadio.value : 'simple';

    // Prepare FormData
    const formData = new FormData();
    formData.append('language', language);
    formData.append('level', level);

    if (hasImage) {
      formData.append('image', state.selectedFile);
    }
    if (question) {
      formData.append('question', question);
    }

    // Set Loading State
    DOM.submitBtn.disabled = true;
    DOM.loadingState.style.display = 'block';
    DOM.resultSection.style.display = 'none';
    DOM.quizSection.style.display = 'none';

    try {
      // Frozen contract: POST /api/explain, do NOT set Content-Type manually
      const response = await fetch('/api/explain', {
        method: 'POST',
        body: formData
      });

      let data;
      try {
        data = await response.json();
      } catch (parseErr) {
        throw new Error('Received an invalid response format from the server.');
      }

      if (!response.ok || (data && data.error)) {
        const errorMsg = (data && data.error) ? data.error : `Server returned status ${response.status}.`;
        throw new Error(errorMsg);
      }

      // Success
      state.topic = data.topic || 'Doubt Explanation';
      state.explanation = data.explanation || '';
      state.steps = Array.isArray(data.steps) ? data.steps : [];
      state.keyPoints = Array.isArray(data.key_points) ? data.key_points : [];
      state.language = language;
      state.level = level;

      renderExplanation();

    } catch (err) {
      showError(err.message || 'Unable to connect to the DoubtLens service. Please check your network.');
    } finally {
      DOM.loadingState.style.display = 'none';
      DOM.submitBtn.disabled = false;
    }
  }

  function renderExplanation() {
    // Strict textContent rendering
    DOM.resultTopic.textContent = state.topic;
    DOM.resultExplanation.textContent = state.explanation;

    // Steps list rendering
    DOM.stepsList.replaceChildren();
    state.steps.forEach((step, index) => {
      const li = document.createElement('li');
      li.className = 'step-item';

      const counter = document.createElement('span');
      counter.className = 'step-counter';
      counter.textContent = String(index + 1).padStart(2, '0');

      const text = document.createElement('div');
      text.className = 'step-text';
      text.textContent = step; // Strict textContent

      li.appendChild(counter);
      li.appendChild(text);
      DOM.stepsList.appendChild(li);
    });

    // Key points rendering
    DOM.keyPointsGrid.replaceChildren();
    state.keyPoints.forEach(point => {
      const card = document.createElement('div');
      card.className = 'key-point-chip';
      card.textContent = point; // Strict textContent
      DOM.keyPointsGrid.appendChild(card);
    });

    DOM.resultSection.style.display = 'block';
    DOM.resultSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  // ---------------------------------------------------------------------------
  // 8. COPY EXPLANATION
  // ---------------------------------------------------------------------------
  function initCopy() {
    if (!DOM.copyBtn) return;

    DOM.copyBtn.addEventListener('click', async () => {
      const markdown = [
        `# ${state.topic}`,
        '',
        state.explanation,
        '',
        '## Steps',
        state.steps.map((s, i) => `${i + 1}. ${s}`).join('\n'),
        '',
        '## Key Points',
        state.keyPoints.map(k => `- ${k}`).join('\n')
      ].join('\n');

      try {
        await navigator.clipboard.writeText(markdown);
        DOM.copyBtnText.textContent = 'Copied!';
        setTimeout(() => {
          DOM.copyBtnText.textContent = 'Copy explanation';
        }, 2000);
      } catch (err) {
        showError('Could not access clipboard.');
      }
    });

    // Quickstart terminal copy
    if (DOM.copyTerminalBtn && DOM.terminalCode) {
      DOM.copyTerminalBtn.addEventListener('click', async () => {
        try {
          await navigator.clipboard.writeText(DOM.terminalCode.textContent);
          DOM.copyTerminalBtn.textContent = 'Copied!';
          setTimeout(() => {
            DOM.copyTerminalBtn.textContent = 'Copy';
          }, 2000);
        } catch (err) {
          // ignore
        }
      });
    }
  }

  // ---------------------------------------------------------------------------
  // 9. INTERACTIVE QUIZ FLOW (/api/quiz) — ONE QUESTION AT A TIME
  // ---------------------------------------------------------------------------
  async function handleStartQuiz() {
    hideError();

    if (!state.topic || !state.explanation) {
      showError('Please solve a doubt first before testing yourself.');
      return;
    }

    DOM.quizSection.style.display = 'block';
    DOM.quizLoading.style.display = 'block';
    DOM.quizCard.style.display = 'none';
    DOM.quizScoreCard.style.display = 'none';

    DOM.quizSection.scrollIntoView({ behavior: 'smooth', block: 'start' });

    try {
      // Contract: POST /api/quiz with JSON body
      const response = await fetch('/api/quiz', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          topic: state.topic,
          explanation: state.explanation,
          language: state.language
        })
      });

      let data;
      try {
        data = await response.json();
      } catch (parseErr) {
        throw new Error('Received an invalid quiz format from the server.');
      }

      if (!response.ok || (data && data.error)) {
        const errorMsg = (data && data.error) ? data.error : `Quiz request failed with status ${response.status}.`;
        throw new Error(errorMsg);
      }

      if (!data || !Array.isArray(data.questions) || data.questions.length === 0) {
        throw new Error('Quiz data returned empty questions list.');
      }

      state.quizQuestions = data.questions;
      state.currentQuizIndex = 0;
      state.quizScore = 0;
      state.quizAnswers = {};

      DOM.quizLoading.style.display = 'none';
      renderCurrentQuestion();

    } catch (err) {
      DOM.quizLoading.style.display = 'none';
      DOM.quizSection.style.display = 'none';
      showError(err.message || 'Unable to load practice quiz. Please try again.');
    }
  }

  function renderCurrentQuestion() {
    const qIndex = state.currentQuizIndex;
    const total = state.quizQuestions.length;
    const question = state.quizQuestions[qIndex];

    if (!question) return;

    // Update Counter & Progress
    DOM.quizCounter.textContent = `Question ${qIndex + 1} of ${total}`;
    const percent = Math.round(((qIndex + 1) / total) * 100);
    DOM.quizProgressFill.style.width = `${percent}%`;

    // Strict textContent for question
    DOM.quizQuestionText.textContent = question.q;

    // Reset feedback and next button
    DOM.quizFeedbackBox.style.display = 'none';
    DOM.quizNextRow.style.display = 'none';

    // Update next button label
    if (qIndex === total - 1) {
      DOM.quizNextBtn.textContent = 'View final score \u2192';
    } else {
      DOM.quizNextBtn.textContent = 'Next question \u2192';
    }

    // Render Options
    DOM.quizOptionsList.replaceChildren();
    const letters = ['A', 'B', 'C', 'D'];

    question.options.forEach((optText, optIdx) => {
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'quiz-option-btn';

      const letterSpan = document.createElement('span');
      letterSpan.className = 'opt-letter';
      letterSpan.textContent = letters[optIdx] || String(optIdx + 1);

      const textSpan = document.createElement('span');
      textSpan.className = 'opt-text';
      textSpan.textContent = optText; // Strict textContent

      btn.appendChild(letterSpan);
      btn.appendChild(textSpan);

      btn.addEventListener('click', () => handleOptionClick(optIdx));
      DOM.quizOptionsList.appendChild(btn);
    });

    DOM.quizCard.style.display = 'block';
  }

  function handleOptionClick(chosenIdx) {
    const qIndex = state.currentQuizIndex;
    if (state.quizAnswers[qIndex] !== undefined) return; // Locked

    const question = state.quizQuestions[qIndex];
    state.quizAnswers[qIndex] = chosenIdx;

    const isCorrect = (chosenIdx === question.answer_index);
    if (isCorrect) {
      state.quizScore++;
    }

    // Disable and colorize option buttons
    const buttons = DOM.quizOptionsList.querySelectorAll('.quiz-option-btn');
    buttons.forEach((btn, idx) => {
      btn.disabled = true;

      if (idx === question.answer_index) {
        btn.classList.add('opt-correct');
      } else if (idx === chosenIdx && !isCorrect) {
        btn.classList.add('opt-wrong');
      }
    });

    // Feedback badge & why text
    if (isCorrect) {
      DOM.feedbackBadge.className = 'feedback-badge badge-correct';
      DOM.feedbackBadge.textContent = 'Correct';
    } else {
      DOM.feedbackBadge.className = 'feedback-badge badge-wrong';
      DOM.feedbackBadge.textContent = 'Incorrect';
    }

    DOM.feedbackWhyText.textContent = question.why; // Strict textContent
    DOM.quizFeedbackBox.style.display = 'block';

    // Reveal Next Button
    DOM.quizNextRow.style.display = 'flex';
  }

  function handleNextQuestion() {
    const total = state.quizQuestions.length;
    if (state.currentQuizIndex < total - 1) {
      state.currentQuizIndex++;
      renderCurrentQuestion();
    } else {
      // Show Final Score Screen
      showFinalScore();
    }
  }

  function showFinalScore() {
    DOM.quizCard.style.display = 'none';

    const score = state.quizScore;
    const total = state.quizQuestions.length;

    DOM.quizScoreTitle.textContent = `You scored ${score}/${total}`;

    if (score === total) {
      DOM.quizScoreMessage.textContent = 'Outstanding! You answered every question correctly and demonstrated complete mastery.';
    } else if (score >= 3) {
      DOM.quizScoreMessage.textContent = 'Good effort! You understand the key concepts. Review the step breakdown above for any missed details.';
    } else {
      DOM.quizScoreMessage.textContent = 'Take a moment to re-read the steps and key takeaways above, then try the quiz again.';
    }

    DOM.quizScoreCard.style.display = 'block';
    DOM.quizScoreCard.scrollIntoView({ behavior: 'smooth', block: 'center' });
  }

  function initQuizActions() {
    if (DOM.startQuizBtn) {
      DOM.startQuizBtn.addEventListener('click', handleStartQuiz);
    }

    if (DOM.quizNextBtn) {
      DOM.quizNextBtn.addEventListener('click', handleNextQuestion);
    }

    if (DOM.quizRetryBtn) {
      DOM.quizRetryBtn.addEventListener('click', () => {
        state.currentQuizIndex = 0;
        state.quizScore = 0;
        state.quizAnswers = {};
        DOM.quizScoreCard.style.display = 'none';
        renderCurrentQuestion();
        DOM.quizCard.scrollIntoView({ behavior: 'smooth', block: 'start' });
      });
    }

    if (DOM.quizNewDoubtBtn) {
      DOM.quizNewDoubtBtn.addEventListener('click', () => {
        clearFile();
        DOM.questionInput.value = '';
        DOM.resultSection.style.display = 'none';
        DOM.quizSection.style.display = 'none';
        hideError();
        const trySection = document.getElementById('try');
        if (trySection) {
          trySection.scrollIntoView({ behavior: 'smooth' });
        }
        DOM.questionInput.focus();
      });
    }
  }

  // ---------------------------------------------------------------------------
  // 11. 3D ROTATING ASCII GLYPH SPHERE ANIMATION (Optimus Mathematical Engine)
  // ---------------------------------------------------------------------------
  function initHeroAsciiSphere() {
    const canvas = document.getElementById('hero-ascii-canvas');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const glyphs = '░▒▓█▀▄▌▐│─┤├┴┬╭╮╰╯';
    let angle = 0;
    let animId = null;

    function handleResize() {
      const dpr = window.devicePixelRatio || 1;
      const rect = canvas.getBoundingClientRect();
      if (rect.width === 0 || rect.height === 0) return;
      canvas.width = rect.width * dpr;
      canvas.height = rect.height * dpr;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    }

    handleResize();
    window.addEventListener('resize', handleResize);

    function draw() {
      const rect = canvas.getBoundingClientRect();
      if (rect.width === 0 || rect.height === 0) {
        animId = requestAnimationFrame(draw);
        return;
      }

      ctx.clearRect(0, 0, rect.width, rect.height);

      const centerX = rect.width / 2;
      const centerY = rect.height / 2;
      const radius = 0.525 * Math.min(rect.width, rect.height);

      ctx.font = '12px monospace';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';

      const points = [];

      for (let theta = 0; theta < 2 * Math.PI; theta += 0.15) {
        for (let phi = 0; phi < Math.PI; phi += 0.15) {
          const r = Math.sin(phi) * Math.cos(theta + 0.5 * angle);
          const s = Math.sin(phi) * Math.sin(theta + 0.5 * angle);
          const i = Math.cos(phi);

          const u = 0.3 * angle;
          const m = r * Math.cos(u) - i * Math.sin(u);
          const p = r * Math.sin(u) + i * Math.cos(u);

          const x = 0.2 * angle;
          const h = s * Math.cos(x) - p * Math.sin(x);
          const f = s * Math.sin(x) + p * Math.cos(x);

          const charIdx = Math.floor(((f + 1) / 2) * (glyphs.length - 1));

          points.push({
            x: centerX + m * radius,
            y: centerY + h * radius,
            z: f,
            char: glyphs[Math.max(0, Math.min(glyphs.length - 1, charIdx))]
          });
        }
      }

      // Back-to-front depth sorting
      points.sort((a, b) => a.z - b.z);

      // Render glyphs with depth opacity
      for (let k = 0; k < points.length; k++) {
        const pt = points[k];
        const alpha = 0.2 + (pt.z + 1) * 0.4;
        ctx.fillStyle = `rgba(10, 10, 10, ${alpha.toFixed(3)})`;
        ctx.fillText(pt.char, pt.x, pt.y);
      }

      angle += 0.02;
      animId = requestAnimationFrame(draw);
    }

    draw();
  }

  // ---------------------------------------------------------------------------
  // 10. BOOTSTRAP INITIALIZATION
  // ---------------------------------------------------------------------------
  function init() {
    initMobileMenu();
    initDropzone();
    initSamples();
    initCopy();
    initQuizActions();
    initHeroAsciiSphere();

    if (DOM.form) {
      DOM.form.addEventListener('submit', handleExplainSubmit);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();
