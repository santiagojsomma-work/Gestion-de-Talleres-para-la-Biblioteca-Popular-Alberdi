"""
URLs del modulo de talleres.
"""

from django.urls import path
from . import views

urlpatterns = [
    # CRUD para el administrador
    path('', views.lista_talleres, name='lista_talleres'),
    path('crear/', views.crear_taller, name='crear_taller'),
    path('editar/<int:pk>/', views.editar_taller, name='editar_taller'),
    path('baja/<int:pk>/', views.dar_baja_taller, name='dar_baja_taller'),
    path('alta/<int:pk>/', views.dar_alta_taller, name='dar_alta_taller'),

    # Grilla semanal publica
    path('grilla/', views.grilla_semanal, name='grilla_semanal'),
]
