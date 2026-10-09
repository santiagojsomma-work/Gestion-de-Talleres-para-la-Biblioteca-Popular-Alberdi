"""
Configuracion del admin de Django para el modulo de ingresos.
"""

from django.contrib import admin
from .models import Ingreso


@admin.register(Ingreso)
class IngresoAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'fecha_hora', 'observacion']
    list_filter = ['fecha_hora']
    search_fields = ['usuario__first_name', 'usuario__last_name', 'usuario__dni']
