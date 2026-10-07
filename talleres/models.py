"""
Modelos del modulo de talleres.
Incluye los modelos de Taller y Horario.
"""

from django.db import models
from django.core.validators import MinValueValidator
from usuarios.models import Usuario


class Taller(models.Model):
    """
    Modelo que representa un taller de la biblioteca.
    """

    nombre = models.CharField(max_length=150, verbose_name='Nombre')
    descripcion = models.TextField(blank=True, verbose_name='Descripcion')
    docente = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='talleres',
        verbose_name='Docente',
        limit_choices_to={'rol': Usuario.ROL_DOCENTE, 'aprobado': True}
    )
    cupo = models.PositiveIntegerField(
        default=10,
        validators=[MinValueValidator(1)],
        verbose_name='Cupo maximo'
    )
    cuota_mensual = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name='Cuota mensual (ARS)'
    )
    activo = models.BooleanField(default=True, verbose_name='Activo')
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creacion')

    class Meta:
        verbose_name = 'Taller'
        verbose_name_plural = 'Talleres'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

    @property
    def cantidad_inscriptos(self):
        """Devuelve la cantidad de alumnos activos inscriptos en el taller."""
        from inscripciones.models import Inscripcion
        return Inscripcion.objects.filter(taller=self, activa=True, en_lista_espera=False).count()

    @property
    def cupo_disponible(self):
        """Devuelve la cantidad de cupos disponibles."""
        return self.cupo - self.cantidad_inscriptos

    @property
    def tiene_cupo(self):
        """Verifica si hay cupo disponible."""
        return self.cupo_disponible > 0


class Horario(models.Model):
    """
    Modelo que representa un horario de clase de un taller.
    """

    # Dias de la semana
    LUNES = 0
    MARTES = 1
    MIERCOLES = 2
    JUEVES = 3
    VIERNES = 4
    SABADO = 5
    DOMINGO = 6

    DIAS_SEMANA = [
        (LUNES, 'Lunes'),
        (MARTES, 'Martes'),
        (MIERCOLES, 'Miercoles'),
        (JUEVES, 'Jueves'),
        (VIERNES, 'Viernes'),
        (SABADO, 'Sabado'),
        (DOMINGO, 'Domingo'),
    ]

    taller = models.ForeignKey(
        Taller,
        on_delete=models.CASCADE,
        related_name='horarios',
        verbose_name='Taller'
    )
    dia_semana = models.PositiveSmallIntegerField(
        choices=DIAS_SEMANA,
        verbose_name='Dia de la semana'
    )
    hora_inicio = models.TimeField(verbose_name='Hora de inicio')
    hora_fin = models.TimeField(verbose_name='Hora de fin')

    class Meta:
        verbose_name = 'Horario'
        verbose_name_plural = 'Horarios'
        ordering = ['dia_semana', 'hora_inicio']

    def __str__(self):
        return f'{self.taller.nombre} - {self.get_dia_semana_display()} {self.hora_inicio.strftime("%H:%M")} a {self.hora_fin.strftime("%H:%M")}'
