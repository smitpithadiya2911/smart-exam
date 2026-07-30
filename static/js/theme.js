// Dark / Light Theme Controller
document.addEventListener('DOMContentLoaded', () => {
  const themeToggleBtn = document.getElementById('dark-mode-toggle');
  const savedTheme = localStorage.getItem('theme');
  const initialTheme = savedTheme || document.documentElement.getAttribute('data-theme') || 'dark';
  
  document.documentElement.setAttribute('data-theme', initialTheme);
  updateToggleIcon(initialTheme === 'dark');

  if (themeToggleBtn) {
    themeToggleBtn.addEventListener('click', () => {
      const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
      const newTheme = isDark ? 'light' : 'dark';
      
      // Animate icon rotation
      const icon = document.getElementById('theme-icon');
      if (icon) {
        icon.style.transform = 'rotate(360deg) scale(1.2)';
        icon.style.transition = 'transform 0.4s cubic-bezier(0.68, -0.55, 0.27, 1.55)';
        setTimeout(() => {
          icon.style.transform = 'rotate(0deg) scale(1)';
        }, 400);
      }

      document.documentElement.setAttribute('data-theme', newTheme);
      localStorage.setItem('theme', newTheme);
      updateToggleIcon(newTheme === 'dark');

      // Sync to Django user preference endpoint if logged in
      fetch('/toggle-dark-mode/', {
        method: 'POST',
        headers: {
          'X-CSRFToken': getCsrfToken(),
          'Content-Type': 'application/json'
        }
      }).catch(err => console.log('Theme sync notice:', err));
    });
  }
});

function updateToggleIcon(isDark) {
  const icon = document.getElementById('theme-icon');
  const toggleBtn = document.getElementById('dark-mode-toggle');
  if (icon) {
    icon.className = isDark ? 'bi bi-sun-fill text-warning' : 'bi bi-moon-stars-fill text-info';
  }
  if (toggleBtn) {
    toggleBtn.setAttribute('title', isDark ? 'Switch to Light Theme' : 'Switch to Dark Cyber Theme');
  }
}


function getCsrfToken() {
  const name = 'csrftoken';
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// Global Show/Hide Password Eye Toggle Handler
function togglePassword(inputId, btnElement) {
  var input = inputId ? document.getElementById(inputId) : null;
  if (!input && btnElement) {
    var container = btnElement.closest('.input-group, .position-relative, .password-wrapper, div');
    if (container) {
      input = container.querySelector('input[name="password"], input[name="confirm_password"], input[name="new_password"], input[type="password"], input[type="text"]');
    }
  }
  
  if (input) {
    var isPassword = (input.type === 'password');
    input.type = isPassword ? 'text' : 'password';

    var icon = btnElement ? (btnElement.tagName === 'I' ? btnElement : btnElement.querySelector('i')) : null;
    if (icon) {
      if (isPassword) {
        icon.className = 'bi bi-eye-slash-fill';
      } else {
        icon.className = 'bi bi-eye-fill';
      }
    }
  }
}

document.addEventListener('click', (e) => {
  const toggleBtn = e.target.closest('.toggle-password-btn');
  if (toggleBtn) {
    e.preventDefault();
    const targetSelector = toggleBtn.getAttribute('data-target');
    togglePassword(targetSelector ? targetSelector.replace('#', '') : null, toggleBtn);
  }
});



