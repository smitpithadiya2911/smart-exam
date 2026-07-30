// Live Exam Taking Engine & Anti-Cheating Violation Monitor
let remainingSeconds = 0;
let timerInterval = null;
let currentQuestionIndex = 0;

function initExamEngine(initialSeconds, attemptId, maxViolations) {
  remainingSeconds = initialSeconds;
  startTimer();
  setupAntiCheat(attemptId, maxViolations);
  setupPaletteListeners(attemptId);
}

function startTimer() {
  const timerDisplay = document.getElementById('exam-countdown-timer');
  if (!timerDisplay) return;

  timerInterval = setInterval(() => {
    if (remainingSeconds <= 0) {
      clearInterval(timerInterval);
      alert("Time is up! Submitting your exam automatically...");
      document.getElementById('exam-taking-form')?.submit();
      return;
    }

    remainingSeconds--;
    const mins = Math.floor(remainingSeconds / 60);
    const secs = remainingSeconds % 60;
    timerDisplay.innerText = `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;

    if (remainingSeconds === 300) { // 5 min warning
      showToast("Warning: 5 minutes remaining!", "bg-warning");
    }
  }, 1000);
}

function setupAntiCheat(attemptId, maxViolations) {
  // 1. Detect Tab Switch / Window Focus Lost
  document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
      logViolation(attemptId, 'TAB_SWITCH', 'Switched browser tab or minimized window');
    }
  });

  window.addEventListener('blur', () => {
    logViolation(attemptId, 'WINDOW_BLUR', 'Lost window focus');
  });

  // 2. Disable Right Click, Copy, Cut, Paste, Text Selection
  document.addEventListener('contextmenu', (e) => {
    e.preventDefault();
    return false;
  });

  document.addEventListener('copy', (e) => {
    e.preventDefault();
    logViolation(attemptId, 'COPY_PASTE', 'Text copy attempt detected');
  });

  document.addEventListener('cut', (e) => {
    e.preventDefault();
    logViolation(attemptId, 'COPY_PASTE', 'Text cut attempt detected');
  });

  document.addEventListener('paste', (e) => {
    e.preventDefault();
    logViolation(attemptId, 'COPY_PASTE', 'Text paste attempt detected');
  });

  // 3. Block Anti-Cheating Keyboard Shortcuts (Ctrl+C, Ctrl+V, F12, Ctrl+U, Inspect)
  document.addEventListener('keydown', (e) => {
    const key = e.key.toLowerCase();
    // F12 or Ctrl+Shift+I/J/C
    if (e.keyCode === 123 || (e.ctrlKey && e.shiftKey && (key === 'i' || key === 'j' || key === 'c'))) {
      e.preventDefault();
      logViolation(attemptId, 'COPY_PASTE', 'Attempted developer inspect tools');
      return false;
    }
    // Ctrl+C, Ctrl+V, Ctrl+X, Ctrl+U, Ctrl+A
    if (e.ctrlKey && (key === 'c' || key === 'v' || key === 'x' || key === 'u' || key === 'a')) {
      e.preventDefault();
      logViolation(attemptId, 'COPY_PASTE', `Blocked keyboard shortcut: Ctrl+${key.toUpperCase()}`);
      return false;
    }
  });

  // 4. Detect Fullscreen Exit
  document.addEventListener('fullscreenchange', () => {
    if (!document.fullscreenElement) {
      logViolation(attemptId, 'FULLSCREEN_EXIT', 'Exited full screen mode');
      alert("WARNING: Full screen mode is required during the examination!");
    }
  });
}

function logViolation(attemptId, type, details) {
  const formData = new FormData();
  formData.append('attempt_id', attemptId);
  formData.append('violation_type', type);
  formData.append('details', details);

  fetch('/exams/log-violation/', {
    method: 'POST',
    headers: { 'X-CSRFToken': getCsrfToken() },
    body: formData
  })
  .then(res => res.json())
  .then(data => {
    if (data.disqualified) {
      alert("EXAM DISQUALIFIED: You have exceeded the maximum allowed cheating violations.");
      window.location.reload();
    } else {
      showToast(`Violation Warning (${data.violations_count}/${data.max_allowed}): ${type}`, 'bg-danger text-white');
    }
  })
  .catch(err => console.log('Violation logging error:', err));
}

function setupPaletteListeners(attemptId) {
  // Radio button / input change listener for AJAX autosave
  document.querySelectorAll('.q-option-input, .q-text-input').forEach(input => {
    input.addEventListener('change', (e) => {
      const questionId = e.target.getAttribute('data-question-id');
      const selectedOption = e.target.value;
      
      autosaveAnswer(attemptId, questionId, selectedOption, '');
      
      // Update Palette Badge to Green (Answered)
      const badge = document.getElementById(`palette-badge-${questionId}`);
      if (badge) {
        badge.className = 'q-badge q-answered';
      }
    });
  });
}

function autosaveAnswer(attemptId, questionId, selectedOption, textResponse) {
  const formData = new FormData();
  formData.append('attempt_id', attemptId);
  formData.append('question_id', questionId);
  formData.append('selected_option', selectedOption);
  formData.append('text_response', textResponse);

  fetch('/exams/autosave/', {
    method: 'POST',
    headers: { 'X-CSRFToken': getCsrfToken() },
    body: formData
  })
  .then(res => res.json())
  .then(data => console.log('Answer autosaved:', data))
  .catch(err => console.log('Autosave error:', err));
}

function showToast(message, bgClass = 'bg-primary text-white') {
  const container = document.getElementById('toast-container');
  if (!container) return;
  
  const toast = document.createElement('div');
  toast.className = `toast align-items-center ${bgClass} border-0 show animate__animated animate__fadeInUp`;
  toast.role = 'alert';
  toast.innerHTML = `
    <div class="d-flex">
      <div class="toast-body">${message}</div>
      <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
    </div>
  `;
  container.appendChild(toast);
  setTimeout(() => toast.remove(), 4000);
}
