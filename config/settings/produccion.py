"""
Configuracion para el entorno de produccion.
Hereda de base.py y ajusta valores para produccion.
IMPORTANTE: En produccion, DEBUG debe ser False y SECRET_KEY debe ser segura.
"""

from .base import *

# En produccion, DEBUG siempre es False
DEBUG = False

# Hosts permitidos en produccion (configurar con el dominio real)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost').split(',')

# Base de datos PostgreSQL en produccion
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME', default='biblioteca'),
        'USER': config('DB_USER', default='postgres'),
        'PASSWORD': config('DB_PASSWORD', default=''),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
    }
}

# Email SMTP en produccion
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# Configuracion de seguridad en produccion
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
