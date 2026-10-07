"""
Configuracion base del proyecto Django.
Contiene las configuraciones comunes a todos los entornos.
"""

from pathlib import Path

from decouple import AutoConfig

# Ruta base del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Configurar python-decouple para buscar .env en la raiz del proyecto
config = AutoConfig(search_path=str(BASE_DIR))

# Configuracion de seguridad
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost').split(',')

# Aplicaciones instaladas
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Apps del proyecto
    'usuarios',

    # Si todavia no creaste estas apps, dejalas comentadas.
    # Cuando las crees, descomentalas.
    # 'talleres',
    # 'inscripciones',
    # 'pagos',
    # 'asistencia',
    # 'ingresos',
    # 'notificaciones',
]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Configuracion de URLs
ROOT_URLCONF = 'config.urls'

# Configuracion de plantillas
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

# Configuracion WSGI
WSGI_APPLICATION = 'config.wsgi.application'

# Configuracion de base de datos
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Validadores de contraseña
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

# Configuracion internacional
LANGUAGE_CODE = config('LANGUAGE_CODE', default='es-ar')
TIME_ZONE = config('TIME_ZONE', default='America/Argentina/Buenos_Aires')
USE_I18N = True
USE_TZ = True

# Archivos estaticos
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Archivos media
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Campo primario por defecto
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configuracion de email
EMAIL_BACKEND = config(
    'EMAIL_BACKEND',
    default='django.core.mail.backends.console.EmailBackend'
)
EMAIL_HOST = config('EMAIL_HOST', default='localhost')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = config(
    'DEFAULT_FROM_EMAIL',
    default='biblioteca@ejemplo.com'
)

# Configuracion de login
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'

# Modelo de usuario personalizado
AUTH_USER_MODEL = 'usuarios.Usuario'