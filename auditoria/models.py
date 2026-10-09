"""
Modelos del modulo de auditoria.
"""

from django.db import models
from usuarios.models import Usuario


class Auditoria(models.Model):
    """
    Modelo que registra las acciones criticas del sistema.
    """

    # Tipos de accion
    CREAR_TALLER = 'crear_taller'
    EDITAR_TALLER = 'editar_taller'
    BAJA_TALLER = 'baja_taller'
    APROBAR_DOCENTE = 'aprobar_docente'
    RECHAZAR_DOCENTE = 'rechazar_docente'
    REGISTRAR_PAGO = 'registrar_pago'
    ANULAR_PAGO = 'anular_pago'
    SUSPENDER_CLASE = 'suspender_clase'
    CREAR_NOVEDAD = 'crear_novedad'

    ACCIONES = [
        (CREAR_TALLER, 'Crear taller'),
        (EDITAR_TALLER, 'Editar taller'),
        (BAJA_TALLER, 'Baja taller'),
        (APROBAR_DOCENTE, 'Aprobar docente'),
        (RECHAZAR_DOCENTE, 'Rechazar docente'),
        (REGISTRAR_PAGO, 'Registrar pago'),
        (ANULAR_PAGO, 'Anular pago'),
        (SUSPENDER_CLASE, 'Suspender clase'),
        (CREAR_NOVEDAD, 'Crear novedad'),
    ]

    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        related_name='auditorias',
        verbose_name='Usuario'
    )
    accion = models.CharField(max_length=30, choices=ACCIONES, verbose_name='Accion')
    descripcion = models.TextField(verbose_name='Descripcion')
    fecha_hora = models.DateTimeField(auto_now_add=True, verbose_name='Fecha y hora')
    ip = models.GenericIPAddressField(null=True, blank=True, verbose_name='IP')

    class Meta:
        verbose_name = 'Auditoria'
        verbose_name_plural = 'Auditorias'
        ordering = ['-fecha_hora']

    def __str__(self):
        return f'{self.get_accion_display()} - {self.usuario} - {self.fecha_hora}'
