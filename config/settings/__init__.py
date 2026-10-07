"""
Configuración de Django para el proyecto.

Por defecto usa desarrollo.py.

Para producción, definir la variable de entorno:

    DJANGO_SETTINGS_MODULE=config.settings.produccion
"""

from .desarrollo import *