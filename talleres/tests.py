"""
Pruebas automatizadas del modulo de talleres.
"""

from datetime import time
from django.test import TestCase, Client
from django.urls import reverse
from .models import Taller, Horario
from usuarios.models import Usuario


class TallerModelTest(TestCase):
    """Pruebas del modelo Taller."""

    def setUp(self):
        self.docente = Usuario.objects.create_user(
            email='docente@test.com',
            username='docente',
            password='testpass123',
            first_name='Docente',
            last_name='Test',
            dni='11111111',
            fecha_nacimiento='1985-01-01',
            rol=Usuario.ROL_DOCENTE,
            aprobado=True
        )
        self.taller = Taller.objects.create(
            nombre='Taller de Prueba',
            descripcion='Descripcion del taller',
            docente=self.docente,
            cupo=10,
            cuota_mensual=15000.00
        )

    def test_creacion_taller(self):
        """Verifica que se puede crear un taller."""
        self.assertEqual(self.taller.nombre, 'Taller de Prueba')
        self.assertTrue(self.taller.activo)

    def test_str(self):
        """Verifica la representacion en string."""
        self.assertEqual(str(self.taller), 'Taller de Prueba')


class HorarioModelTest(TestCase):
    """Pruebas del modelo Horario."""

    def setUp(self):
        self.docente = Usuario.objects.create_user(
            email='docente2@test.com',
            username='docente2',
            password='testpass123',
            first_name='Docente',
            last_name='Dos',
            dni='22222222',
            fecha_nacimiento='1985-01-01',
            rol=Usuario.ROL_DOCENTE,
            aprobado=True
        )
        self.taller = Taller.objects.create(
            nombre='Taller de Prueba 2',
            docente=self.docente,
            cupo=10,
            cuota_mensual=15000.00
        )
        self.horario = Horario.objects.create(
            taller=self.taller,
            dia_semana=Horario.LUNES,
            hora_inicio=time(18, 0),
            hora_fin=time(20, 0)
        )

    def test_creacion_horario(self):
        """Verifica que se puede crear un horario."""
        self.assertEqual(self.horario.dia_semana, Horario.LUNES)
        self.assertEqual(str(self.horario.hora_inicio), '18:00:00')

    def test_str(self):
        """Verifica la representacion en string."""
        self.assertIn('Taller de Prueba 2', str(self.horario))
        self.assertIn('Lunes', str(self.horario))
