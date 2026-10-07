"""
Configuracion del admin de Django para el modulo de talleres.
"""

from django.contrib import admin
from .models import Taller, Horario


@admin.register(Taller)
class TallerAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'docente', 'cupo', 'cuota_mensual', 'activo']
    list_filter = ['activo']
    search_fields = ['nombre']


@admin.register(Horario)
class HorarioAdmin(admin.ModelAdmin):
    list_display = ['taller', 'dia_semana', 'hora_inicio', 'hora_fin']
    list_filter = ['dia_semana']
