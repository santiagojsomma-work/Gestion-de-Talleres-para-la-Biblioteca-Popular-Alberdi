"""
URLs del modulo de asistencia.
"""

from django.urls import path
from . import views

urlpatterns = [
    path('clases/<int:taller_pk>/', views.lista_clases, name='lista_clases'),
    path('clases/<int:taller_pk>/crear/', views.crear_clase, name='crear_clase'),
    path('tomar-asistencia/<int:clase_pk>/', views.tomar_asistencia, name='tomar_asistencia'),
    path('mi-asistencia/', views.mi_asistencia, name='mi_asistencia'),
]
