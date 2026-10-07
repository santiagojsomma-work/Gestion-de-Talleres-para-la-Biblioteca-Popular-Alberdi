"""
Modelos del modulo de usuarios.
Incluye el modelo de Usuario personalizado y el modelo de Tutor.
"""

from datetime import date

from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class Usuario(AbstractUser):
    """
    Modelo de usuario personalizado que extiende el modelo base de Django.
    Agrega campos adicionales: DNI, telefono, fecha de nacimiento, rol, etc.

    Usa email como identificador principal en lugar de username.
    """

    # Roles disponibles
    ROL_ALUMNO = 'alumno'
    ROL_DOCENTE = 'docente'
    ROL_ADMIN = 'admin'

    ROLES = [
        (ROL_ALUMNO, 'Alumno'),
        (ROL_DOCENTE, 'Docente'),
        (ROL_ADMIN, 'Administrador'),
    ]

    # El email es el identificador principal, por lo tanto debe ser unico.
    email = models.EmailField(
        verbose_name='Email',
        unique=True,
        error_messages={
            'unique': 'Ya existe un usuario con este email.',
        },
    )

    # Si el login es por email, username puede quedar opcional.
    username = models.CharField(
        verbose_name='Nombre de usuario',
        max_length=150,
        blank=True,
        null=True,
    )

    # Campos adicionales
    dni = models.CharField(
        max_length=20,
        unique=True,
        validators=[
            RegexValidator(
                r'^\d+$',
                'El DNI debe contener solo numeros.'
            )
        ],
        verbose_name='DNI'
    )

    telefono = models.CharField(
        max_length=30,
        blank=True,
        verbose_name='Telefono'
    )

    fecha_nacimiento = models.DateField(
        verbose_name='Fecha de nacimiento'
    )

    rol = models.CharField(
        max_length=20,
        choices=ROLES,
        default=ROL_ALUMNO,
        verbose_name='Rol'
    )

    aprobado = models.BooleanField(
        default=False,
        verbose_name='Aprobado'
    )

    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de creacion'
    )

    # El email es el campo de autenticacion principal.
    USERNAME_FIELD = 'email'

    # Campos requeridos al crear un superusuario desde consola.
    # Se quita username porque el login es por email.
    REQUIRED_FIELDS = ['dni', 'fecha_nacimiento']

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.email})'

    @property
    def es_menor_de_edad(self):
        """Verifica si el usuario es menor de edad segun su fecha de nacimiento."""
        hoy = date.today()
        edad = hoy.year - self.fecha_nacimiento.year - (
            (hoy.month, hoy.day) < (
                self.fecha_nacimiento.month,
                self.fecha_nacimiento.day
            )
        )
        return edad < 18

    @property
    def es_docente(self):
        """Verifica si el usuario es docente."""
        return self.rol == self.ROL_DOCENTE

    @property
    def es_alumno(self):
        """Verifica si el usuario es alumno."""
        return self.rol == self.ROL_ALUMNO

    @property
    def es_admin(self):
        """Verifica si el usuario es administrador."""
        return self.rol == self.ROL_ADMIN


class Tutor(models.Model):
    """
    Modelo que almacena los datos del padre, madre o tutor
    de un alumno menor de edad.
    """

    # Tipos de parentesco
    PADRE = 'padre'
    MADRE = 'madre'
    TUTOR = 'tutor'

    PARENTESCOS = [
        (PADRE, 'Padre'),
        (MADRE, 'Madre'),
        (TUTOR, 'Tutor'),
    ]

    usuario_alumno = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        related_name='tutor',
        verbose_name='Alumno'
    )

    nombre = models.CharField(
        max_length=100,
        verbose_name='Nombre'
    )

    apellido = models.CharField(
        max_length=100,
        verbose_name='Apellido'
    )

    dni = models.CharField(
        max_length=20,
        verbose_name='DNI'
    )

    telefono = models.CharField(
        max_length=30,
        verbose_name='Telefono'
    )

    email = models.EmailField(
        blank=True,
        verbose_name='Email'
    )

    parentesco = models.CharField(
        max_length=20,
        choices=PARENTESCOS,
        verbose_name='Parentesco'
    )

    class Meta:
        verbose_name = 'Tutor'
        verbose_name_plural = 'Tutores'

    def __str__(self):
        return f'{self.nombre} {self.apellido} ({self.get_parentesco_display()})'