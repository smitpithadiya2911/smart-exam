// 3D Visual Accents: Cyberpunk Admin 3D Bar Stat & Parallax Card Tilt
document.addEventListener('DOMContentLoaded', () => {
  // 1. Certificate & Card Parallax 3D Tilt
  const tiltCard = document.querySelector('.tilt-card');
  if (tiltCard) {
    tiltCard.addEventListener('mousemove', (e) => {
      const rect = tiltCard.getBoundingClientRect();
      const x = e.clientX - rect.left - rect.width / 2;
      const y = e.clientY - rect.top - rect.height / 2;
      
      const rotateX = (-y / rect.height) * 16;
      const rotateY = (x / rect.width) * 16;
      
      tiltCard.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale3d(1.02, 1.02, 1.02)`;
    });

    tiltCard.addEventListener('mouseleave', () => {
      tiltCard.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) scale3d(1, 1, 1)';
    });
  }

  // 2. Admin Cyber 3D Bar Accent Visualization
  const barCanvas = document.getElementById('admin-3d-stat-canvas');
  if (barCanvas && typeof THREE !== 'undefined') {
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(60, barCanvas.clientWidth / barCanvas.clientHeight, 0.1, 100);
    camera.position.set(0, 2.2, 5.2);

    const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
    renderer.setSize(barCanvas.clientWidth, barCanvas.clientHeight);
    barCanvas.appendChild(renderer.domElement);

    // Cyber Color Palette
    const colorsList = [0x00F5FF, 0x3EA6FF, 0x7B3FFB, 0x00FF9D];
    const heights = [1.8, 2.7, 3.4, 2.2];

    heights.forEach((h, i) => {
      const geom = new THREE.BoxGeometry(0.6, h, 0.6);
      const mat = new THREE.MeshPhongMaterial({
        color: colorsList[i],
        emissive: colorsList[i],
        emissiveIntensity: 0.3,
        shininess: 100
      });
      const mesh = new THREE.Mesh(geom, mat);
      mesh.position.set((i - 1.5) * 1.1, h / 2, 0);
      scene.add(mesh);
    });

    const light1 = new THREE.DirectionalLight(0x00F5FF, 1.5);
    light1.position.set(2, 4, 3);
    scene.add(light1);

    const light2 = new THREE.PointLight(0x7B3FFB, 2, 10);
    light2.position.set(-2, 2, 2);
    scene.add(light2);

    scene.add(new THREE.AmbientLight(0xffffff, 0.5));

    function render3D() {
      requestAnimationFrame(render3D);
      scene.rotation.y += 0.008;
      renderer.render(scene, camera);
    }
    render3D();
  }
});
