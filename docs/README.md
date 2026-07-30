# Smart Online Examination & Learning Analytics System
### BCA Final Year Project & EdTech Startup Product

A production-ready, visually premium "Smart Online Examination & Learning Analytics System" built with **Python Django 5.x**, **MySQL 8.x** (via Laragon), **Django REST Framework**, **Chart.js 2D Analytics**, **Three.js 3D Visual Accents**, **GSAP**, **ReportLab PDF Generator**, and **python-qrcode**.

---

## 🌟 Key Features & Highlights

1. **Modern EdTech Glass UI/UX Design System**:
   - Glassmorphic translucent cards, custom CSS design tokens (`--color-primary`, `--color-accent`), geometric typography (Poppins & Inter).
   - Full Dark Mode persistence with localStorage & backend user preference sync.
   - Ambient 3D Three.js rotating hero background on login/landing pages.
   - 3D mouse parallax tilt certificate cards and 3D shiny achievement medals.

2. **Full Role-Based Access Control (RBAC)**:
   - **Super Admin**: Complete CRUD over departments, courses, semesters, subjects, teachers, students, exam bank, system reports, announcements, and access audit logs.
   - **Teacher**: Create/schedule exams, question bank management with Excel import/export, random question generator, manual subjective grading interface.
   - **Student**: Exam calendar, live examination room with color-coded question palette, live countdown timer, AJAX autosave, anti-cheat detection, instant PDF scorecard, QR certificate verification, AI learning recommendations, and 3D achievement badges.

3. **Proctored Anti-Cheating Engine**:
   - Detects browser tab switching, window blur/focus loss, full-screen mode exit, right-click, and copy-paste attempts.
   - Real-time AJAX violation logger automatically disqualifies and auto-submits exam when the configured violation threshold is exceeded.

4. **Rule-Based AI Learning Recommendation Engine**:
   - Identifies weak focus topics (< 50% accuracy) from past exam attempts.
   - Generates personalized study recommendations, suggested review chapters, recommended practice question sets, and score trend predictions.

5. **Official PDF Scorecards & QR Certificate Verification**:
   - Automated objective question grading with negative marking calculation.
   - ReportLab PDF scorecard generator with question-wise analysis.
   - `python-qrcode` certificate generator pointing to a **Public No-Login Verification Portal** (`/certificates/verify/<uuid>/`).

6. **RESTful API & Interactive Swagger Docs**:
   - Full DRF v1 endpoints under `/api/v1/` with auto-generated interactive OpenAPI Swagger UI docs at `/api/docs/`.
