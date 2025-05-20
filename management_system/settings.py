import os
from pathlib import Path
from django.core.management.utils import get_random_secret_key

# Build paths inside the project like this: BASE_DIR / 'subdir'.
#BASE_DIR = Path(__file__).resolve().parent.parent
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', get_random_secret_key())

# Security settings
DEBUG = 'False'
#ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'itsupportserver.internal', '192.168.88.196']
#DEBUG = os.getenv('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1,itsupportserver.internal,192.168.88.196').split(',')
#CSRF_TRUSTED_ORIGINS = os.getenv('CSRF_TRUSTED_ORIGINS', 'http://localhost,http://127.0.0.1,http://192.168.88.196').split(',')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'sslserver',
    # Third-party apps
    'crispy_forms',
    'crispy_bootstrap5',
    'django_tables2',
    'django_filters',
    'import_export',
    'django.contrib.gis',

    'django_celery_beat',
    #'django_rename_app'

    # Local apps
    'core',
    'employee_management',
    'asset_management',
    'warehouse_management',
    'vendorescalation_management',
    'user_activity',
    'attendance_tracking',
    'report_generation',
    'live',
    'search',
    'file_attachment',
    'email_management',  # New app
    'scan_hardware',
    'administration_management',
    'posteio_integration',
    'custom_email_client',
    'security',
     #2MFA apps
    'two_factor_auth',
    'django_otp',

    'django_otp.plugins.otp_totp',  # Time-based OTP
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django_otp.middleware.OTPMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'live.middleware.LocationTrackingMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # ✅ Add this line
]

ROOT_URLCONF = 'management_system.urls'

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
                'django.template.context_processors.media',
               
            ],
        },
    },
]

WSGI_APPLICATION = 'management_system.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE', 'django.db.backends.postgresql'),
        'NAME': os.getenv('DB_NAME', 'management_system'),
        'USER': os.getenv('DB_USER', 'mgmt_user'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'securepassword'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}

# For SQLite fallback
if DATABASES['default']['ENGINE'] == 'django.db.backends.sqlite3':
    DATABASES['default']['NAME'] = os.path.join(BASE_DIR, 'db.sqlite3')

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Karachi'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
# Media files (uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Authentication

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
LOGIN_URL = 'two_factor_login'
#LOGIN_REDIRECT_URL = '/reports/'


# Session settings
SESSION_COOKIE_AGE = 3600  # 1 hour
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Use database-backed sessions
SESSION_ENGINE = "django.contrib.sessions.backends.db"
SESSION_COOKIE_SECURE = False  # For development only


# Security headers (for production)
if not DEBUG:
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Email configuration
#EMAIL_BACKEND = 'posteio_integration.email_backend.PosteIOEmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'mail.itsupportserver.internal'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'no-reply@itsupportserver.internal'
EMAIL_HOST_PASSWORD = 'Ufone@2288'  # Set if required
DEFAULT_FROM_EMAIL = 'no-reply@itsupportserver.internal'
#EMAIL_BACKEND = 'custom_email_client.email_backend.CustomEmailBackend'
#EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
#EMAIL_HOST = 'localhost'
#EMAIL_PORT = 1025
#EMAIL_HOST_USER = ''
#EMAIL_HOST_PASSWORD = ''
#DEFAULT_FROM_EMAIL = 'test@localhost'
#EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
#EMAIL_PORT = os.getenv('EMAIL_PORT', 587)
#EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', True)
#EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', 'your-email@gmail.com')
#EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', 'your-email-password')
#DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'your-email@gmail.com')

# Third-party app configurations
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

DJANGO_TABLES2_TEMPLATE = "django_tables2/bootstrap5.html"

# File upload settings
FILE_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10MB

# Biometric settings
BIOMETRIC_IMAGE_SIZE = (300, 300)  # Width, Height in pixels
BIOMETRIC_IMAGE_QUALITY = 85  # Percentage

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG' if DEBUG else 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'debug.log'),
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['file', 'console'],
        'level': 'DEBUG' if DEBUG else 'INFO',
    },
}

# Custom settings
APP_VERSION = '1.0.0'
MAX_EMPLOYEE_RECORDS = 1000  # For pagination testing

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
#    'authentication.backends.CustomUserAuthBackend',  # If you have custom backend
]

# Add to the bottom of settings.py
#GEOIP_PATH = os.path.join(BASE_DIR, 'geoip')  # Path to your geoip folder
#GEOIP_CITY = 'GeoLite2-City.mmdb'  # City database filename
#GEOIP_COUNTRY = 'GeoLite2-Country.mmdb'  # Country database filename

# Add to your existing settings.py
#NOMINATIM_EMAIL = 'asaboorcai@gmail.com'

# Google Maps API Key
#GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY','dff9139a506c4afd8e4aad7227392733')

# Remove Google Maps API key and add:
LEAFLET_CONFIG = {
    'DEFAULT_CENTER': (30.3753, 69.3451),  # Pakistan coordinates
    'DEFAULT_ZOOM': 5,
    'MIN_ZOOM': 3,
    'MAX_ZOOM': 18,
    'TILES': 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'live': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    },
}

TWO_FACTOR_PATCH_ADMIN = False

# Append to settings.py

CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'ERROR',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}

SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
