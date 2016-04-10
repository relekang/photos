import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_DIR = os.path.dirname(BASE_DIR)


def load_secrets():
    try:
        with open(os.path.join(REPO_DIR, 'secrets.json')) as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

secrets = load_secrets()

DEBUG = secrets.get('debug', True)
ALLOWED_HOSTS = secrets.get('allowed_hosts', [])
SECRET_KEY = secrets.get('secret_key', 'a secret')

AUTH_USER_MODEL = 'users.User'
LOGIN_REDIRECT_URL = '/admin/'

SOCIAL_AUTH_URL_NAMESPACE = 'social'
SOCIAL_AUTH_TWITTER_KEY = secrets.get('social_auth_twitter_key', '')
SOCIAL_AUTH_TWITTER_SECRET = secrets.get('social_auth_twitter_secret', '')

AUTHENTICATION_BACKENDS = (
    'social.backends.twitter.TwitterOAuth',
    'django.contrib.auth.backends.ModelBackend',
)


INSTALLED_APPS = [
    'photos.gallery',
    'photos.users',

    'social.apps.django_app.default',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'photos.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'photos.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': secrets.get('db_name', 'photos'),
    }
}


LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(REPO_DIR, 'static')

MEDIA_URL = '/uploads/'
MEDIA_ROOT = os.path.join(REPO_DIR, 'uploads')
