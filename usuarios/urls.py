"""
URLs del modulo de usuarios.
"""

from django.urls import path
from . import views

urlpatterns = [
    # Registro
    path('registro/alumno/', views.registro_alumno, name='registro_alumno'),
    path('registro/docente/', views.registro_docente, name='registro_docente'),

    # Autenticacion
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Perfil
    path('perfil/', views.perfil, name='perfil'),

    # Administracion de docentes
    path('docentes/pendientes/', views.lista_docentes_pendientes, name='lista_docentes_pendientes'),
    path('docentes/aprobar/<int:pk>/', views.aprobar_docente, name='aprobar_docente'),
    path('docentes/rechazar/<int:pk>/', views.rechazar_docente, name='rechazar_docente'),
]
