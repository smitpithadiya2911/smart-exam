/**
 * Cyberpunk 60FPS Dynamic Background Engine
 * Renders glowing floating particles, neural network web, digital grid,
 * ambient blue/purple fog waves, and cursor light aura.
 */
document.addEventListener('DOMContentLoaded', () => {
  const canvas = document.getElementById('cyber-particle-canvas');
  if (!canvas) return;

  const ctx = canvas.getContext('2d');
  let width = (canvas.width = window.innerWidth);
  let height = (canvas.height = window.innerHeight);

  let mouse = { x: width / 2, y: height / 2, targetX: width / 2, targetY: height / 2 };

  window.addEventListener('resize', () => {
    width = canvas.width = window.innerWidth;
    height = canvas.height = window.innerHeight;
  });

  window.addEventListener('mousemove', (e) => {
    mouse.targetX = e.clientX;
    mouse.targetY = e.clientY;
  });

  // Particle System Parameters
  const particleCount = Math.min(Math.floor(window.innerWidth / 16), 80);
  const particles = [];

  const colors = [
    { r: 0, g: 245, b: 255 },  // Glow Cyan
    { r: 0, g: 168, b: 255 },  // Primary Blue
    { r: 123, g: 63, b: 251 }, // Purple Glow
    { r: 62, g: 166, b: 255 }  // Electric Blue
  ];

  class Particle {
    constructor() {
      this.reset();
    }

    reset() {
      this.x = Math.random() * width;
      this.y = Math.random() * height;
      this.vx = (Math.random() - 0.5) * 0.8;
      this.vy = (Math.random() - 0.5) * 0.8;
      this.radius = Math.random() * 2.2 + 1;
      this.color = colors[Math.floor(Math.random() * colors.length)];
      this.alpha = Math.random() * 0.6 + 0.3;
      this.pulseSpeed = Math.random() * 0.02 + 0.005;
      this.maxAlpha = this.alpha;
    }

    update() {
      this.x += this.vx;
      this.y += this.vy;

      if (this.x < 0 || this.x > width) this.vx *= -1;
      if (this.y < 0 || this.y > height) this.vy *= -1;

      // Pulse opacity
      this.alpha = Math.sin(Date.now() * this.pulseSpeed) * 0.3 + (this.maxAlpha - 0.2);

      // Mouse attraction
      const dx = mouse.x - this.x;
      const dy = mouse.y - this.y;
      const dist = Math.sqrt(dx * dx + dy * dy);
      if (dist < 140) {
        this.x -= (dx / dist) * 0.6;
        this.y -= (dy / dist) * 0.6;
      }
    }

    draw() {
      ctx.beginPath();
      ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(${this.color.r}, ${this.color.g}, ${this.color.b}, ${Math.max(0.1, this.alpha)})`;
      ctx.shadowBlur = 12;
      ctx.shadowColor = `rgba(${this.color.r}, ${this.color.g}, ${this.color.b}, 0.8)`;
      ctx.fill();
      ctx.shadowBlur = 0;
    }
  }

  for (let i = 0; i < particleCount; i++) {
    particles.push(new Particle());
  }

  // Draw cyber digital grid line overlays
  function drawDigitalGrid() {
    ctx.strokeStyle = 'rgba(0, 245, 255, 0.025)';
    ctx.lineWidth = 1;
    const gridSize = 60;

    for (let x = 0; x < width; x += gridSize) {
      ctx.beginPath();
      ctx.moveTo(x, 0);
      ctx.lineTo(x, height);
      ctx.stroke();
    }

    for (let y = 0; y < height; y += gridSize) {
      ctx.beginPath();
      ctx.moveTo(0, y);
      ctx.lineTo(width, y);
      ctx.stroke();
    }
  }

  // Draw ambient floating glow fog spots
  function drawGlowOrbs() {
    const time = Date.now() * 0.0005;

    // Orb 1: Cyan Glow
    const x1 = width * 0.25 + Math.sin(time) * 120;
    const y1 = height * 0.3 + Math.cos(time * 0.8) * 80;
    const grad1 = ctx.createRadialGradient(x1, y1, 10, x1, y1, 350);
    grad1.addColorStop(0, 'rgba(0, 245, 255, 0.12)');
    grad1.addColorStop(0.5, 'rgba(0, 168, 255, 0.05)');
    grad1.addColorStop(1, 'rgba(4, 6, 15, 0)');
    ctx.fillStyle = grad1;
    ctx.fillRect(0, 0, width, height);

    // Orb 2: Purple Glow
    const x2 = width * 0.75 + Math.cos(time * 0.9) * 100;
    const y2 = height * 0.7 + Math.sin(time * 1.1) * 90;
    const grad2 = ctx.createRadialGradient(x2, y2, 10, x2, y2, 400);
    grad2.addColorStop(0, 'rgba(123, 63, 251, 0.14)');
    grad2.addColorStop(0.6, 'rgba(62, 166, 255, 0.04)');
    grad2.addColorStop(1, 'rgba(4, 6, 15, 0)');
    ctx.fillStyle = grad2;
    ctx.fillRect(0, 0, width, height);
  }

  // Draw neural connections between nearby particles
  function drawConnections() {
    for (let i = 0; i < particles.length; i++) {
      for (let j = i + 1; j < particles.length; j++) {
        const dx = particles[i].x - particles[j].x;
        const dy = particles[i].y - particles[j].y;
        const dist = Math.sqrt(dx * dx + dy * dy);

        if (dist < 130) {
          const alpha = (1 - dist / 130) * 0.25;
          ctx.beginPath();
          ctx.moveTo(particles[i].x, particles[i].y);
          ctx.lineTo(particles[j].x, particles[j].y);
          ctx.strokeStyle = `rgba(0, 245, 255, ${alpha})`;
          ctx.lineWidth = 0.8;
          ctx.stroke();
        }
      }
    }
  }

  // Cursor Light Aura Follower
  function drawCursorGlow() {
    mouse.x += (mouse.targetX - mouse.x) * 0.1;
    mouse.y += (mouse.targetY - mouse.y) * 0.1;

    const grad = ctx.createRadialGradient(mouse.x, mouse.y, 0, mouse.x, mouse.y, 220);
    grad.addColorStop(0, 'rgba(0, 245, 255, 0.10)');
    grad.addColorStop(0.5, 'rgba(123, 63, 251, 0.04)');
    grad.addColorStop(1, 'rgba(0, 0, 0, 0)');
    ctx.fillStyle = grad;
    ctx.beginPath();
    ctx.arc(mouse.x, mouse.y, 220, 0, Math.PI * 2);
    ctx.fill();
  }

  // Main 60FPS Render Loop
  function render() {
    ctx.clearRect(0, 0, width, height);

    drawGlowOrbs();
    drawDigitalGrid();
    drawCursorGlow();

    particles.forEach((p) => {
      p.update();
      p.draw();
    });

    drawConnections();

    requestAnimationFrame(render);
  }

  render();
});
