"""
Pruebas automatizadas del modulo de ingresos.
"""

from django.test import TestCase
from .models import Ingreso
from usuarios.models import Usuario


class IngresoModelTest(TestCase):
    """Pruebas del modelo Ingreso."""

    def setUp(self):
        self.usuario = Usuario.objects.create_user(
            email='usuario_ingreso@test.com',
            username='usuario_ingreso',
            password='testpass123',
            first_name='Usuario',
            last_name='Ingreso',
            dni='12121212',
            fecha_nacimiento='1990-01-01',
            rol=Usuario.ROL_ALUMNO
        )

    def test_creacion_ingreso(self):
        """Verifica que se puede registrar un ingreso."""
        ingreso = Ingreso.objects.create(
            usuario=self.usuario,
            observacion='Ingreso normal'
        )
        self.assertEqual(ingreso.usuario, self.usuario)
        self.assertEqual(ingreso.observacion, 'Ingreso normal')

    def test_str(self):
        """Verifica la representacion en string."""
        ingreso = Ingreso.objects.create(usuario=self.usuario)
        self.assertIn('Usuario Ingreso', str(ingreso))
