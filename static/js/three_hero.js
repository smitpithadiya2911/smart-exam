// Three.js 3D EdTech & Academic Tools Universe Engine
document.addEventListener('DOMContentLoaded', () => {
  const container = document.getElementById('hero-3d-canvas');
  if (!container || typeof THREE === 'undefined') return;

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(55, window.innerWidth / window.innerHeight, 0.1, 1000);
  
  // Position camera closer to clearly show books, pens, and educational items
  camera.position.set(0, 0.8, 4.5);
  camera.lookAt(0, 0, 0);

  const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
  renderer.setSize(window.innerWidth, window.innerHeight);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  container.appendChild(renderer.domElement);

  // Lighting System
  const mainLight = new THREE.DirectionalLight(0x00F5FF, 3.0);
  mainLight.position.set(5, 8, 5);
  scene.add(mainLight);

  const goldLight = new THREE.PointLight(0xFFD700, 3.5, 20);
  goldLight.position.set(0, 0, 2);
  scene.add(goldLight);

  const ambientLight = new THREE.AmbientLight(0x121A2D, 1.8);
  scene.add(ambientLight);

  // ==========================================================================
  // 1. CENTERPIECE: 3D GRADUATION MORTARBOARD CAP & KNOWLEDGE CORE
  // ==========================================================================
  const centerGroup = new THREE.Group();
  centerGroup.position.set(0, 0.1, 0);
  scene.add(centerGroup);

  // Cap Diamond Board
  const boardGeom = new THREE.BoxGeometry(1.25, 0.07, 1.25);
  const capMat = new THREE.MeshStandardMaterial({ color: 0x0A1628, metalness: 0.8, roughness: 0.2 });
  const boardMesh = new THREE.Mesh(boardGeom, capMat);
  boardMesh.rotation.y = Math.PI / 4;
  boardMesh.rotation.x = 0.15;
  centerGroup.add(boardMesh);

  // Cap Skull Dome Base
  const domeGeom = new THREE.CylinderGeometry(0.35, 0.38, 0.28, 24);
  const domeMesh = new THREE.Mesh(domeGeom, capMat);
  domeMesh.position.y = -0.16;
  centerGroup.add(domeMesh);

  // Golden Tassel String & Button
  const btnGeom = new THREE.SphereGeometry(0.07, 16, 16);
  const goldMat = new THREE.MeshStandardMaterial({ color: 0xFFD700, metalness: 0.9, roughness: 0.1 });
  const btnMesh = new THREE.Mesh(btnGeom, goldMat);
  btnMesh.position.y = 0.05;
  centerGroup.add(btnMesh);

  const tasselGeom = new THREE.CylinderGeometry(0.015, 0.035, 0.45);
  const tasselMesh = new THREE.Mesh(tasselGeom, goldMat);
  tasselMesh.position.set(0.35, -0.15, 0.35);
  tasselMesh.rotation.z = -0.2;
  centerGroup.add(tasselMesh);

  // Holographic Knowledge Orbit Rings
  for (let i = 0; i < 3; i++) {
    const ringGeom = new THREE.TorusGeometry(0.95 + i * 0.15, 0.012, 16, 64);
    const ringMat = new THREE.MeshBasicMaterial({ color: i % 2 === 0 ? 0x00F5FF : 0x7B3FFB, transparent: true, opacity: 0.65 });
    const ringMesh = new THREE.Mesh(ringGeom, ringMat);
    ringMesh.rotation.x = Math.PI / 2 + (i * 0.3);
    ringMesh.rotation.y = i * 0.4;
    centerGroup.add(ringMesh);
  }

  // ==========================================================================
  // 2. HELPER FUNCTIONS TO BUILD 3D EDUCATIONAL TOOLS
  // ==========================================================================

  // Tool 1: Open Textbook
  function createBookMesh() {
    const bookGroup = new THREE.Group();
    const coverMat = new THREE.MeshStandardMaterial({ color: 0x00A8FF, metalness: 0.5, roughness: 0.3 });
    const pageMat = new THREE.MeshStandardMaterial({ color: 0xFFFFFF, roughness: 0.9 });

    // Left Page Block
    const pageL = new THREE.Mesh(new THREE.BoxGeometry(0.3, 0.4, 0.04), pageMat);
    pageL.position.x = -0.16;
    pageL.rotation.y = 0.25;
    bookGroup.add(pageL);

    // Right Page Block
    const pageR = new THREE.Mesh(new THREE.BoxGeometry(0.3, 0.4, 0.04), pageMat);
    pageR.position.x = 0.16;
    pageR.rotation.y = -0.25;
    bookGroup.add(pageR);

    // Hardcover Spine
    const spine = new THREE.Mesh(new THREE.CylinderGeometry(0.04, 0.04, 0.42, 12), coverMat);
    spine.rotation.x = Math.PI / 2;
    bookGroup.add(spine);

    return bookGroup;
  }

  // Tool 2: Fountain Pen & Nib
  function createPenMesh() {
    const penGroup = new THREE.Group();
    const bodyMat = new THREE.MeshStandardMaterial({ color: 0x0F172A, metalness: 0.9, roughness: 0.1 });
    const goldMat = new THREE.MeshStandardMaterial({ color: 0xFFD700, metalness: 0.9, roughness: 0.1 });

    // Barrel Body
    const body = new THREE.Mesh(new THREE.CylinderGeometry(0.045, 0.045, 0.65, 16), bodyMat);
    penGroup.add(body);

    // Nib Cone Tip
    const nib = new THREE.Mesh(new THREE.ConeGeometry(0.045, 0.2, 16), goldMat);
    nib.position.y = 0.425;
    penGroup.add(nib);

    // Gold Trim Ring
    const trim = new THREE.Mesh(new THREE.TorusGeometry(0.048, 0.008, 12, 24), goldMat);
    trim.rotation.x = Math.PI / 2;
    trim.position.y = 0.15;
    penGroup.add(trim);

    return penGroup;
  }

  // Tool 3: Certificate Diploma Scroll
  function createScrollMesh() {
    const scrollGroup = new THREE.Group();
    const paperMat = new THREE.MeshStandardMaterial({ color: 0xFAF5FF, roughness: 0.8 });
    const ribbonMat = new THREE.MeshStandardMaterial({ color: 0xFF0055, metalness: 0.5 });

    // Rolled Paper Body
    const paper = new THREE.Mesh(new THREE.CylinderGeometry(0.08, 0.08, 0.65, 20), paperMat);
    paper.rotation.z = Math.PI / 2;
    scrollGroup.add(paper);

    // Tied Ribbon Ring
    const ribbon = new THREE.Mesh(new THREE.TorusGeometry(0.088, 0.02, 12, 24), ribbonMat);
    ribbon.rotation.y = Math.PI / 2;
    scrollGroup.add(ribbon);

    return scrollGroup;
  }

  // Tool 4: Idea Lightbulb
  function createLightbulbMesh() {
    const bulbGroup = new THREE.Group();
    const glassMat = new THREE.MeshPhysicalMaterial({ color: 0xFFD700, emissive: 0xFFD700, emissiveIntensity: 0.8, transparent: true, opacity: 0.85 });
    const baseMat = new THREE.MeshStandardMaterial({ color: 0x94A3B8, metalness: 0.9 });

    // Glass Bulb
    const bulb = new THREE.Mesh(new THREE.SphereGeometry(0.2, 20, 20), glassMat);
    bulbGroup.add(bulb);

    // Screw Base
    const base = new THREE.Mesh(new THREE.CylinderGeometry(0.09, 0.09, 0.15, 16), baseMat);
    base.position.y = -0.22;
    bulbGroup.add(base);

    return bulbGroup;
  }

  // Tool 5: AI Neural Atom Node
  function createAtomMesh() {
    const atomGroup = new THREE.Group();
    const coreMat = new THREE.MeshStandardMaterial({ color: 0x00F5FF, emissive: 0x00A8FF });
    const ringMat = new THREE.MeshBasicMaterial({ color: 0x7B3FFB, wireframe: true });

    // Nucleus Core
    const nuc = new THREE.Mesh(new THREE.SphereGeometry(0.14, 16, 16), coreMat);
    atomGroup.add(nuc);

    // 3 Orbiting Electron Rings
    for (let i = 0; i < 3; i++) {
      const ring = new THREE.Mesh(new THREE.TorusGeometry(0.32, 0.01, 12, 32), ringMat);
      ring.rotation.x = (i * Math.PI) / 3;
      ring.rotation.y = (i * Math.PI) / 4;
      atomGroup.add(ring);
    }

    return atomGroup;
  }

  // Tool 6: Exam Clipboard
  function createClipboardMesh() {
    const boardGroup = new THREE.Group();
    const woodMat = new THREE.MeshStandardMaterial({ color: 0x1E293B, roughness: 0.4 });
    const clipMat = new THREE.MeshStandardMaterial({ color: 0x00F5FF, metalness: 0.9 });

    // Board
    const board = new THREE.Mesh(new THREE.BoxGeometry(0.36, 0.48, 0.03), woodMat);
    boardGroup.add(board);

    // Top Clip
    const clip = new THREE.Mesh(new THREE.BoxGeometry(0.16, 0.05, 0.04), clipMat);
    clip.position.set(0, 0.22, 0.02);
    boardGroup.add(clip);

    return boardGroup;
  }

  // ==========================================================================
  // 3. ORBITING TOOLS ARRAY SETUP
  // ==========================================================================
  const toolFactories = [
    { create: createBookMesh,      dist: 1.6, speed: 0.020 },
    { create: createPenMesh,       dist: 2.2, speed: 0.016, isPen: true },
    { create: createScrollMesh,    dist: 2.8, speed: 0.013 },
    { create: createLightbulbMesh, dist: 3.4, speed: 0.010 },
    { create: createAtomMesh,      dist: 4.1, speed: 0.008 },
    { create: createClipboardMesh, dist: 4.8, speed: 0.006 }
  ];

  const tools = [];

  toolFactories.forEach((cfg) => {
    // Faint Knowledge Track Ring
    const trackGeom = new THREE.RingGeometry(cfg.dist - 0.012, cfg.dist + 0.012, 64);
    const trackMat = new THREE.MeshBasicMaterial({ color: 0x00F5FF, side: THREE.DoubleSide, transparent: true, opacity: 0.14 });
    const track = new THREE.Mesh(trackGeom, trackMat);
    track.rotation.x = Math.PI / 2.2;
    scene.add(track);

    // Pivot Group at center
    const pivot = new THREE.Group();
    pivot.rotation.x = Math.PI / 8;
    scene.add(pivot);

    // Create Tool Mesh
    const mesh = cfg.create();
    mesh.position.x = cfg.dist;
    pivot.add(mesh);

    tools.push({
      pivot: pivot,
      mesh: mesh,
      speed: cfg.speed,
      angle: Math.random() * Math.PI * 2,
      isPen: cfg.isPen
    });
  });

  // Glowing Cyan Ink Trail Particles for Fountain Pen
  const inkTrailCount = 60;
  const inkGeom = new THREE.BufferGeometry();
  const inkPositions = new Float32Array(inkTrailCount * 3);
  inkGeom.setAttribute('position', new THREE.BufferAttribute(inkPositions, 3));
  const inkMat = new THREE.PointsMaterial({ color: 0x00F5FF, size: 0.055, transparent: true, opacity: 0.85 });
  const inkTrailMesh = new THREE.Points(inkGeom, inkMat);
  scene.add(inkTrailMesh);

  // ==========================================================================
  // 4. INTERACTIVE CLICK EXPLOSION KNOWLEDGE PARTICLES
  // ==========================================================================
  const clickParticleCount = 80;
  const clickGeom = new THREE.BufferGeometry();
  const clickPositions = new Float32Array(clickParticleCount * 3);
  const clickVelocities = [];

  for (let i = 0; i < clickParticleCount; i++) {
    clickPositions[i * 3] = 0;
    clickPositions[i * 3 + 1] = -9999; // Hidden initial position
    clickPositions[i * 3 + 2] = 0;
    clickVelocities.push(new THREE.Vector3());
  }

  clickGeom.setAttribute('position', new THREE.BufferAttribute(clickPositions, 3));
  const clickMat = new THREE.PointsMaterial({ color: 0x00FF9D, size: 0.08, transparent: true, opacity: 1.0 });
  const clickParticlesMesh = new THREE.Points(clickGeom, clickMat);
  scene.add(clickParticlesMesh);

  // Trigger 3D Knowledge Particle Explosion on Mouse Click
  window.addEventListener('click', (e) => {
    // Convert click coordinates to 3D Normalized Device Space
    const vec = new THREE.Vector3(
      (e.clientX / window.innerWidth) * 2 - 1,
      -(e.clientY / window.innerHeight) * 2 + 1,
      0.5
    );
    vec.unproject(camera);
    const dir = vec.sub(camera.position).normalize();
    const distance = -camera.position.z / dir.z;
    const clickPos = camera.position.clone().add(dir.multiplyScalar(distance));

    const posArr = clickParticlesMesh.geometry.attributes.position.array;

    for (let i = 0; i < clickParticleCount; i++) {
      posArr[i * 3] = clickPos.x;
      posArr[i * 3 + 1] = clickPos.y;
      posArr[i * 3 + 2] = clickPos.z;

      // Random 3D explosion direction
      const vx = (Math.random() - 0.5) * 0.12;
      const vy = (Math.random() - 0.5) * 0.12;
      const vz = (Math.random() - 0.5) * 0.12;
      clickVelocities[i].set(vx, vy, vz);
    }
    clickParticlesMesh.geometry.attributes.position.needsUpdate = true;
  });

  // Background Ambient Knowledge Starfield
  const starCount = 450;
  const starGeom = new THREE.BufferGeometry();
  const starPositions = new Float32Array(starCount * 3);
  for (let i = 0; i < starCount; i++) {
    starPositions[i * 3] = (Math.random() - 0.5) * 26;
    starPositions[i * 3 + 1] = (Math.random() - 0.5) * 26;
    starPositions[i * 3 + 2] = (Math.random() - 0.5) * 14 - 2;
  }
  starGeom.setAttribute('position', new THREE.BufferAttribute(starPositions, 3));
  const starMat = new THREE.PointsMaterial({ color: 0xFFFFFF, size: 0.035, transparent: true, opacity: 0.8 });
  const starField = new THREE.Points(starGeom, starMat);
  scene.add(starField);

  // Mouse Parallax
  let mouseX = 0, mouseY = 0;
  window.addEventListener('mousemove', (e) => {
    mouseX = (e.clientX / window.innerWidth - 0.5) * 0.4;
    mouseY = (e.clientY / window.innerHeight - 0.5) * 0.4;
  });

  // ==========================================================================
  // RENDER LOOP & TOOL MOVEMENT PHYSICS
  // ==========================================================================
  let clock = new THREE.Clock();

  function animate() {
    requestAnimationFrame(animate);

    const delta = clock.getDelta();
    const time = clock.getElapsedTime();

    // Rotate Centerpiece Graduation Cap & Orbit Rings
    boardMesh.rotation.y += 0.005;
    tasselMesh.rotation.z = -0.2 + Math.sin(time * 3) * 0.05;

    // Orbit & Rotate Educational Tools
    tools.forEach((t) => {
      t.angle += t.speed * 0.7;
      t.pivot.rotation.y = t.angle;
      t.mesh.rotation.y += 0.015;
      t.mesh.rotation.x = Math.sin(time * 2 + t.angle) * 0.15; // Floating movement

      // Mouse magnetic tilt attraction
      t.mesh.rotation.z += (mouseX * 0.2 - t.mesh.rotation.z) * 0.05;
    });

    // Animate Interactive Click Particle Physics
    const clickArr = clickParticlesMesh.geometry.attributes.position.array;
    for (let i = 0; i < clickParticleCount; i++) {
      if (clickArr[i * 3 + 1] > -9000) {
        clickArr[i * 3] += clickVelocities[i].x;
        clickArr[i * 3 + 1] += clickVelocities[i].y;
        clickArr[i * 3 + 2] += clickVelocities[i].z;
        clickVelocities[i].multiplyScalar(0.96); // Drag resistance
      }
    }
    clickParticlesMesh.geometry.attributes.position.needsUpdate = true;

    // Mouse Camera Parallax
    scene.rotation.y += (mouseX - scene.rotation.y) * 0.05;
    scene.rotation.x += (-mouseY - scene.rotation.x) * 0.05;

    renderer.render(scene, camera);
  }
  animate();

  // Canvas Resize Handler
  window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
  });
});





