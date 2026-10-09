"""
URLs del modulo de notificaciones.
"""

from django.urls import path
from . import views

urlpatterns = [
    path('mis-notificaciones/', views.mis_notificaciones, name='mis_notificaciones'),
    path('marcar-leida/<int:notificacion_pk>/', views.marcar_notificacion_leida, name='marcar_notificacion_leida'),
    path('novedades/', views.novedades_publicas, name='novedades_publicas'),
    path('novedades/crear/', views.crear_novedad, name='crear_novedad'),
    path('novedades/lista/', views.lista_novedades, name='lista_novedades'),
]
