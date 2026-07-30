# Production Deployment Guide

## Architecture Overview
- **OS**: Ubuntu 22.04 LTS / Windows Server
- **Web Server**: Nginx (Reverse Proxy & Static Asset Server)
- **WSGI Application Server**: Gunicorn / Waitress
- **Database**: MySQL 8.x
- **Process Manager**: Systemd / Supervisor

---

## Deployment Steps
1. **Clone Repository & Environment**:
   ```bash
   git clone <repo-url> /var/www/online_exam_system
   cd /var/www/online_exam_system
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Environment Variables**:
   Set `DEBUG=False`, `ALLOWED_HOSTS=['yourdomain.com']`, `USE_MYSQL=True`, `SECRET_KEY='<production-secret-key>'` in environment configuration.

3. **Collect Static & Run Migrations**:
   ```bash
   python manage.py collectstatic --noinput
   python manage.py migrate
   python manage.py seed_data
   ```

4. **Configure Nginx & Gunicorn**:
   Proxy requests to `127.0.0.1:8000` and serve `/static/` and `/media/` directly via Nginx.
