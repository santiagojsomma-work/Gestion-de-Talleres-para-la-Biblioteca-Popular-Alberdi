"""
Configuracion del admin de Django para el modulo de notificaciones.
"""

from django.contrib import admin
from .models import Notificacion, Novedad


@admin.register(Notificacion)
class NotificacionAdmin(admin.ModelAdmin):
    list_display = ['usuario_destinatario', 'titulo', 'tipo', 'leida', 'fecha_creacion']
    list_filter = ['tipo', 'leida', 'fecha_creacion']
    search_fields = ['titulo', 'mensaje', 'usuario_destinatario__email']


@admin.register(Novedad)
class NovedadAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'tipo', 'fecha_creacion']
    list_filter = ['tipo', 'fecha_creacion']
    search_fields = ['titulo', 'contenido']
