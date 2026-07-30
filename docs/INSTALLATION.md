# Installation & Setup Guide
## Smart Online Examination & Learning Analytics System

### Prerequisites
1. **Python 3.12+**
2. **Laragon / MySQL 8.x** (Started on `localhost:3306` with user `root`, no password)

---

### Step 1: Database Setup (Laragon / MySQL)
1. Open Laragon -> Click **Start All** (MySQL server running on port 3306).
2. Open MySQL Terminal / HeidiSQL / phpMyAdmin and create database `online_exam_db`:
   ```sql
   CREATE DATABASE online_exam_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

---

### Step 2: Install Python Dependencies
In your project directory:
```bash
pip install -r requirements.txt
```

---

### Step 3: Run Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

---

### Step 4: Load Realistic Sample Seed Data
Populate realistic departments, courses, semesters, subjects, teachers, students, question bank, exams, and results:
```bash
python manage.py seed_data
```

---

### Step 5: Start Django Development Server
```bash
python manage.py runserver
```

Open your browser at `http://127.0.0.1:8000/`.

---

### Pre-Configured Login Credentials (via `seed_data`):
- **Super Admin**: `smitpithadiya@gmail.com` / `Smit#2911`
- **Teacher**: `prof.sharma@exam.com` / `Password123`
- **Student**: `student.rahul@exam.com` / `Password123`
- **API Documentation**: `http://127.0.0.1:8000/api/docs/`
