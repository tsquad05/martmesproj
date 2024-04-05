

from pathlib import Path
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-p^&9m-v^^!+5113stm^-l32!how=$)rg1r+c@mq%t^&e#h^x0r"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    "django.contrib.humanize",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'django.contrib.sitemaps',

    #custom apps
    "userauths",
    'taggit',
    "core",
    'ckeditor',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]

ROOT_URLCONF = "martmesproj.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, 'templates')],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "core.context_processor.default", 
                'core.context_processor.recommended_products',
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                
            ],
        },
    },
]

WSGI_APPLICATION = "martmesproj.wsgi.application"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres.vruhzvoeolhtwmpwtrvu',
        'PASSWORD': '6MgOYsfCH1Aks0Rt',
        'HOST': 'aws-0-us-west-1.pooler.supabase.com',
        'PORT': '5432',
    }
}



AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Africa/Lagos"

USE_I18N = True

USE_TZ = True


STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
AUTH_USER_MODEL = 'userauths.User'

SENSITIVE_VARIABLE = "re_XKERd4Zs_7YbCWHpaoPQbeA7YGZMjFgGg"


SESSION_COOKIE_AGE = 60 * 60 * 24 * 4



CKEDITOR_UPLOAD_PATH = 'uploads/'

CKEDITOR_CONFIGS = {
    'default':{
        'skin': 'moono',
        'codeSnippet_theme': 'monokai',
        'toolbar': 'all',
        'extraPlugins': ','.join(['codesnippet', 'widget', 'dialog','clipboard',]),
    }
}
STATICFILES_STORAGE = 'pipeline.storage.PipelineStorage'

PIPELINE = {
    'COMPILERS': ('pipeline.compilers.sass.SASSCompiler',),
    'CSS_COMPRESSOR': 'pipeline.compressors.yuglify.YuglifyCompressor',
    'JS_COMPRESSOR': 'pipeline.compressors.yuglify.YuglifyCompressor',
}

CLOUD_NAME = 'de3pm0yxc'
API_KEY ='799178857418374'
API_SECRET = 'DnfRY1QDLUMzELSeNyfTxgbMYN8'
LOGIN_URL = '/sign-in/'