"""
Django settings for Smart Online Examination & Learning Analytics System.
Configured for Python 3.12+, Django 5.x, MySQL 8.x (Laragon), and DRF.
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env file if it exists
_env_path = BASE_DIR / '.env'
if _env_path.exists():
    with open(_env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, _, value = line.partition('=')
                os.environ.setdefault(key.strip(), value.strip())


SECRET_KEY =  os.environ.get(
    'SECRET_KEY',
    'django-insecure-default-key'
)

# Disable DEBUG automatically on Vercel for better performance and security
DEBUG = os.environ.get('VERCEL') != '1'

ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    'django.contrib.sites',

'allauth',
'allauth.account',
'allauth.socialaccount',
'allauth.socialaccount.providers.google',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third Party Apps
    'rest_framework',
    'drf_spectacular',

    # Project Modules
    'accounts.apps.AccountsConfig',
    'departments.apps.DepartmentsConfig',
    'courses.apps.CoursesConfig',
    'semesters.apps.SemestersConfig',
    'subjects.apps.SubjectsConfig',
    'students.apps.StudentsConfig',
    'teachers.apps.TeachersConfig',
    'questions.apps.QuestionsConfig',
    'exams.apps.ExamsConfig',
    'results.apps.ResultsConfig',
    'analytics.apps.AnalyticsConfig',
    'notifications.apps.NotificationsConfig',
    'certificates.apps.CertificatesConfig',
    'feedback.apps.FeedbackConfig',
    'leaderboard.apps.LeaderboardConfig',
    'reports.apps.ReportsConfig',
    'api.apps.ApiConfig',

    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'notifications.context_processors.unread_notifications',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database Configuration: MySQL 8.x (Laragon Defaults) with dynamic fallback
DATABASE_URL = os.environ.get('DATABASE_URL')
USE_MYSQL = os.environ.get('USE_MYSQL', 'True').lower() in ('true', '1')

if DATABASE_URL:
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
elif USE_MYSQL:
    try:
        import pymysql
        pymysql.install_as_MySQLdb()
        
        # Test connection credentials to find the correct password
        mysql_pwd = ''
        try:
            # Try default empty password
            conn = pymysql.connect(host='localhost', port=3306, user='root', password='', connect_timeout=1)
            conn.close()
        except Exception:
            try:
                # Try password 'root' (often used in some Laragon/MAMP setups)
                conn = pymysql.connect(host='localhost', port=3306, user='root', password='root', connect_timeout=1)
                conn.close()
                mysql_pwd = 'root'
            except Exception as e:
                # If both fail, raise connection error to fallback or print
                raise e

        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': 'smart_exam',
                'USER': 'root',
                'PASSWORD': mysql_pwd,
                'HOST': 'localhost',
                'PORT': '3306',
                'OPTIONS': {
                    'charset': 'utf8mb4',
                    'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
                },
            }
        }
    except Exception:
        import shutil
        db_path = BASE_DIR / 'db.sqlite3'
        if os.environ.get('VERCEL') == '1':
            tmp_db_path = Path('/tmp/db.sqlite3')
            if not tmp_db_path.exists() and db_path.exists():
                shutil.copy2(db_path, tmp_db_path)
            db_path = tmp_db_path
            
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': db_path,
            }
        }
else:
    import shutil
    db_path = BASE_DIR / 'db.sqlite3'
    if os.environ.get('VERCEL') == '1':
        tmp_db_path = Path('/tmp/db.sqlite3')
        if not tmp_db_path.exists() and db_path.exists():
            shutil.copy2(db_path, tmp_db_path)
        db_path = tmp_db_path

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': db_path,
        }
    }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Custom User Model
AUTH_USER_MODEL = 'accounts.User'

# Django Allauth Configuration
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

# Static & Media Files
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Auth URLs
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'login'

# Google OAuth Configuration
GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID', 'YOUR_GOOGLE_CLIENT_ID.apps.googleusercontent.com')

SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "APP": {
            "client_id": GOOGLE_CLIENT_ID,
            "secret": os.environ.get("GOOGLE_CLIENT_SECRET", "dummy_secret"),
            "key": ""
        },
        "SCOPE": [
            "profile",
            "email",
        ],
        "AUTH_PARAMS": {
            "access_type": "online",
        },
    }
}

# Email Backend — Gmail SMTP for real delivery
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")

DEFAULT_FROM_EMAIL = os.environ.get('EMAIL_HOST_USER', 'noreply@exam.com')

# Fast2SMS API Key for real SMS delivery
FAST2SMS_API_KEY = os.environ.get('FAST2SMS_API_KEY', '')

# REST Framework Configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

# Swagger / OpenAPI Settings
SPECTACULAR_SETTINGS = {
    'TITLE': 'Smart Online Examination & Learning Analytics API',
    'DESCRIPTION': 'RESTful APIs for Students, Teachers, Exams, Analytics, Certificates and Reports.',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}

# --- VERCEL FIXES FOR LOGIN ---
# Vercel is a serverless environment. If you are using SQLite, it will be 
# read-only/ephemeral across requests. By default, Django stores sessions in the database.
# To make login work without a persistent database, we store sessions in the user's cookies.
SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'

# Ensure CSRF and session cookies work properly on Vercel's HTTPS domains
CSRF_TRUSTED_ORIGINS = ['https://*.vercel.app', 'http://127.0.0.1:8000', 'http://localhost:8000']
env_csrf = os.environ.get('CSRF_TRUSTED_ORIGINS')
if env_csrf:
    CSRF_TRUSTED_ORIGINS.extend([origin.strip() for origin in env_csrf.split(',')])

if os.environ.get('VERCEL') == '1':
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True


SITE_ID = 1
