"""
Configuracion para el entorno de desarrollo.
Hereda de base.py y ajusta valores para desarrollo local.
"""

from .base import *

# En desarrollo, DEBUG siempre es True
DEBUG = True

# Permitir todos los hosts en desarrollo
ALLOWED_HOSTS = ['*']

# Base de datos SQLite en desarrollo
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Email por consola en desarrollo (no se envian emails reales)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Mostrar errores detallados
INTERNAL_IPS = ['127.0.0.1']
