"""
Modelos del modulo de ingresos.
"""

from django.db import models
from usuarios.models import Usuario


class Ingreso(models.Model):
    """
    Modelo que representa el ingreso de una persona a la biblioteca.
    """

    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='ingresos',
        verbose_name='Usuario'
    )
    fecha_hora = models.DateTimeField(auto_now_add=True, verbose_name='Fecha y hora')
    observacion = models.TextField(blank=True, verbose_name='Observacion')

    class Meta:
        verbose_name = 'Ingreso'
        verbose_name_plural = 'Ingresos'
        ordering = ['-fecha_hora']

    def __str__(self):
        return f'{self.usuario} - {self.fecha_hora.strftime("%d/%m/%Y %H:%M")}'
