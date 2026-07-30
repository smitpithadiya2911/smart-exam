# Automated & Manual Testing Documentation

## 1. Automated Test Suite
To execute Django's automated test suite across all 16 apps:
```bash
python manage.py test
```

### Test Coverage Summary:
- **Accounts**: Test custom user creation, superuser role checks, and password hashing.
- **Academic Modules**: Test model string representations and relational integrity constraints (`end_date > start_date`).
- **Exams & Results**: Test objective question auto-evaluation, negative marking arithmetic, and random question sampler service.
- **Certificates**: Test QR code URL resolution and landscape PDF reportlab document generation.
- **Analytics**: Test rule-based AI recommendation heuristic engine.

---

## 2. Manual Verification Checklist
- [x] Laragon MySQL database `online_exam_db` migration validation.
- [x] Light/Dark mode toggle persistence in `localStorage`.
- [x] Three.js 3D ambient hero background rendering on landing page.
- [x] Question palette AJAX autosave and status badge color updates.
- [x] Proctored anti-cheat violation logging (tab switch, window blur, copy-paste block).
- [x] Public QR Certificate Verification page (`/certificates/verify/<uuid>/`).
