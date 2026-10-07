"""
Decoradores para permisos por rol.
Permiten restringir el acceso a vistas segun el rol del usuario.
"""

from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def es_admin_required(view_func):
    """
    Decorador que verifica que el usuario sea administrador.
    Si no lo es, redirige al home con un mensaje de error.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Debe iniciar sesion para acceder a esta pagina.')
            return redirect('login')
        if not request.user.es_admin:
            messages.error(request, 'No tiene permisos para acceder a esta pagina.')
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def es_docente_required(view_func):
    """
    Decorador que verifica que el usuario sea docente aprobado.
    Si no lo es, redirige al home con un mensaje de error.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Debe iniciar sesion para acceder a esta pagina.')
            return redirect('login')
        if not request.user.es_docente or not request.user.aprobado:
            messages.error(request, 'No tiene permisos para acceder a esta pagina.')
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def es_alumno_required(view_func):
    """
    Decorador que verifica que el usuario sea alumno.
    Si no lo es, redirige al home con un mensaje de error.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Debe iniciar sesion para acceder a esta pagina.')
            return redirect('login')
        if not request.user.es_alumno:
            messages.error(request, 'No tiene permisos para acceder a esta pagina.')
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return _wrapped_view
