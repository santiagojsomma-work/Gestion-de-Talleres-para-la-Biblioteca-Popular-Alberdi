"""
Configuracion de Django para el proyecto.
Selecciona el entorno segun la variable de entorno DJANGO_SETTINGS_MODULE.
Por defecto usa desarrollo.py.
"""

import os

# Seleccionar el modulo de settings segun la variable de entorno
# Si no esta definida, usa desarrollo por defecto
SETTINGS_MODULE = os.environ.get('DJANGO_SETTINGS_MODULE', 'config.settings.desarrollo')

# Importar el modulo de settings correspondiente
if SETTINGS_MODULE == 'config.settings.produccion':
    from .produccion import *
else:
    from .desarrollo import *
