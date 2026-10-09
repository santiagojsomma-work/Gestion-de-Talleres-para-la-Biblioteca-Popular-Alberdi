"""
Pruebas automatizadas del modulo de usuarios.
"""

from datetime import date
from django.test import TestCase, Client
from django.urls import reverse
from .models import Usuario, Tutor


class UsuarioModelTest(TestCase):
    """Pruebas del modelo Usuario."""

    def setUp(self):
        self.usuario = Usuario.objects.create_user(
            email='test@ejemplo.com',
            username='testuser',
            password='testpass123',
            first_name='Test',
            last_name='User',
            dni='12345678',
            fecha_nacimiento=date(1990, 1, 1),
            rol=Usuario.ROL_ALUMNO,
            aprobado=True
        )

    def test_creacion_usuario(self):
        """Verifica que se puede crear un usuario."""
        self.assertEqual(self.usuario.email, 'test@ejemplo.com')
        self.assertEqual(self.usuario.rol, Usuario.ROL_ALUMNO)
        self.assertTrue(self.usuario.aprobado)

    def test_es_menor_de_edad(self):
        """Verifica la deteccion de menores de edad."""
        self.assertFalse(self.usuario.es_menor_de_edad)

        menor = Usuario.objects.create_user(
            email='menor@ejemplo.com',
            username='menor',
            password='testpass123',
            first_name='Menor',
            last_name='User',
            dni='87654321',
            fecha_nacimiento=date(2015, 1, 1),
            rol=Usuario.ROL_ALUMNO
        )
        self.assertTrue(menor.es_menor_de_edad)

    def test_str(self):
        """Verifica la representacion en string."""
        self.assertEqual(str(self.usuario), 'Test User (test@ejemplo.com)')


class RegistroAlumnoViewTest(TestCase):
    """Pruebas de la vista de registro de alumnos."""

    def setUp(self):
        self.client = Client()

    def test_registro_alumno_mayor(self):
        """Verifica que un alumno mayor de edad puede registrarse."""
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
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Usuario.objects.filter(email='nuevo@ejemplo.com').exists())

    def test_registro_alumno_menor_con_tutor(self):
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

    def test_registro_alumno_menor_sin_tutor_falla(self):
        """Verifica que un menor de edad no puede registrarse sin tutor."""
        response = self.client.post(reverse('registro_alumno'), {
            'email': 'menor3@ejemplo.com',
            'first_name': 'Menor',
            'last_name': 'Tres',
            'dni': '66666666',
            'telefono': '11-6666-6666',
            'fecha_nacimiento': '2015-01-01',
            'password1': 'testpass123',
            'password2': 'testpass123',
        })
        self.assertEqual(response.status_code, 200)  # No redirige, muestra errores
        self.assertFalse(Usuario.objects.filter(email='menor3@ejemplo.com').exists())


class LoginViewTest(TestCase):
    """Pruebas de la vista de inicio de sesion."""

    def setUp(self):
        self.client = Client()
        self.usuario = Usuario.objects.create_user(
            email='login@ejemplo.com',
            username='loginuser',
            password='testpass123',
            first_name='Login',
            last_name='User',
            dni='55555555',
            fecha_nacimiento=date(1990, 1, 1),
            rol=Usuario.ROL_ALUMNO
        )

    def test_login_correcto(self):
        """Verifica que un usuario puede iniciar sesion correctamente."""
        response = self.client.post(reverse('login'), {
            'username': 'login@ejemplo.com',
            'password': 'testpass123',
        })
        self.assertEqual(response.status_code, 302)

    def test_login_incorrecto(self):
        """Verifica que un usuario no puede iniciar sesion con contraseña incorrecta."""
        response = self.client.post(reverse('login'), {
            'username': 'login@ejemplo.com',
            'password': 'wrongpassword',
        })
        self.assertEqual(response.status_code, 200)  # No redirige, muestra errores
