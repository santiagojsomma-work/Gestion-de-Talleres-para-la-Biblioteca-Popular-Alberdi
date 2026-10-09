"""
Pruebas automatizadas del modulo de pagos.
"""

from datetime import date
from django.test import TestCase
from .models import Cuota, Pago
from inscripciones.models import Inscripcion
from usuarios.models import Usuario
from talleres.models import Taller


class PagoModelTest(TestCase):
    """Pruebas del modelo Pago."""

    def setUp(self):
        self.alumno = Usuario.objects.create_user(
            email='alumno_pago@test.com',
            username='alumno_pago',
            password='testpass123',
            first_name='Alumno',
            last_name='Pago',
            dni='77777777',
            fecha_nacimiento='1990-01-01',
            rol=Usuario.ROL_ALUMNO
        )
        self.docente = Usuario.objects.create_user(
            email='docente_pago@test.com',
            username='docente_pago',
            password='testpass123',
            first_name='Docente',
            last_name='Pago',
            dni='88888888',
            fecha_nacimiento='1985-01-01',
            rol=Usuario.ROL_DOCENTE,
            aprobado=True
        )
        self.taller = Taller.objects.create(
            nombre='Taller de Pagos',
            docente=self.docente,
            cupo=10,
            cuota_mensual=15000.00
        )
        self.inscripcion = Inscripcion.objects.create(
            alumno=self.alumno,
            taller=self.taller
        )
        self.cuota = Cuota.objects.create(
            inscripcion=self.inscripcion,
            mes_anio=date(2026, 10, 1),
            monto=15000.00,
            fecha_vencimiento=date(2026, 11, 10)
        )

    def test_creacion_cuota(self):
        """Verifica que se puede crear una cuota."""
        self.assertEqual(self.cuota.monto, 15000.00)
        self.assertEqual(self.cuota.estado, Cuota.PENDIENTE)

    def test_pago_completo(self):
        """Verifica que un pago completo actualiza el estado de la cuota."""
        pago = Pago.objects.create(
            cuota=self.cuota,
            monto=15000.00,
            fecha_pago=date(2026, 10, 5),
            metodo=Pago.EFECTIVO
        )
        self.cuota.refresh_from_db()
        self.assertEqual(self.cuota.estado, Cuota.PAGADA)

    def test_pago_parcial(self):
        """Verifica que un pago parcial actualiza el estado de la cuota."""
        pago = Pago.objects.create(
            cuota=self.cuota,
            monto=5000.00,
            fecha_pago=date(2026, 10, 5),
            metodo=Pago.EFECTIVO
        )
        self.cuota.refresh_from_db()
        self.assertEqual(self.cuota.estado, Cuota.PARCIAL)
        self.assertEqual(self.cuota.saldo_pendiente, 10000.00)

    def test_anular_pago(self):
        """Verifica que se puede anular un pago."""
        pago = Pago.objects.create(
            cuota=self.cuota,
            monto=15000.00,
            fecha_pago=date(2026, 10, 5),
            metodo=Pago.EFECTIVO
        )
        pago.anular('Error en el pago')
        self.cuota.refresh_from_db()
        self.assertTrue(pago.anulado)
        self.assertEqual(self.cuota.estado, Cuota.PENDIENTE)
