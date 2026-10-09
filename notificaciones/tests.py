"""
Pruebas automatizadas del modulo de notificaciones.
"""

from django.test import TestCase
from .models import Notificacion, Novedad
from usuarios.models import Usuario


class NotificacionModelTest(TestCase):
    """Pruebas del modelo Notificacion."""

    def setUp(self):
        self.usuario = Usuario.objects.create_user(
            email='usuario_noti@test.com',
            username='usuario_noti',
            password='testpass123',
            first_name='Usuario',
            last_name='Notificacion',
            dni='13131313',
            fecha_nacimiento='1990-01-01',
            rol=Usuario.ROL_ALUMNO
        )

    def test_creacion_notificacion(self):
        """Verifica que se puede crear una notificacion."""
        notificacion = Notificacion.objects.create(
            usuario_destinatario=self.usuario,
            titulo='Notificacion de prueba',
            mensaje='Este es el mensaje de la notificacion',
            tipo=Notificacion.NOVEDAD
        )
        self.assertEqual(notificacion.titulo, 'Notificacion de prueba')
        self.assertFalse(notificacion.leida)

    def test_marcar_como_leida(self):
        """Verifica que se puede marcar una notificacion como leida."""
        notificacion = Notificacion.objects.create(
            usuario_destinatario=self.usuario,
            titulo='Notificacion de prueba',
            mensaje='Este es el mensaje de la notificacion',
            tipo=Notificacion.NOVEDAD
        )
        notificacion.marcar_como_leida()
        self.assertTrue(notificacion.leida)


class NovedadModelTest(TestCase):
    """Pruebas del modelo Novedad."""

    def test_creacion_novedad(self):
        """Verifica que se puede crear una novedad."""
        novedad = Novedad.objects.create(
            titulo='Novedad de prueba',
            contenido='Contenido de la novedad',
            tipo=Novedad.NOVEDAD
        )
        self.assertEqual(novedad.titulo, 'Novedad de prueba')
        self.assertEqual(novedad.tipo, Novedad.NOVEDAD)
