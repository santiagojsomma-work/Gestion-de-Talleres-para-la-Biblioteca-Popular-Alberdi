"""
URLs del modulo de pagos.
"""

from django.urls import path
from . import views

urlpatterns = [
    path('cuotas-pendientes/', views.cuotas_pendientes, name='cuotas_pendientes'),
    path('registrar-pago/<int:cuota_pk>/', views.registrar_pago_view, name='registrar_pago'),
    path('anular-pago/<int:pago_pk>/', views.anular_pago, name='anular_pago'),
    path('mis-pagos/', views.mis_pagos, name='mis_pagos'),
]
