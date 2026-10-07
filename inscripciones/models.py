"""
Modelos del modulo de inscripciones.
"""

from django.db import models
from django.core.exceptions import ValidationError
from usuarios.models import Usuario
from talleres.models import Taller


class Inscripcion(models.Model):
    """
    Modelo que representa la inscripcion de un alumno a un taller.
    Incluye soporte para lista de espera.
    """

    alumno = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='inscripciones',
        verbose_name='Alumno',
        limit_choices_to={'rol': Usuario.ROL_ALUMNO}
    )
    taller = models.ForeignKey(
        Taller,
        on_delete=models.CASCADE,
        related_name='inscripciones',
        verbose_name='Taller'
    )
    fecha_inscripcion = models.DateField(auto_now_add=True, verbose_name='Fecha de inscripcion')
    activa = models.BooleanField(default=True, verbose_name='Activa')
    en_lista_espera = models.BooleanField(default=False, verbose_name='En lista de espera')
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creacion')

    class Meta:
        verbose_name = 'Inscripcion'
        verbose_name_plural = 'Inscripciones'
        unique_together = ['alumno', 'taller']
        ordering = ['-fecha_creacion']

    def __str__(self):
        estado = 'Lista de espera' if self.en_lista_espera else 'Inscripto'
        return f'{self.alumno} - {self.taller} ({estado})'

    def clean(self):
        """Valida que el alumno no este ya inscripto en el taller."""
        if not self.pk:  # Solo al crear
            if Inscripcion.objects.filter(alumno=self.alumno, taller=self.taller, activa=True).exists():
                raise ValidationError('El alumno ya esta inscripto en este taller.')

    def save(self, *args, **kwargs):
        """Al guardar, verifica si hay cupo disponible."""
        if not self.pk and not self.en_lista_espera:  # Solo al crear
            if not self.taller.tiene_cupo:
                self.en_lista_espera = True
        super().save(*args, **kwargs)

    def confirmar_inscripcion(self):
        """
        Confirma la inscripcion de un alumno que estaba en lista de espera.
        Se llama cuando se libera un cupo.
        """
        self.en_lista_espera = False
        self.activa = True
        self.save()

    @classmethod
    def notificar_lista_espera(cls, taller):
        """
        Notifica al primer alumno en lista de espera que se libero un cupo.
        """
        primera_inscripcion = cls.objects.filter(
            taller=taller,
            activa=True,
            en_lista_espera=True
        ).order_by('fecha_creacion').first()

        if primera_inscripcion:
            primera_inscripcion.confirmar_inscripcion()
            return primera_inscripcion
        return None
