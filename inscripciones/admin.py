"""
Configuracion del admin de Django para el modulo de inscripciones.
"""

from django.contrib import admin
from .models import Inscripcion


@admin.register(Inscripcion)
class InscripcionAdmin(admin.ModelAdmin):
    list_display = ['alumno', 'taller', 'fecha_inscripcion', 'activa', 'en_lista_espera']
    list_filter = ['activa', 'en_lista_espera', 'fecha_inscripcion']
    search_fields = ['alumno__first_name', 'alumno__last_name', 'taller__nombre']
