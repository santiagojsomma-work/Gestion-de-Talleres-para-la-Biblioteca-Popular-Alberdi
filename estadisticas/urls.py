"""
URLs del modulo de estadisticas.
"""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.panel_estadisticas, name='panel_estadisticas'),
    path('exportar-csv/', views.exportar_estadisticas_csv, name='exportar_estadisticas_csv'),
]
