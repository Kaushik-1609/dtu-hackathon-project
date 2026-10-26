/**
 * DOUBTLENS — Multimodal STEM AI Problem Solver
 * Vanilla JS Application Controller
 * No external libraries | 100% Frozen API Contract Compliant
 * Hacktoberfest Hack Day Delhi x SKILLOP DTU (MLH)
 */

'use strict';

(function () {
  // ---------------------------------------------------------------------------
  // Application State
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
    quizAnswers: {},
    quizScore: 0,
    isSpeaking: false,
    loadingInterval: null
  };

  // Sample doubts for quick 1-click testing
  const SAMPLE_DOUBTS = {
    newton: "A 5 kg wooden block is pulled horizontally across a rough surface with a force of 25 N. The coefficient of kinetic friction is 0.2. Calculate the frictional force and the resulting acceleration of the block using Newton's Second Law (F = ma).",
    quadratic: "Find the roots of the quadratic equation 3x² - 5x + 2 = 0 using the quadratic formula. State the value of the discriminant (b² - 4ac) and describe the nature of the roots.",
    photosynthesis: "Explain the light-dependent reactions of photosynthesis in the chloroplast thylakoid membrane. Describe the roles of Photosystem II, photolysis of water, electron transport, and ATP synthase.",
    chemistry: "According to Le Chatelier's Principle, explain how increasing total pressure and decreasing temperature affects the equilibrium yield of ammonia in the Haber-Bosch reaction: N₂(g) + 3H₂(g) ⇌ 2NH₃(g) + 92 kJ."
  };

  // Loading state cycling messages
  const LOADING_MESSAGES = [
    { title: "Gemma 4 is reading your doubt...", sub: "Extracting visual diagrams, math symbols, and core questions" },
    { title: "Analyzing STEM concepts...", sub: "Mapping problem parameters to physical principles and formulas" },
    { title: "Synthesizing step-by-step walkthrough...", sub: "Structuring intuitive explanation and exam takeaways via Gemini API" }
  ];

  // ---------------------------------------------------------------------------
  // DOM Elements Cache
  // ---------------------------------------------------------------------------
  const DOM = {
    // Health Pill
    healthPill: document.getElementById('health-pill'),
    healthText: document.getElementById('health-text'),
    themeToggleBtn: document.getElementById('theme-toggle-btn'),

    // Toast
    toast: document.getElementById('toast'),
    toastIcon: document.getElementById('toast-icon'),
    toastMessage: document.getElementById('toast-message'),
    toastClose: document.getElementById('toast-close'),

    // Form & Inputs
    form: document.getElementById('doubt-form'),
    dropzone: document.getElementById('dropzone'),
    imageInput: document.getElementById('image-input'),
    dropzoneEmpty: document.getElementById('dropzone-empty'),
    dropzonePreview: document.getElementById('dropzone-preview'),
    previewImage: document.getElementById('preview-image'),
    previewFilename: document.getElementById('preview-filename'),
    previewFilesize: document.getElementById('preview-filesize'),
    removeImageBtn: document.getElementById('remove-image-btn'),
    questionInput: document.getElementById('question-input'),
    sampleChips: document.querySelectorAll('.sample-chip'),
    submitBtn: document.getElementById('submit-btn'),

    // Loading Section
    loadingSection: document.getElementById('loading-section'),
    loadingStageText: document.getElementById('loading-stage-text'),
    loadingSubText: document.getElementById('loading-sub-text'),

    // Explanation Section
    explanationSection: document.getElementById('explanation-section'),
    explanationTopic: document.getElementById('explanation-topic'),
    topicLangPill: document.getElementById('topic-lang-pill'),
    topicLevelPill: document.getElementById('topic-level-pill'),
    explanationText: document.getElementById('explanation-text'),
    stepsList: document.getElementById('steps-list'),
    stepsCountBadge: document.getElementById('steps-count-badge'),
    keyPointsList: document.getElementById('key-points-list'),
    keypointsCountBadge: document.getElementById('keypoints-count-badge'),
    speakBtn: document.getElementById('speak-btn'),
    speakBtnText: document.getElementById('speak-btn-text'),
    copyBtn: document.getElementById('copy-btn'),
    copyBtnText: document.getElementById('copy-btn-text'),
    ctaTopicName: document.getElementById('cta-topic-name'),
    startQuizBtn: document.getElementById('start-quiz-btn'),

    // Quiz Section
    quizSection: document.getElementById('quiz-section'),
    quizLoading: document.getElementById('quiz-loading'),
    quizLoadingTopic: document.getElementById('quiz-loading-topic'),
    quizBoard: document.getElementById('quiz-board'),
    quizTopicHeader: document.getElementById('quiz-topic-header'),
    quizAnsweredCount: document.getElementById('quiz-answered-count'),
    quizScoreCurrent: document.getElementById('quiz-score-current'),
    quizProgressFill: document.getElementById('quiz-progress-fill'),
    quizQuestionsContainer: document.getElementById('quiz-questions-container'),
    quizResultCard: document.getElementById('quiz-result-card'),
    resultEmoji: document.getElementById('result-emoji'),
    resultTitle: document.getElementById('result-title'),
    resultFinalScore: document.getElementById('result-final-score'),
    resultFeedbackMessage: document.getElementById('result-feedback-message'),
    retakeQuizBtn: document.getElementById('retake-quiz-btn'),
    newDoubtBtn: document.getElementById('new-doubt-btn'),
    confettiCanvas: document.getElementById('confetti-canvas')
  };

  // ---------------------------------------------------------------------------
  // Utility Functions
  // ---------------------------------------------------------------------------
  function escapeHTML(str) {
    if (!str) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }

  function formatBytes(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  }

  let toastTimer = null;
  function showToast(message, type = 'info', duration = 4000) {
    if (toastTimer) clearTimeout(toastTimer);

    DOM.toastMessage.textContent = message;
    DOM.toast.className = 'toast show';

    if (type === 'error') {
      DOM.toast.classList.add('toast-error');
      DOM.toastIcon.textContent = '❌';
    } else if (type === 'success') {
      DOM.toast.classList.add('toast-success');
      DOM.toastIcon.textContent = '✅';
    } else {
      DOM.toast.classList.add('toast-info');
      DOM.toastIcon.textContent = '💡';
    }

    toastTimer = setTimeout(() => {
      DOM.toast.classList.remove('show');
    }, duration);
  }

  if (DOM.toastClose) {
    DOM.toastClose.addEventListener('click', () => {
      DOM.toast.classList.remove('show');
      if (toastTimer) clearTimeout(toastTimer);
    });
  }

  // ---------------------------------------------------------------------------
  // Theme Toggle Management
  // ---------------------------------------------------------------------------
  function initTheme() {
    const savedTheme = localStorage.getItem('doubtlens-theme') || 'theme-dark';
    document.body.className = savedTheme;

    if (DOM.themeToggleBtn) {
      DOM.themeToggleBtn.addEventListener('click', () => {
        const isDark = document.body.classList.contains('theme-dark');
        const newTheme = isDark ? 'theme-light' : 'theme-dark';
        document.body.className = newTheme;
        localStorage.setItem('doubtlens-theme', newTheme);
      });
    }
  }

  // ---------------------------------------------------------------------------
  // Backend API Health Check
  // ---------------------------------------------------------------------------
  async function checkBackendHealth() {
    try {
      const response = await fetch('/api/health');
      if (response.ok) {
        const data = await response.json();
        if (data && data.status === 'ok') {
          DOM.healthPill.className = 'status-pill status-ok';
          DOM.healthText.textContent = 'Backend Live';
          return;
        }
      }
      throw new Error('Non-ok response');
    } catch (err) {
      DOM.healthPill.className = 'status-pill status-down';
      DOM.healthText.textContent = 'Offline / Standby';
    }
  }

  // ---------------------------------------------------------------------------
  // Image Upload, Drag-and-Drop, and Clipboard Handling
  // ---------------------------------------------------------------------------
  const MAX_FILE_SIZE = 5 * 1024 * 1024; // 5 MB contract limit
  const ALLOWED_MIME_TYPES = ['image/png', 'image/jpeg', 'image/webp'];

  function handleFileSelection(file) {
    if (!file) return;

    if (!ALLOWED_MIME_TYPES.includes(file.type)) {
      showToast('Please upload a valid image file (PNG, JPG, or WEBP).', 'error');
      return;
    }

    if (file.size > MAX_FILE_SIZE) {
      showToast('Image file exceeds 5 MB limit. Please select a smaller image.', 'error');
      return;
    }

    state.selectedFile = file;

    // Generate preview
    const reader = new FileReader();
    reader.onload = (e) => {
      DOM.previewImage.src = e.target.result;
      DOM.previewFilename.textContent = file.name;
      DOM.previewFilesize.textContent = formatBytes(file.size);
      DOM.dropzoneEmpty.style.display = 'none';
      DOM.dropzonePreview.style.display = 'flex';
      showToast('Problem image attached successfully!', 'success');
    };
    reader.readAsDataURL(file);
  }

  function clearSelectedImage() {
    state.selectedFile = null;
    DOM.imageInput.value = '';
    DOM.previewImage.src = '';
    DOM.previewFilename.textContent = '';
    DOM.previewFilesize.textContent = '';
    DOM.dropzonePreview.style.display = 'none';
    DOM.dropzoneEmpty.style.display = 'flex';
  }

  function initDropzone() {
    // Open file picker on click (unless clicking remove button)
    DOM.dropzone.addEventListener('click', (e) => {
      if (e.target.closest('#remove-image-btn')) return;
      DOM.imageInput.click();
    });

    // Keyboard navigation
    DOM.dropzone.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        DOM.imageInput.click();
      }
    });

    DOM.imageInput.addEventListener('change', (e) => {
      if (e.target.files && e.target.files[0]) {
        handleFileSelection(e.target.files[0]);
      }
    });

    DOM.removeImageBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      clearSelectedImage();
    });

    // Drag and Drop
    ['dragenter', 'dragover'].forEach(eventType => {
      DOM.dropzone.addEventListener(eventType, (e) => {
        e.preventDefault();
        e.stopPropagation();
        DOM.dropzone.classList.add('drag-active');
      });
    });

    ['dragleave', 'drop'].forEach(eventType => {
      DOM.dropzone.addEventListener(eventType, (e) => {
        e.preventDefault();
        e.stopPropagation();
        DOM.dropzone.classList.remove('drag-active');
      });
    });

    DOM.dropzone.addEventListener('drop', (e) => {
      const files = e.dataTransfer.files;
      if (files && files.length > 0) {
        handleFileSelection(files[0]);
      }
    });

    // Clipboard Paste Listener (Ctrl+V / Cmd+V)
    window.addEventListener('paste', (e) => {
      const items = (e.clipboardData || e.originalEvent.clipboardData).items;
      for (const item of items) {
        if (item.type.indexOf('image') === 0) {
          const file = item.getAsFile();
          if (file) {
            handleFileSelection(file);
            showToast('Image pasted from clipboard!', 'success');
            break;
          }
        }
      }
    });
  }

  // ---------------------------------------------------------------------------
  // Sample Doubts Chips
  // ---------------------------------------------------------------------------
  function initSampleDoubts() {
    DOM.sampleChips.forEach(chip => {
      chip.addEventListener('click', () => {
        const sampleKey = chip.getAttribute('data-sample');
        if (SAMPLE_DOUBTS[sampleKey]) {
          DOM.questionInput.value = SAMPLE_DOUBTS[sampleKey];
          DOM.questionInput.focus();
          DOM.questionInput.scrollIntoView({ behavior: 'smooth', block: 'center' });
          showToast('Sample doubt loaded into question field!', 'info');
        }
      });
    });
  }

  // ---------------------------------------------------------------------------
  // Form Submission (/api/explain)
  // ---------------------------------------------------------------------------
  function startLoadingAnimation() {
    DOM.loadingSection.style.display = 'block';
    DOM.submitBtn.disabled = true;

    let stepIndex = 0;
    DOM.loadingStageText.textContent = LOADING_MESSAGES[0].title;
    DOM.loadingSubText.textContent = LOADING_MESSAGES[0].sub;

    state.loadingInterval = setInterval(() => {
      stepIndex = (stepIndex + 1) % LOADING_MESSAGES.length;
      DOM.loadingStageText.textContent = LOADING_MESSAGES[stepIndex].title;
      DOM.loadingSubText.textContent = LOADING_MESSAGES[stepIndex].sub;
    }, 2400);

    DOM.loadingSection.scrollIntoView({ behavior: 'smooth', block: 'center' });
  }

  function stopLoadingAnimation() {
    if (state.loadingInterval) {
      clearInterval(state.loadingInterval);
      state.loadingInterval = null;
    }
    DOM.loadingSection.style.display = 'none';
    DOM.submitBtn.disabled = false;
  }

  async function handleExplainSubmit(e) {
    e.preventDefault();

    const questionText = DOM.questionInput.value.trim();
    const hasImage = Boolean(state.selectedFile);

    // Contract validation: At least one of image / question is required
    if (!hasImage && !questionText) {
      showToast('Please upload a problem photo or type a question to get started.', 'error');
      DOM.questionInput.focus();
      return;
    }

    const languageInput = DOM.form.querySelector('input[name="language"]:checked');
    const levelInput = DOM.form.querySelector('input[name="level"]:checked');

    const language = languageInput ? languageInput.value : 'en';
    const level = levelInput ? levelInput.value : 'simple';

    // Build Multipart Form Data
    const formData = new FormData();
    formData.append('language', language);
    formData.append('level', level);

    if (hasImage) {
      formData.append('image', state.selectedFile);
    }
    if (questionText) {
      formData.append('question', questionText);
    }

    // Hide prior results
    DOM.explanationSection.style.display = 'none';
    DOM.quizSection.style.display = 'none';
    stopSpeaking();

    startLoadingAnimation();

    try {
      const response = await fetch('/api/explain', {
        method: 'POST',
        body: formData
      });

      const data = await response.json().catch(() => null);

      if (!response.ok) {
        const errorMsg = (data && data.error) ? data.error : `Request failed with status ${response.status}`;
        throw new Error(errorMsg);
      }

      if (!data || !data.topic || !data.explanation) {
        throw new Error('Received incomplete response structure from server.');
      }

      // Update State
      state.topic = data.topic;
      state.explanation = data.explanation;
      state.steps = Array.isArray(data.steps) ? data.steps : [];
      state.keyPoints = Array.isArray(data.key_points) ? data.key_points : [];
      state.language = language;
      state.level = level;

      renderExplanation();
      showToast('Doubt solved successfully!', 'success');

    } catch (err) {
      console.error('Explain Error:', err);
      showToast(err.message || 'Failed to explain problem. Please try again.', 'error');
    } finally {
      stopLoadingAnimation();
    }
  }

  function renderExplanation() {
    DOM.explanationTopic.textContent = state.topic;
    DOM.ctaTopicName.textContent = state.topic;
    DOM.topicLangPill.textContent = state.language === 'hi' ? '🇮🇳 हिन्दी' : '🇬🇧 English';
    DOM.topicLevelPill.textContent = state.level === 'detailed' ? '🔬 Detailed' : '⚡ Simple';

    DOM.explanationText.textContent = state.explanation;

    // Render Steps
    DOM.stepsList.innerHTML = '';
    if (state.steps.length > 0) {
      DOM.stepsCountBadge.textContent = `${state.steps.length} Steps`;
      state.steps.forEach((step, index) => {
        const stepCard = document.createElement('div');
        stepCard.className = 'step-card';
        stepCard.innerHTML = `
          <div class="step-number">${index + 1}</div>
          <div class="step-content">${escapeHTML(step)}</div>
        `;
        DOM.stepsList.appendChild(stepCard);
      });
    } else {
      DOM.stepsCountBadge.textContent = '0 Steps';
    }

    // Render Key Points
    DOM.keyPointsList.innerHTML = '';
    if (state.keyPoints.length > 0) {
      DOM.keypointsCountBadge.textContent = `${state.keyPoints.length} Points`;
      state.keyPoints.forEach((point) => {
        const pointCard = document.createElement('div');
        pointCard.className = 'key-point-card';
        pointCard.innerHTML = `
          <span class="key-point-bullet" aria-hidden="true">🔑</span>
          <span class="key-point-text">${escapeHTML(point)}</span>
        `;
        DOM.keyPointsList.appendChild(pointCard);
      });
    } else {
      DOM.keypointsCountBadge.textContent = '0 Points';
    }

    DOM.explanationSection.style.display = 'block';
    DOM.explanationSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  // ---------------------------------------------------------------------------
  // Speech Synthesis & Copy Features
  // ---------------------------------------------------------------------------
  function stopSpeaking() {
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
    }
    state.isSpeaking = false;
    DOM.speakBtn.classList.remove('speaking');
    DOM.speakBtnText.textContent = 'Read Aloud';
  }

  function initSpeechAndCopy() {
    // Read Aloud
    DOM.speakBtn.addEventListener('click', () => {
      if (!('speechSynthesis' in window)) {
        showToast('Speech synthesis is not supported in this browser.', 'info');
        return;
      }

      if (state.isSpeaking) {
        stopSpeaking();
        return;
      }

      const fullText = `${state.topic}. ${state.explanation}. ${state.steps.join('. ')}`;
      const utterance = new SpeechSynthesisUtterance(fullText);
      utterance.lang = state.language === 'hi' ? 'hi-IN' : 'en-US';
      utterance.rate = 0.95;

      utterance.onend = () => stopSpeaking();
      utterance.onerror = () => stopSpeaking();

      state.isSpeaking = true;
      DOM.speakBtn.classList.add('speaking');
      DOM.speakBtnText.textContent = 'Stop Listening';
      window.speechSynthesis.speak(utterance);
    });

    // Copy to Clipboard
    DOM.copyBtn.addEventListener('click', async () => {
      const markdown = [
        `# ${state.topic}`,
        '',
        `## Concept Explanation`,
        state.explanation,
        '',
        `## Step-by-Step Breakdown`,
        state.steps.map((s, i) => `${i + 1}. ${s}`).join('\n'),
        '',
        `## Key Exam Points`,
        state.keyPoints.map(k => `- ${k}`).join('\n')
      ].join('\n');

      try {
        await navigator.clipboard.writeText(markdown);
        DOM.copyBtnText.textContent = 'Copied! ✓';
        showToast('Full explanation copied to clipboard as Markdown!', 'success');
        setTimeout(() => {
          DOM.copyBtnText.textContent = 'Copy';
        }, 2200);
      } catch (err) {
        showToast('Could not copy to clipboard.', 'error');
      }
    });
  }

  // ---------------------------------------------------------------------------
  // Interactive Quiz Flow (/api/quiz)
  // ---------------------------------------------------------------------------
  async function handleStartQuiz() {
    if (!state.topic || !state.explanation) {
      showToast('Please solve a doubt first before testing yourself.', 'error');
      return;
    }

    DOM.quizSection.style.display = 'block';
    DOM.quizLoading.style.display = 'flex';
    DOM.quizBoard.style.display = 'none';
    DOM.quizResultCard.style.display = 'none';
    DOM.quizLoadingTopic.textContent = state.topic;

    DOM.quizSection.scrollIntoView({ behavior: 'smooth', block: 'start' });

    try {
      const payload = {
        topic: state.topic,
        explanation: state.explanation,
        language: state.language
      };

      const response = await fetch('/api/quiz', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      const data = await response.json().catch(() => null);

      if (!response.ok) {
        const errorMsg = (data && data.error) ? data.error : `Quiz request failed with status ${response.status}`;
        throw new Error(errorMsg);
      }

      if (!data || !Array.isArray(data.questions) || data.questions.length === 0) {
        throw new Error('Received invalid quiz questions from server.');
      }

      state.quizQuestions = data.questions;
      state.quizAnswers = {};
      state.quizScore = 0;

      renderQuizBoard();

    } catch (err) {
      console.error('Quiz Error:', err);
      showToast(err.message || 'Failed to generate quiz. Please try again.', 'error');
      DOM.quizSection.style.display = 'none';
    } finally {
      DOM.quizLoading.style.display = 'none';
    }
  }

  function renderQuizBoard() {
    DOM.quizTopicHeader.textContent = `Quiz: ${state.topic}`;
    DOM.quizAnsweredCount.textContent = '0';
    DOM.quizScoreCurrent.textContent = '0';
    DOM.quizProgressFill.style.width = '0%';
    DOM.quizQuestionsContainer.innerHTML = '';

    const optionLabels = ['A', 'B', 'C', 'D'];

    state.quizQuestions.forEach((qObj, qIdx) => {
      const qCard = document.createElement('div');
      qCard.className = 'card question-card';
      qCard.id = `quiz-card-${qIdx}`;

      const metaRow = document.createElement('div');
      metaRow.className = 'question-meta-row';
      metaRow.innerHTML = `
        <span class="q-badge">Question ${qIdx + 1} of 5</span>
        <span class="q-status-badge unanswered" id="q-status-${qIdx}">Unanswered</span>
      `;
      qCard.appendChild(metaRow);

      const qText = document.createElement('h4');
      qText.className = 'q-text';
      qText.textContent = qObj.q;
      qCard.appendChild(qText);

      const optionsGrid = document.createElement('div');
      optionsGrid.className = 'options-grid';

      qObj.options.forEach((optText, optIdx) => {
        const optBtn = document.createElement('button');
        optBtn.type = 'button';
        optBtn.className = 'option-btn';
        optBtn.setAttribute('data-qidx', qIdx);
        optBtn.setAttribute('data-optidx', optIdx);

        optBtn.innerHTML = `
          <span class="opt-prefix">${optionLabels[optIdx] || optIdx + 1}</span>
          <span class="opt-text">${escapeHTML(optText)}</span>
        `;

        optBtn.addEventListener('click', () => handleOptionSelect(qIdx, optIdx, qObj, qCard));
        optionsGrid.appendChild(optBtn);
      });

      qCard.appendChild(optionsGrid);

      // Feedback / Why container (hidden initially)
      const whyContainer = document.createElement('div');
      whyContainer.className = 'why-card';
      whyContainer.id = `q-why-${qIdx}`;
      whyContainer.style.display = 'none';
      whyContainer.innerHTML = `
        <div class="why-header">💡 Why this is correct</div>
        <div class="why-text">${escapeHTML(qObj.why)}</div>
      `;
      qCard.appendChild(whyContainer);

      DOM.quizQuestionsContainer.appendChild(qCard);
    });

    DOM.quizBoard.style.display = 'block';
  }

  function handleOptionSelect(qIdx, selectedOptIdx, qObj, qCard) {
    if (state.quizAnswers[qIdx] !== undefined) return; // Already answered

    state.quizAnswers[qIdx] = selectedOptIdx;

    const isCorrect = (selectedOptIdx === qObj.answer_index);
    if (isCorrect) {
      state.quizScore++;
    }

    // Update Question Card UI
    const statusBadge = qCard.querySelector(`#q-status-${qIdx}`);
    const optionButtons = qCard.querySelectorAll('.option-btn');

    optionButtons.forEach((btn, idx) => {
      btn.disabled = true;

      if (idx === qObj.answer_index) {
        btn.classList.add(isCorrect ? 'selected-correct' : 'revealed-correct');
      } else if (idx === selectedOptIdx && !isCorrect) {
        btn.classList.add('selected-wrong');
      }
    });

    if (statusBadge) {
      if (isCorrect) {
        statusBadge.className = 'q-status-badge correct';
        statusBadge.textContent = '✅ Correct';
      } else {
        statusBadge.className = 'q-status-badge incorrect';
        statusBadge.textContent = '❌ Incorrect';
      }
    }

    // Reveal Why
    const whyCard = qCard.querySelector(`#q-why-${qIdx}`);
    if (whyCard) {
      whyCard.style.display = 'block';
    }

    // Update Progress & Score
    const answeredTotal = Object.keys(state.quizAnswers).length;
    DOM.quizAnsweredCount.textContent = answeredTotal;
    DOM.quizScoreCurrent.textContent = state.quizScore;
    DOM.quizProgressFill.style.width = `${(answeredTotal / state.quizQuestions.length) * 100}%`;

    // If all questions are answered, show summary card
    if (answeredTotal === state.quizQuestions.length) {
      setTimeout(() => {
        showQuizResults();
      }, 500);
    }
  }

  function showQuizResults() {
    const score = state.quizScore;
    const total = state.quizQuestions.length;

    DOM.resultFinalScore.textContent = score;

    if (score === 5) {
      DOM.resultEmoji.textContent = '🏆';
      DOM.resultTitle.textContent = 'Perfect Score!';
      DOM.resultFeedbackMessage.textContent = 'Outstanding conceptual mastery! You solved every single question correctly with zero hesitation.';
      triggerConfetti();
    } else if (score >= 4) {
      DOM.resultEmoji.textContent = '🌟';
      DOM.resultTitle.textContent = 'Excellent Mastery!';
      DOM.resultFeedbackMessage.textContent = 'Great understanding! You have a solid grasp of the core STEM principles behind this doubt.';
      triggerConfetti();
    } else if (score >= 3) {
      DOM.resultEmoji.textContent = '👍';
      DOM.resultTitle.textContent = 'Good Effort!';
      DOM.resultFeedbackMessage.textContent = 'You grasped the main ideas, but review the step-by-step breakdown above to polish the finer details.';
    } else {
      DOM.resultEmoji.textContent = '📚';
      DOM.resultTitle.textContent = 'Needs Revision';
      DOM.resultFeedbackMessage.textContent = 'Take a moment to carefully re-read the steps and key takeaways above, then retake the quiz!';
    }

    DOM.quizResultCard.style.display = 'block';
    DOM.quizResultCard.scrollIntoView({ behavior: 'smooth', block: 'center' });
  }

  // ---------------------------------------------------------------------------
  // Pure JavaScript Confetti Engine (No external dependencies)
  // ---------------------------------------------------------------------------
  function triggerConfetti() {
    const canvas = DOM.confettiCanvas;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    canvas.width = canvas.offsetWidth;
    canvas.height = canvas.offsetHeight;

    const particles = [];
    const colors = ['#38bdf8', '#818cf8', '#c084fc', '#ec4899', '#10b981', '#f59e0b'];

    for (let i = 0; i < 70; i++) {
      particles.push({
        x: canvas.width / 2,
        y: canvas.height / 2,
        vx: (Math.random() - 0.5) * 14,
        vy: (Math.random() - 0.7) * 14,
        size: Math.random() * 8 + 4,
        color: colors[Math.floor(Math.random() * colors.length)],
        rotation: Math.random() * 360,
        vr: (Math.random() - 0.5) * 10,
        alpha: 1
      });
    }

    let animationFrame;
    function render() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      let aliveCount = 0;

      particles.forEach(p => {
        p.x += p.vx;
        p.y += p.vy;
        p.vy += 0.35; // Gravity
        p.vx *= 0.98; // Friction
        p.rotation += p.vr;
        p.alpha -= 0.012;

        if (p.alpha > 0) {
          aliveCount++;
          ctx.save();
          ctx.translate(p.x, p.y);
          ctx.rotate((p.rotation * Math.PI) / 180);
          ctx.globalAlpha = Math.max(0, p.alpha);
          ctx.fillStyle = p.color;
          ctx.fillRect(-p.size / 2, -p.size / 2, p.size, p.size * 0.7);
          ctx.restore();
        }
      });

      if (aliveCount > 0) {
        animationFrame = requestAnimationFrame(render);
      } else {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        cancelAnimationFrame(animationFrame);
      }
    }

    render();
  }

  // ---------------------------------------------------------------------------
  // Retake & New Doubt Handlers
  // ---------------------------------------------------------------------------
  function initQuizActions() {
    DOM.startQuizBtn.addEventListener('click', handleStartQuiz);

    DOM.retakeQuizBtn.addEventListener('click', () => {
      state.quizAnswers = {};
      state.quizScore = 0;
      DOM.quizResultCard.style.display = 'none';
      renderQuizBoard();
      DOM.quizBoard.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });

    DOM.newDoubtBtn.addEventListener('click', () => {
      clearSelectedImage();
      DOM.questionInput.value = '';
      DOM.explanationSection.style.display = 'none';
      DOM.quizSection.style.display = 'none';
      stopSpeaking();
      window.scrollTo({ top: 0, behavior: 'smooth' });
      DOM.questionInput.focus();
    });
  }

  // ---------------------------------------------------------------------------
  // Application Bootstrap
  // ---------------------------------------------------------------------------
  function init() {
    initTheme();
    checkBackendHealth();
    initDropzone();
    initSampleDoubts();
    initSpeechAndCopy();
    initQuizActions();

    DOM.form.addEventListener('submit', handleExplainSubmit);

    // Periodically re-verify health every 45s
    setInterval(checkBackendHealth, 45000);
  }

  // Run on DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();
