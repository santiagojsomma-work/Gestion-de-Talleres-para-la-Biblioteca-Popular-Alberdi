"""
Pruebas automatizadas del modulo de inscripciones.
"""

from django.test import TestCase, Client
from django.urls import reverse
from .models import Inscripcion
from usuarios.models import Usuario
from talleres.models import Taller


class InscripcionModelTest(TestCase):
    """Pruebas del modelo Inscripcion."""

    def setUp(self):
        self.alumno = Usuario.objects.create_user(
            email='alumno@test.com',
            username='alumno',
            password='testpass123',
            first_name='Alumno',
            last_name='Test',
            dni='33333333',
            fecha_nacimiento='1990-01-01',
            rol=Usuario.ROL_ALUMNO
        )
        self.docente = Usuario.objects.create_user(
            email='docente3@test.com',
            username='docente3',
            password='testpass123',
            first_name='Docente',
            last_name='Tres',
            dni='44444444',
            fecha_nacimiento='1985-01-01',
            rol=Usuario.ROL_DOCENTE,
            aprobado=True
        )
        self.taller = Taller.objects.create(
            nombre='Taller de Inscripcion',
            docente=self.docente,
            cupo=10,
            cuota_mensual=15000.00
        )

    def test_creacion_inscripcion(self):
        """Verifica que se puede crear una inscripcion."""
        inscripcion = Inscripcion.objects.create(
            alumno=self.alumno,
            taller=self.taller
        )
        self.assertTrue(inscripcion.activa)
        self.assertFalse(inscripcion.en_lista_espera)

    def test_tiene_cupo(self):
        """Verifica que el taller tiene cupo disponible."""
        self.assertTrue(self.taller.tiene_cupo)
        self.assertEqual(self.taller.cupo_disponible, 10)

    def test_cupo_lleno_lista_espera(self):
        """Verifica que si el taller esta lleno, se anota en lista de espera."""
        # Llenar el taller
        for i in range(10):
            alumno = Usuario.objects.create_user(
                email=f'alumno{i}@test.com',
                username=f'alumno{i}',
                password='testpass123',
                first_name=f'Alumno{i}',
                last_name='Test',
                dni=f'5555555{i}',
                fecha_nacimiento='1990-01-01',
                rol=Usuario.ROL_ALUMNO
            )
            Inscripcion.objects.create(alumno=alumno, taller=self.taller)

        # El taller esta lleno
        self.assertFalse(self.taller.tiene_cupo)

        # Nuevo alumno se anota en lista de espera
        nuevo_alumno = Usuario.objects.create_user(
            email='nuevo@test.com',
            username='nuevo',
            password='testpass123',
            first_name='Nuevo',
            last_name='Alumno',
            dni='66666666',
            fecha_nacimiento='1990-01-01',
            rol=Usuario.ROL_ALUMNO
        )
        inscripcion = Inscripcion.objects.create(alumno=nuevo_alumno, taller=self.taller)
        self.assertTrue(inscripcion.en_lista_espera)
