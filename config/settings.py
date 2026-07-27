"""
Django settings for the project.
This file contains the main configuration for your Django application.
"""

from pathlib import Path
from decouple import config   # pip install python-decouple

# The main project folder (used to build file paths)
BASE_DIR = Path(__file__).resolve().parent.parent

# =========================
# Security Settings
# =========================

# Secret key used by Django for security (keep it private in production)
SECRET_KEY = config('SECRET_KEY')

# Shows detailed error pages when True (only for development)
DEBUG = True

# List of domains that are allowed to access the project
ALLOWED_HOSTS = []


# =========================
# AI / LLM Configuration   (Secure Key Management)
# =========================
# An API key is a CREDENTIAL: it costs real money and grants real access.
# We load it here, in ONE place, from the .env file. Everything else
# (the client) READS it from settings — it never touches the env itself.
#   .env  ->  OPENAI_API_KEY=sk-...
#             OPENAI_MODEL=gpt-...
OPENAI_API_KEY = config('OPENAI_API_KEY')
OPENAI_MODEL = config('OPENAI_MODEL')

# Reusable summary limits — overridable per-environment from .env, with
# sensible defaults so the service works even if they aren't set.
AI_SUMMARY_MIN_INPUT = config('AI_SUMMARY_MIN_INPUT', default=20, cast=int)
AI_SUMMARY_MAX_LENGTH = config('AI_SUMMARY_MAX_LENGTH', default=2000, cast=int)

# =========================
# Installed Applications
# =========================

# Apps that are available in this Django project
INSTALLED_APPS = [
    'django.contrib.admin',         # Django admin dashboard
    'django.contrib.auth',          # User authentication system
    'django.contrib.contenttypes',  # Content type framework
    'django.contrib.sessions',      # Session management
    'django.contrib.messages',      # Flash messages (success, error, etc.)
    'django.contrib.staticfiles',   # Static files (CSS, JS, Images)

    'blog',                         # Our custom blog app
    'rest_framework',  # pip install djangorestframework
    'drf_yasg',  # pip install drf-yasg  (Swagger docs)
]


# =========================
# Middleware
# =========================

# Middleware processes every request and response
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',          # Security features
    'django.contrib.sessions.middleware.SessionMiddleware',   # Handles user sessions
    'django.middleware.common.CommonMiddleware',              # Common request/response features
    'django.middleware.csrf.CsrfViewMiddleware',              # Protects against CSRF attacks
    'django.contrib.auth.middleware.AuthenticationMiddleware',# Handles logged-in users
    'django.contrib.messages.middleware.MessageMiddleware',   # Enables messages
    'django.middleware.clickjacking.XFrameOptionsMiddleware', # Protects against clickjacking
]


# Main URL configuration file
ROOT_URLCONF = 'config.urls'


# =========================
# Templates
# =========================

# Configuration for HTML templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# Used when deploying the project
WSGI_APPLICATION = 'config.wsgi.application'


# =========================
# Database — PostgreSQL via .env
# =========================

# ---- DEFAULT WAY (SQLite — zero setup, good for learning) ----
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# ---- CUSTOMIZED WAY (PostgreSQL via .env — production practice) ----
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config('DATABASE_NAME'),
        'USER': config('DATABASE_USER'),
        'PASSWORD': config('DATABASE_PASSWORD'),
        'HOST': config('DATABASE_HOST'),
        'PORT': config('DATABASE_PORT'),
        'OPTIONS': {
            'options': f"-c search_path={config('DATABASE_SCHEMA', default='public')}"
        },
    }
}


# =========================
# Password Validation
# =========================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# =========================
# DRF — Rate Limiting & Abuse Prevention
# =========================
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_RATES': {
        'anon': '20/hour',    # per-IP  (if you enable AnonRateThrottle)
        'user': '100/hour',   # per-account (if you enable UserRateThrottle)
        'ai':   '10/hour',    # the STRICT cap for the AI endpoint
    },
    # Global throttling is left OFF; only the costly AI view is throttled,
    # via SummarizeThrottle in blog/views/summarize.py.
}


# =========================
# Language & Time
# =========================

# Default language of the project
LANGUAGE_CODE = 'en-us'

# Default time zone
TIME_ZONE = 'UTC'

# Enable Django's internationalization features
USE_I18N = True

# Store dates and times with time zone support
USE_TZ = True


# =========================
# Static Files
# =========================

# URL used to serve CSS, JavaScript, and images
STATIC_URL = 'static/'
