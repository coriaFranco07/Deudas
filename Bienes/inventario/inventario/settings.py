"""
Django settings for inventario project.

Generated by 'django-admin startproject' using Django 4.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
from pathlib import Path
import environ

env=environ.Env()
environ.Env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
#DEBUG = os.environ.get('DEBUG')
DEBUG=env.bool('DEBUG', default=False)
ALLOWED_HOSTS = ['*']#env.list('ALLOWED_HOSTS_DEV')

#controlar login attemps
AUTHENTICATION_BACKENDS = [
   'axes.backends.AxesBackend', # Axes must be first
   'django.contrib.auth.backends.ModelBackend',
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.clase',
    'apps.marca',
    'apps.modelo',
    'apps.tipo',
    'apps.oficina',
    'apps.bien',
    'apps.estado',
    'apps.movdata',
    'apps.operador',
    'apps.imgbien',
    'axes', #controla veces que se hace login fallido
    'crispy_forms',
    'crispy_bootstrap5',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django_session_timeout.middleware.SessionTimeoutMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'axes.middleware.AxesMiddleware',
]

ROOT_URLCONF = 'inventario.urls'

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

CRISPY_TEMPLATE_PACK = "bootstrap5"

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
            ],
        },
    },
]

WSGI_APPLICATION = 'inventario.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'inventario',
        'USER': 'inventario',
        'PASSWORD': 'data-Base$35',
        'PORT': '3306',
        'HOST': 'serverlegdig',
        
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'es-ar'

TIME_ZONE = 'America/Argentina/Buenos_Aires'
USE_TZ = False
USE_I18N = True
USE_L10N = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
#STATIC_ROOT = BASE_DIR / 'static'
STATICFILES_DIRS = [
    BASE_DIR / "static",
    #"static/",
]
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = 'login'
#pip install django-session-timeout
SESSION_EXPIRE_SECONDS = 3600  # 1 hora
SESSION_TIMEOUT_REDIRECT = '/'
SESSION_EXPIRE_AFTER_LAST_ACTIVITY = True
SESSION_EXPIRE_AFTER_LAST_ACTIVITY_GRACE_PERIOD = 900 # en segundos
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 45 * 60

#cantidad de fallos en el loguin
AXES_FAILURE_LIMIT: 3

#tiempo en horas para volver a intentar 
AXES_COOLOFF_TIME: 1

#si el usuario se loguea bien entonces debo resetar los axes
AXES_RESET_ON_SUCCESS = True

#configurar que se bloquea
AXES_LOCKOUT_PARAMETERS=[
   # ["ip_address", "user_agent", "username"]
   ["username"]
]
#funcion que llama cuando el usuario esta bloqueado
AXES_LOCKOUT_CALLABLE = "inventario.views.lockout"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
MEDIA_URL='media/'
MEDIA_ROOT=BASE_DIR / 'media'


#configuro quien puede usar nuestro sitio, puerto 3000 es de react el 8000 es django
CORS_ORIGIN_WHITELIST =env.list('CORS_ORIGIN_WHITELIST_DEV')

CSRF_TRUSTED_ORIGINS =env.list('CSRF_TRUSTED_ORIGINS_DEV')

if not DEBUG:
    
    ALLOWED_HOSTS=env.list('ALLOWED_HOSTS_DEPLOY')
    CORS_ORIGIN_WHITELIST =env.list('CORS_ORIGIN_WHITELIST_DEPLOY')
    CSRF_TRUSTED_ORIGINS =env.list('CSRF_TRUSTED_ORIGINS_DEPLOY')
    
    #tambien config para base de datos
    DATABASES={
        'default':env.db("DATABASE_URL"),
    }
    DATABASES["default"]["ATOMIC_REQUESTS"]=True #Evita llamados duplicados