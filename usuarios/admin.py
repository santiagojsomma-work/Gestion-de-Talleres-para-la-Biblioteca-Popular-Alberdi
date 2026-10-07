"""
Configuracion del admin de Django para el modulo de usuarios.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Tutor, Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    """
    Configuracion del admin para el modelo de Usuario personalizado.
    """

    model = Usuario

    list_display = [
        'email',
        'first_name',
        'last_name',
        'dni',
        'rol',
        'aprobado',
        'is_active',
    ]

    list_filter = [
        'rol',
        'aprobado',
        'is_active',
    ]

    search_fields = [
        'email',
        'first_name',
        'last_name',
        'dni',
    ]

    ordering = ['email']

    fieldsets = (
        (
            None,
            {
                'fields': ('email', 'password')
            }
        ),
        (
            'Informacion personal',
            {
                'fields': (
                    'first_name',
                    'last_name',
                    'dni',
                    'telefono',
                    'fecha_nacimiento',
                )
            }
        ),
        (
            'Roles y estado',
            {
                'fields': (
                    'rol',
                    'aprobado',
                    'is_active',
                )
            }
        ),
        (
            'Permisos',
            {
                'fields': (
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                )
            }
        ),
        (
            'Fechas importantes',
            {
                'fields': (
                    'last_login',
                    'date_joined',
                )
            }
        ),
    )

    readonly_fields = [
        'last_login',
        'date_joined',
    ]

    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'email',
                    'first_name',
                    'last_name',
                    'dni',
                    'fecha_nacimiento',
                    'password1',
                    'password2',
                ),
            }
        ),
    )

    filter_horizontal = [
        'groups',
        'user_permissions',
    ]


@admin.register(Tutor)
class TutorAdmin(admin.ModelAdmin):
    """
    Configuracion del admin para el modelo de Tutor.
    """

    list_display = [
        'nombre',
        'apellido',
        'dni',
        'parentesco',
        'usuario_alumno',
    ]

    list_filter = [
        'parentesco',
    ]

    search_fields = [
        'nombre',
        'apellido',
        'dni',
        'usuario_alumno__email',
    ]