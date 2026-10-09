"""
Pruebas automatizadas del modulo de asistencia.
"""

from django.test import TestCase
from .models import Clase, Asistencia
from inscripciones.models import Inscripcion
from usuarios.models import Usuario
from talleres.models import Taller


class AsistenciaModelTest(TestCase):
    """Pruebas del modelo Asistencia."""

    def setUp(self):
        self.alumno = Usuario.objects.create_user(
            email='alumno_asis@test.com',
            username='alumno_asis',
            password='testpass123',
            first_name='Alumno',
            last_name='Asistencia',
            dni='99999999',
            fecha_nacimiento='1990-01-01',
            rol=Usuario.ROL_ALUMNO
        )
        self.docente = Usuario.objects.create_user(
            email='docente_asis@test.com',
            username='docente_asis',
            password='testpass123',
            first_name='Docente',
            last_name='Asistencia',
            dni='10101010',
            fecha_nacimiento='1985-01-01',
            rol=Usuario.ROL_DOCENTE,
            aprobado=True
        )
        self.taller = Taller.objects.create(
            nombre='Taller de Asistencia',
            docente=self.docente,
            cupo=10,
            cuota_mensual=15000.00
        )
        self.inscripcion = Inscripcion.objects.create(
            alumno=self.alumno,
            taller=self.taller
        )
        self.clase = Clase.objects.create(
            taller=self.taller,
            fecha='2026-10-07',
            tema='Clase 1'
        )

    def test_creacion_clase(self):
        """Verifica que se puede crear una clase."""
        self.assertEqual(self.clase.tema, 'Clase 1')
        self.assertFalse(self.clase.suspendida)

    def test_creacion_asistencia(self):
        """Verifica que se puede registrar asistencia."""
        asistencia = Asistencia.objects.create(
            clase=self.clase,
            inscripcion=self.inscripcion,
            estado=Asistencia.PRESENTE
        )
        self.assertEqual(asistencia.estado, Asistencia.PRESENTE)

    def test_asistencia_justificada(self):
        """Verifica que se puede registrar una ausencia justificada."""
        asistencia = Asistencia.objects.create(
            clase=self.clase,
            inscripcion=self.inscripcion,
            estado=Asistencia.JUSTIFICADO,
            justificacion='Cita medica'
        )
        self.assertEqual(asistencia.estado, Asistencia.JUSTIFICADO)
        self.assertEqual(asistencia.justificacion, 'Cita medica')
