"""
Configuracion del admin de Django para el modulo de auditoria.
"""

from django.contrib import admin
from .models import Auditoria


@admin.register(Auditoria)
class AuditoriaAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'accion', 'descripcion', 'fecha_hora']
    list_filter = ['accion', 'fecha_hora']
    search_fields = ['usuario__email', 'descripcion']
    readonly_fields = ['usuario', 'accion', 'descripcion', 'fecha_hora', 'ip']
