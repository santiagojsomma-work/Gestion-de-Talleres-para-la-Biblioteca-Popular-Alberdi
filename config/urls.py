"""
URL configuration for config project.
"""

from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='base.html'), name='home'),
    path('usuarios/', include('usuarios.urls')),
    path('talleres/', include('talleres.urls')),
    path('inscripciones/', include('inscripciones.urls')),
    path('pagos/', include('pagos.urls')),
    path('asistencia/', include('asistencia.urls')),
    path('ingresos/', include('ingresos.urls')),
    path('notificaciones/', include('notificaciones.urls')),

    # Recuperacion de contraseña
    path('password-reset/', TemplateView.as_view(template_name='registration/password_reset_form.html'), name='password_reset'),
    path('password-reset/done/', TemplateView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', TemplateView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', TemplateView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
]
