"""
Modelos del modulo de pagos.
Incluye los modelos de Cuota y Pago.
"""

from django.db import models
from django.core.exceptions import ValidationError
from inscripciones.models import Inscripcion


class Cuota(models.Model):
    """
    Modelo que representa una cuota mensual generada automaticamente.
    """

    # Estados de la cuota
    PENDIENTE = 'pendiente'
    PAGADA = 'pagada'
    PARCIAL = 'parcial'
    VENCIDA = 'vencida'
    ESTADOS = [
        (PENDIENTE, 'Pendiente'),
        (PAGADA, 'Pagada'),
        (PARCIAL, 'Pago parcial'),
        (VENCIDA, 'Vencida'),
    ]

    inscripcion = models.ForeignKey(
        Inscripcion,
        on_delete=models.CASCADE,
        related_name='cuotas',
        verbose_name='Inscripcion'
    )
    mes_anio = models.DateField(verbose_name='Mes y anio')
    monto = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Monto (ARS)')
    fecha_vencimiento = models.DateField(verbose_name='Fecha de vencimiento')
    estado = models.CharField(max_length=20, choices=ESTADOS, default=PENDIENTE, verbose_name='Estado')
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creacion')

    class Meta:
        verbose_name = 'Cuota'
        verbose_name_plural = 'Cuotas'
        unique_together = ['inscripcion', 'mes_anio']
        ordering = ['-mes_anio']

    def __str__(self):
        return f'Cuota {self.mes_anio.strftime("%Y-%m")} - {self.inscripcion} - {self.get_estado_display()}'

    def save(self, *args, **kwargs):
        """Al guardar, verifica si la cuota esta vencida."""
        from datetime import date
        if self.estado == self.PENDIENTE and date.today() > self.fecha_vencimiento:
            self.estado = self.VENCIDA
        super().save(*args, **kwargs)

    @property
    def monto_pagado(self):
        """Devuelve el monto total pagado (sin anulaciones)."""
        return self.pagos.filter(anulado=False).aggregate(
            total=models.Sum('monto')
        )['total'] or 0

    @property
    def saldo_pendiente(self):
        """Devuelve el saldo pendiente de pago."""
        return self.monto - self.monto_pagado


class Pago(models.Model):
    """
    Modelo que representa un pago realizado sobre una cuota.
    """

    # Metodos de pago
    EFECTIVO = 'efectivo'
    TRANSFERENCIA = 'transferencia'
    DEBITO = 'debito'
    METODOS = [
        (EFECTIVO, 'Efectivo'),
        (TRANSFERENCIA, 'Transferencia'),
        (DEBITO, 'Debito'),
    ]

    cuota = models.ForeignKey(
        Cuota,
        on_delete=models.CASCADE,
        related_name='pagos',
        verbose_name='Cuota'
    )
    monto = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Monto (ARS)')
    fecha_pago = models.DateField(verbose_name='Fecha de pago')
    metodo = models.CharField(max_length=20, choices=METODOS, verbose_name='Metodo de pago')
    anulado = models.BooleanField(default=False, verbose_name='Anulado')
    motivo_anulacion = models.TextField(blank=True, verbose_name='Motivo de anulacion')
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creacion')

    class Meta:
        verbose_name = 'Pago'
        verbose_name_plural = 'Pagos'
        ordering = ['-fecha_creacion']

    def __str__(self):
        estado = 'ANULADO' if self.anulado else 'Activo'
        return f'Pago ${self.monto} - {self.cuota} - {estado}'

    def clean(self):
        """Valida que el monto del pago no supere el saldo pendiente."""
        if not self.anulado:
            saldo = self.cuota.saldo_pendiente
            if self.monto > saldo:
                raise ValidationError(f'El monto del pago (${self.monto}) supera el saldo pendiente (${saldo}).')

    def save(self, *args, **kwargs):
        """Al guardar, actualiza el estado de la cuota."""
        super().save(*args, **kwargs)
        self.actualizar_estado_cuota()

    def actualizar_estado_cuota(self):
        """Actualiza el estado de la cuota segun los pagos registrados."""
        cuota = self.cuota
        monto_pagado = cuota.monto_pagado

        if monto_pagado >= cuota.monto:
            cuota.estado = Cuota.PAGADA
        elif monto_pagado > 0:
            cuota.estado = Cuota.PARCIAL
        else:
            from datetime import date
            if date.today() > cuota.fecha_vencimiento:
                cuota.estado = Cuota.VENCIDA
            else:
                cuota.estado = Cuota.PENDIENTE

        cuota.save()

    def anular(self, motivo):
        """Anula el pago con un motivo."""
        self.anulado = True
        self.motivo_anulacion = motivo
        self.save()
        self.actualizar_estado_cuota()
