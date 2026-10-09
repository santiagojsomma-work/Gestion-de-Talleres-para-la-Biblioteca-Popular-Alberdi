"""
Modelos del modulo de notificaciones.
Incluye los modelos de Notificacion y Novedad.
"""

from django.db import models
from usuarios.models import Usuario


class Notificacion(models.Model):
    """
    Modelo que representa una notificacion dentro del sistema.
    """

    # Tipos de notificacion
    SUSPENSION = 'suspension'
    PAGO = 'pago'
    NOVEDAD = 'novedad'
    LISTA_ESPERA = 'lista_espera'
    TIPOS = [
        (SUSPENSION, 'Suspension de clase'),
        (PAGO, 'Pago registrado'),
        (NOVEDAD, 'Novedad'),
        (LISTA_ESPERA, 'Lista de espera'),
    ]

    usuario_destinatario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='notificaciones',
        verbose_name='Destinatario'
    )
    titulo = models.CharField(max_length=200, verbose_name='Titulo')
    mensaje = models.TextField(verbose_name='Mensaje')
    tipo = models.CharField(max_length=20, choices=TIPOS, verbose_name='Tipo')
    leida = models.BooleanField(default=False, verbose_name='Leida')
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creacion')

    class Meta:
        verbose_name = 'Notificacion'
        verbose_name_plural = 'Notificaciones'
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f'{self.titulo} - {self.usuario_destinatario}'

    def marcar_como_leida(self):
        """Marca la notificacion como leida."""
        self.leida = True
        self.save()


class Novedad(models.Model):
    """
    Modelo que representa una novedad o evento de la biblioteca.
    """

    # Tipos de novedad
    NOVEDAD = 'novedad'
    EVENTO = 'evento'
    SUSPENSION = 'suspension'
    TIPOS = [
        (NOVEDAD, 'Novedad'),
        (EVENTO, 'Evento'),
        (SUSPENSION, 'Suspension'),
    ]

    titulo = models.CharField(max_length=200, verbose_name='Titulo')
    contenido = models.TextField(verbose_name='Contenido')
    tipo = models.CharField(max_length=20, choices=TIPOS, default=NOVEDAD, verbose_name='Tipo')
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creacion')

    class Meta:
        verbose_name = 'Novedad'
        verbose_name_plural = 'Novedades'
        ordering = ['-fecha_creacion']

    def __str__(self):
        return self.titulo
