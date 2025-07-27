from pathlib import Path
import environ, os
from datetime import timedelta

env = environ.Env(
    DEBUG = (bool, False),
    ROTATE_REFRESH_TOKENS = (bool, True),
    BLACKLIST_AFTER_ROTATION = (bool, True),
    ALLOWED_HOSTS = (list, []),
    JWT_AUTH_HTTPONLY = (bool, False)
)
TOKEN_MODEL = None
REST_USE_JWT = True
REST_AUTH = {
    'USE_JWT': True,
    'LOGIN_SERIALIZER': 'chats.serializers.CustomLoginSerializer',
    "JWT_AUTH_HTTPONLY": env("JWT_AUTH_HTTPONLY"),
}


BASE_DIR = Path(__file__).resolve().parent.parent

environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

SECRET_KEY = env('KEY')

DEBUG = env('DEBUG')

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'chats',

    # Third party apps
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework.authtoken',
    'dj_rest_auth',
    'rest_framework_simplejwt.token_blacklist',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  
]

ROOT_URLCONF = 'messaging_app.urls'

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

WSGI_APPLICATION = 'messaging_app.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': env('DB_ENGINE'),
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT'),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.BasicAuthentication', 
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
        'chats.permissions.IsParticipantOfConversation',
    ),
}

AUTH_USER_MODEL = env('AUTH_USER_MODEL')
ACCESS_TOKEN_LIFETIME = env("ACCESS_TOKEN_LIFETIME")
REFRESH_TOKEN_LIFETIME = env("REFRESH_TOKEN_LIFETIME")
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=int(ACCESS_TOKEN_LIFETIME)),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=int(REFRESH_TOKEN_LIFETIME)),
    "ROTATE_REFRESH_TOKENS": env("ROTATE_REFRESH_TOKENS"),
    "BLACKLIST_AFTER_ROTATION": env("BLACKLIST_AFTER_ROTATION"),
    "SIGNING_KEY": env('KEY'),
    "AUTH_HEADER_TYPES": ("Bearer",),
    "USER_ID_FIELD": env("USER_ID_FIELD"),
}


