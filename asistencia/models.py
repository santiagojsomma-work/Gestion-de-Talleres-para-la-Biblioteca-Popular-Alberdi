"""
Modelos del modulo de asistencia.
Incluye los modelos de Clase y Asistencia.
"""

from django.db import models
from django.core.exceptions import ValidationError
from talleres.models import Taller
from inscripciones.models import Inscripcion


class Clase(models.Model):
    """
    Modelo que representa una clase dictada en una fecha especifica.
    """

    taller = models.ForeignKey(
        Taller,
        on_delete=models.CASCADE,
        related_name='clases',
        verbose_name='Taller'
    )
    fecha = models.DateField(verbose_name='Fecha')
    tema = models.CharField(max_length=200, blank=True, verbose_name='Tema')
    suspendida = models.BooleanField(default=False, verbose_name='Suspendida')
    motivo_suspension = models.TextField(blank=True, verbose_name='Motivo de suspension')

    class Meta:
        verbose_name = 'Clase'
        verbose_name_plural = 'Clases'
        unique_together = ['taller', 'fecha']
        ordering = ['-fecha']

    def __str__(self):
        estado = 'SUSPENDIDA' if self.suspendida else 'Dictada'
        return f'{self.taller.nombre} - {self.fecha} - {estado}'


class Asistencia(models.Model):
    """
    Modelo que representa la asistencia de un alumno a una clase.
    """

    # Estados de asistencia
    PRESENTE = 'presente'
    AUSENTE = 'ausente'
    JUSTIFICADO = 'justificado'
    ESTADOS = [
        (PRESENTE, 'Presente'),
        (AUSENTE, 'Ausente'),
        (JUSTIFICADO, 'Justificado'),
    ]

    clase = models.ForeignKey(
        Clase,
        on_delete=models.CASCADE,
        related_name='asistencias',
        verbose_name='Clase'
    )
    inscripcion = models.ForeignKey(
        Inscripcion,
        on_delete=models.CASCADE,
        related_name='asistencias',
        verbose_name='Inscripcion'
    )
    estado = models.CharField(max_length=20, choices=ESTADOS, default=PRESENTE, verbose_name='Estado')
    justificacion = models.TextField(blank=True, verbose_name='Justificacion')

    class Meta:
        verbose_name = 'Asistencia'
        verbose_name_plural = 'Asistencias'
        unique_together = ['clase', 'inscripcion']
        ordering = ['-clase__fecha']

    def __str__(self):
        return f'{self.inscripcion.alumno} - {self.clase} - {self.get_estado_display()}'

    def clean(self):
        """Valida que la inscripcion pertenezca al taller de la clase."""
        if self.inscripcion.taller != self.clase.taller:
            raise ValidationError('La inscripcion no pertenece al taller de esta clase.')

        # Validar que la clase no sea anterior a la inscripcion
        if self.clase.fecha < self.inscripcion.fecha_inscripcion:
            raise ValidationError('La clase es anterior a la fecha de inscripcion del alumno.')
