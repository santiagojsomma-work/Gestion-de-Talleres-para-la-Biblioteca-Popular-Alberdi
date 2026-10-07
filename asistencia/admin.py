"""
Configuracion del admin de Django para el modulo de asistencia.
"""

from django.contrib import admin
from .models import Clase, Asistencia


@admin.register(Clase)
class ClaseAdmin(admin.ModelAdmin):
    list_display = ['taller', 'fecha', 'tema', 'suspendida']
    list_filter = ['suspendida', 'fecha']
    search_fields = ['taller__nombre', 'tema']


@admin.register(Asistencia)
class AsistenciaAdmin(admin.ModelAdmin):
    list_display = ['clase', 'inscripcion', 'estado']
    list_filter = ['estado', 'clase__fecha']
    search_fields = ['inscripcion__alumno__first_name', 'inscripcion__alumno__last_name']
