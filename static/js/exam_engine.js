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
      Swal.fire({
        title: 'Time is up!',
        text: 'Submitting your exam automatically...',
        icon: 'warning',
        allowOutsideClick: false,
        showConfirmButton: false,
        timer: 3000,
        timerProgressBar: true
      }).then(() => {
        document.getElementById('exam-taking-form')?.submit();
      });
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

let isSubmitting = false;

function setupAntiCheat(attemptId, maxViolations) {
  // 1. Detect Tab Switch / Window Focus Lost
  document.addEventListener('visibilitychange', () => {
    if (document.hidden && !isSubmitting) {
      logViolationBeacon(attemptId, 'TAB_SWITCH', 'Switched browser tab or minimized window');
    }
  });

  window.addEventListener('blur', () => {
    if (!isSubmitting) logViolation(attemptId, 'WINDOW_BLUR', 'Lost window focus');
  });

  // Handle refresh or navigate away
  window.addEventListener('beforeunload', (e) => {
    if (!isSubmitting) {
      logViolationBeacon(attemptId, 'WINDOW_BLUR', 'Navigated away or refreshed page');
    }
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
    if (!document.fullscreenElement && !isSubmitting) {
      logViolation(attemptId, 'FULLSCREEN_EXIT', 'Exited full screen mode');
    }
  });
}

function logViolationBeacon(attemptId, type, details) {
  const formData = new FormData();
  formData.append('attempt_id', attemptId);
  formData.append('violation_type', type);
  formData.append('details', details);
  navigator.sendBeacon('/exams/log-violation/', formData);
  window.location.reload();
}

function logViolation(attemptId, type, details) {
  if (isSubmitting) return;
  isSubmitting = true;
  const formData = new FormData();
  formData.append('attempt_id', attemptId);
  formData.append('violation_type', type);
  formData.append('details', details);

  fetch('/exams/log-violation/', {
    method: 'POST',
    headers: { 'X-CSRFToken': getCsrfToken() },
    body: formData
  })
  .then(() => {
    window.location.reload();
  })
  .catch(err => {
    console.log('Violation logging error:', err);
    window.location.reload();
  });
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

function confirmSubmission() {
  if (typeof Swal !== 'undefined') {
    Swal.fire({
      title: 'Submit Exam?',
      text: "Are you sure you want to finish and submit your exam now?",
      icon: 'question',
      showCancelButton: true,
      confirmButtonColor: '#10b981',
      cancelButtonColor: '#6c757d',
      confirmButtonText: 'Yes, Submit',
      cancelButtonText: 'Review Answers',
      background: '#0f172a',
      color: '#f8fafc',
      customClass: {
        popup: 'border border-secondary border-opacity-25 rounded-4 shadow-lg'
      }
    }).then((result) => {
      if (result.isConfirmed) {
        isSubmitting = true;
        Swal.fire({
          title: 'Submitting...',
          text: 'Please wait while we process your exam.',
          allowOutsideClick: false,
          showConfirmButton: false,
          background: '#0f172a',
          color: '#f8fafc',
          didOpen: () => {
            Swal.showLoading();
          }
        });
        document.getElementById('exam-taking-form')?.submit();
      }
    });
  } else {
    // Fallback if CDN failed
    if (confirm("Are you sure you want to finish and submit your exam now?")) {
      isSubmitting = true;
      document.getElementById('exam-taking-form')?.submit();
    }
  }
}
