"""
Servicios del modulo de auditoria.
"""

from .models import Auditoria


def registrar_accion(usuario, accion, descripcion, ip=None):
    """
    Registra una accion critica en la auditoria.
    """
    Auditoria.objects.create(
        usuario=usuario,
        accion=accion,
        descripcion=descripcion,
        ip=ip
    )
