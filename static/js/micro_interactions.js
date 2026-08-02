/**
 * Micro-Interactions & Luxury Animations Engine
 * Handles page loader, navbar click animations, Web Audio click feedback,
 * button click ripples, magnetic hover, and 3D card tilt.
 */

// Web Audio API Synthesizer Click Sound
let audioCtx = null;
function playCyberClickSound() {
  try {
    if (!audioCtx) {
      audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    }
    if (audioCtx.state === 'suspended') {
      audioCtx.resume();
    }
    const osc = audioCtx.createOscillator();
    const gain = audioCtx.createGain();
    
    osc.type = 'sine';
    osc.frequency.setValueAtTime(800, audioCtx.currentTime);
    osc.frequency.exponentialRampToValueAtTime(300, audioCtx.currentTime + 0.06);
    
    gain.gain.setValueAtTime(0.08, audioCtx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.06);
    
    osc.connect(gain);
    gain.connect(audioCtx.destination);
    
    osc.start();
    osc.stop(audioCtx.currentTime + 0.06);
  } catch (err) {
    // Audio context fallback if blocked by browser policy
  }
}

document.addEventListener('DOMContentLoaded', () => {
  // 1. Hide Loading Overlay Smoothly
  const loader = document.getElementById('cyber-page-loader');
  if (loader) {
    const hideLoader = () => {
      if (loader.style.display !== 'none') {
        loader.classList.add('fade-out');
        setTimeout(() => (loader.style.display = 'none'), 400);
      }
    };

    window.addEventListener('load', hideLoader);
    setTimeout(hideLoader, 1200);
  }

  // 2. Navbar & Button Click Animations with GSAP Spring & Audio Feedback
  document.addEventListener('click', (e) => {
    const targetNav = e.target.closest('.nav-link-glass, .dark-toggle-btn');
    const targetBtn = e.target.closest('.btn, .btn-glass-primary, .btn-cyber-neon, .btn-action-edit, .btn-action-delete, .btn-action-view');

    const activeElem = targetNav || targetBtn;
    if (!activeElem) return;

    // Play subtle high-tech click chime
    playCyberClickSound();

    // GSAP Press Spring Animation if available
    if (typeof gsap !== 'undefined') {
      gsap.to(activeElem, {
        scale: 0.94,
        duration: 0.1,
        ease: 'power2.in',
        onComplete: () => {
          gsap.to(activeElem, {
            scale: 1,
            duration: 0.25,
            ease: 'back.out(1.8)'
          });
        }
      });
    }

    // Ripple Pulse Ring Element
    const rect = activeElem.getBoundingClientRect();
    const ripple = document.createElement('span');
    ripple.className = 'cyber-nav-pulse';

    const size = Math.max(rect.width, rect.height) * 2;
    ripple.style.width = ripple.style.height = `${size}px`;
    ripple.style.left = `${e.clientX - rect.left - size / 2}px`;
    ripple.style.top = `${e.clientY - rect.top - size / 2}px`;

    activeElem.appendChild(ripple);

    setTimeout(() => {
      ripple.remove();
    }, 550);
  });

  // 3. Card Mouse Spotlight Glow & 3D Parallax Tilt
  const cards = document.querySelectorAll('.glass-card, .admin-kpi-card, .quick-hub-card');
  cards.forEach((card) => {
    card.addEventListener('mousemove', (e) => {
      const rect = card.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;

      // Update CSS variables for radial spotlight gradient background
      card.style.setProperty('--mouse-x', `${x}px`);
      card.style.setProperty('--mouse-y', `${y}px`);
    });

    card.addEventListener('mouseleave', () => {
      // Clean up if needed
      card.style.transform = '';
    });
  });

  // 4. Magnetic Hover Effect for CTA Cyber Buttons
  const magneticBtns = document.querySelectorAll('.btn-magnetic, .btn-glass-primary');
  magneticBtns.forEach((btn) => {
    btn.addEventListener('mousemove', (e) => {
      const rect = btn.getBoundingClientRect();
      const x = e.clientX - rect.left - rect.width / 2;
      const y = e.clientY - rect.top - rect.height / 2;

      btn.style.transform = `translate(${x * 0.2}px, ${y * 0.2}px) scale(1.02)`;
    });

    btn.addEventListener('mouseleave', () => {
      btn.style.transform = 'translate(0px, 0px) scale(1)';
    });
  });

  // 5. Side Toast Messages Auto-Dismiss after exactly 3 Seconds
  const toasts = document.querySelectorAll('#toast-container .toast');
  toasts.forEach((toastEl) => {
    setTimeout(() => {
      toastEl.classList.remove('animate__slideInRight');
      toastEl.classList.add('animate__fadeOutRight');
      setTimeout(() => {
        toastEl.remove();
      }, 400);
    }, 3000); // 3 seconds timeout
  });
});

// 6. Dynamic Live AJAX Search dropdown
document.addEventListener('DOMContentLoaded', () => {
  const searchInput = document.getElementById('global-search-input');
  const searchResults = document.getElementById('global-search-results');
  
  if (searchInput && searchResults) {
    let debounceTimer;
    searchInput.addEventListener('input', () => {
      clearTimeout(debounceTimer);
      const query = searchInput.value.trim();
      if (query.length < 2) {
        searchResults.classList.add('d-none');
        searchResults.innerHTML = '';
        return;
      }
      
      debounceTimer = setTimeout(() => {
        fetch(`/analytics/live-search/?q=${encodeURIComponent(query)}`)
          .then(res => res.json())
          .then(data => {
            searchResults.innerHTML = '';
            if (data.results && data.results.length > 0) {
              data.results.forEach(item => {
                const div = document.createElement('a');
                div.href = item.url;
                div.className = 'd-block p-3 text-decoration-none border-bottom border-secondary border-opacity-25 hover-search-item';
                div.innerHTML = `
                  <div class="d-flex justify-content-between align-items-center">
                    <span class="fw-bold text-white small">${item.title}</span>
                    <span class="badge bg-info-subtle text-primary font-monospace" style="font-size: 10px;">${item.category}</span>
                  </div>
                  <div class="text-muted small mt-1" style="font-size: 11px;">${item.info}</div>
                `;
                searchResults.appendChild(div);
              });
              searchResults.classList.remove('d-none');
            } else {
              searchResults.innerHTML = '<div class="p-3 text-muted text-center small">No matches found</div>';
              searchResults.classList.remove('d-none');
            }
          })
          .catch(err => console.error('Search error:', err));
      }, 250);
    });
    
    document.addEventListener('click', (e) => {
      if (!searchInput.contains(e.target) && !searchResults.contains(e.target)) {
        searchResults.classList.add('d-none');
      }
    });
  }
});



