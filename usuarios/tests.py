"""
Pruebas del modulo de usuarios.
"""

from django.test import TestCase
from django.urls import reverse
from .models import Usuario, Tutor


class UsuarioModelTest(TestCase):
    """
    Pruebas del modelo de Usuario.
    """

    def setUp(self):
        """Crear datos de prueba."""
        self.usuario = Usuario.objects.create_user(
            email='test@ejemplo.com',
            username='testuser',
            password='testpass123',
            first_name='Test',
            last_name='User',
            dni='12345678',
            fecha_nacimiento='1990-01-01',
            rol=Usuario.ROL_ALUMNO
        )

    def test_creacion_usuario(self):
        """Verifica que se puede crear un usuario."""
        self.assertEqual(self.usuario.email, 'test@ejemplo.com')
        self.assertEqual(self.usuario.rol, Usuario.ROL_ALUMNO)
        self.assertTrue(self.usuario.aprobado)

    def test_es_menor_de_edad(self):
        """Verifica la deteccion de menores de edad."""
        from datetime import date
        # Usuario mayor de edad
        self.assertFalse(self.usuario.es_menor_de_edad)

        # Usuario menor de edad
        menor = Usuario.objects.create_user(
            email='menor@ejemplo.com',
            username='menor',
            password='testpass123',
            first_name='Menor',
            last_name='User',
            dni='87654321',
            fecha_nacimiento='2015-01-01',
            rol=Usuario.ROL_ALUMNO
        )
        self.assertTrue(menor.es_menor_de_edad)

    def test_str(self):
        """Verifica la representacion en string del usuario."""
        self.assertEqual(str(self.usuario), 'Test User (test@ejemplo.com)')


class TutorModelTest(TestCase):
    """
    Pruebas del modelo de Tutor.
    """

    def setUp(self):
        """Crear datos de prueba."""
        self.menor = Usuario.objects.create_user(
            email='menor@ejemplo.com',
            username='menor',
            password='testpass123',
            first_name='Menor',
            last_name='User',
            dni='87654321',
            fecha_nacimiento='2015-01-01',
            rol=Usuario.ROL_ALUMNO
        )
        self.tutor = Tutor.objects.create(
            usuario_alumno=self.menor,
            nombre='Padre',
            apellido='Tutor',
            dni='11111111',
            telefono='11-1111-1111',
            parentesco=Tutor.PADRE
        )

    def test_creacion_tutor(self):
        """Verifica que se puede crear un tutor."""
        self.assertEqual(self.tutor.nombre, 'Padre')
        self.assertEqual(self.tutor.parentesco, Tutor.PADRE)

    def test_str(self):
        """Verifica la representacion en string del tutor."""
        self.assertEqual(str(self.tutor), 'Padre Tutor (Padre)')


class RegistroAlumnoViewTest(TestCase):
    """
    Pruebas de la vista de registro de alumnos.
    """

    def test_registro_alumno(self):
        """Verifica que se puede registrar un alumno."""
        response = self.client.post(reverse('registro_alumno'), {
            'email': 'nuevo@ejemplo.com',
            'first_name': 'Nuevo',
            'last_name': 'Alumno',
            'dni': '99999999',
            'telefono': '11-9999-9999',
            'fecha_nacimiento': '1990-01-01',
            'password1': 'testpass123',
            'password2': 'testpass123',
        })
        self.assertEqual(response.status_code, 302)  # Redireccion al home
        self.assertTrue(Usuario.objects.filter(email='nuevo@ejemplo.com').exists())

    def test_registro_menor_con_tutor(self):
        """Verifica que un menor de edad puede registrarse con tutor."""
        response = self.client.post(reverse('registro_alumno'), {
            'email': 'menor2@ejemplo.com',
            'first_name': 'Menor',
            'last_name': 'Dos',
            'dni': '88888888',
            'telefono': '11-8888-8888',
            'fecha_nacimiento': '2015-01-01',
            'password1': 'testpass123',
            'password2': 'testpass123',
            'tutor_nombre': 'Padre',
            'tutor_apellido': 'Tutor',
            'tutor_dni': '77777777',
            'tutor_telefono': '11-7777-7777',
            'tutor_parentesco': 'padre',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Usuario.objects.filter(email='menor2@ejemplo.com').exists())
        self.assertTrue(Tutor.objects.filter(usuario_alumno__email='menor2@ejemplo.com').exists())
