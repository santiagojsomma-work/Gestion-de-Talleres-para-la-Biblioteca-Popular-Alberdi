"""
URLs del modulo de ingresos.
"""

from django.urls import path
from . import views

urlpatterns = [
    path('registrar/', views.registrar_ingreso, name='registrar_ingreso'),
    path('historial/', views.historial_ingresos, name='historial_ingresos'),
    path('detalle/<int:ingreso_pk>/', views.detalle_ingreso, name='detalle_ingreso'),
]
