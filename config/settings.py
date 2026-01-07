"""
Django settings for config project.
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "y_e#%0ek53+(sqll)))g28^t7$r(%#c)n8%jl!2s(+5djv2igb" 

DEBUG = True

ALLOWED_HOSTS = [
    "water-management.sifatdev.uz",
    "127.0.0.1",
    "localhost",
] 

# Ilovalar ro'yxati 
INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party apps
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',
    'corsheaders',
    # 'modeltranslation',
    'hitcount',
    'tinymce',
    # 'rosetta',  # tarjima uchun
    'ckeditor',
    'ckeditor_uploader',
    
    'drf_spectacular',
    'drf_spectacular_sidecar',
    # Local apps
    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    # 'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Til sozlamalari
LANGUAGE_CODE = 'uz'

TIME_ZONE = 'Asia/Tashkent'
USE_I18N = True
USE_TZ = True

# Mavjud tillar - O'zbek tilining 2 xil yozuvi va Rus tili
LANGUAGES = [
    ('uz', 'O‘zbekcha (Lotin)'),
    ('uz-cyrl', 'O‘zbekcha (Kirill)'),
    ('ru', 'Русский'),
]

# Har bir til kodini belgilash
LANGUAGE_COOKIE_NAME = 'django_language'

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

# Tarjima uchun
# MODELTRANSLATION_DEFAULT_LANGUAGE = 'uz'
# MODELTRANSLATION_LANGUAGES = ('uz', 'uz-cyrl', 'ru')

# # Tarjima fayllari
# MODELTRANSLATION_TRANSLATION_FILES = (
#     'core.translation',
# )

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST Framework sozlamalari
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

# Telegram bot sozlamalari
TELEGRAM_BOT_TOKEN = '7977582154:AAEqxQsY40i792Vnxrzn0XdBS9iLzGye3ZQ'
TELEGRAM_CHAT_ID = '5182300111'

# Hitcount sozlamalari
HITCOUNT_KEEP_HIT_ACTIVE = {'days': 7}
HITCOUNT_HITS_PER_IP_LIMIT = 0  # cheksiz
HITCOUNT_EXCLUDE_USER_GROUP = ()

CKEDITOR_UPLOAD_PATH = "uploads/"

SPECTACULAR_SETTINGS = {
    'TITLE': 'Water Management API',
    'DESCRIPTION': 'Suv xo\'jaligi tizimi uchun API dokumentatsiyasi',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'SWAGGER_UI_DIST': 'SIDECAR',
    'SWAGGER_UI_FAVICON_HREF': 'SIDECAR',
    'REDOC_DIST': 'SIDECAR',
    'COMPONENT_SPLIT_REQUEST': True,
    'COMPONENT_NO_READ_ONLY_REQUIRED': False,
    
    # Image field'lar uchun
    'COMPONENT_SPLIT_PATCH': True,
    'COMPONENT_SPLIT_CREATE': True,

}

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3001",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "https://water-management.sifatdev.uz",
]
 
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3001",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "https://water-management.sifatdev.uz",
] 