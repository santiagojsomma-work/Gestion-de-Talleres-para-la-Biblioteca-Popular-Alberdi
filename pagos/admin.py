"""
Configuracion del admin de Django para el modulo de pagos.
"""

from django.contrib import admin
from .models import Cuota, Pago


@admin.register(Cuota)
class CuotaAdmin(admin.ModelAdmin):
    list_display = ['inscripcion', 'mes_anio', 'monto', 'fecha_vencimiento', 'estado']
    list_filter = ['estado', 'mes_anio']
    search_fields = ['inscripcion__alumno__first_name', 'inscripcion__alumno__last_name']


@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ['cuota', 'monto', 'fecha_pago', 'metodo', 'anulado']
    list_filter = ['metodo', 'anulado', 'fecha_pago']
    search_fields = ['cuota__inscripcion__alumno__first_name', 'cuota__inscripcion__alumno__last_name']
