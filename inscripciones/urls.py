"""
URLs del modulo de inscripciones.
"""

from django.urls import path
from . import views

urlpatterns = [
    path('mis-inscripciones/', views.mis_inscripciones, name='mis_inscripciones'),
    path('inscribirse/<int:taller_pk>/', views.inscribirse, name='inscribirse'),
    path('baja/<int:inscripcion_pk>/', views.darse_de_baja, name='darse_de_baja'),
]
