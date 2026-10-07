"""
Servicios del modulo de pagos.
Incluye la generacion de cuotas mensuales y el calculo de estado de pago.
"""

from datetime import date
from decimal import Decimal
from django.db import transaction
from .models import Cuota, Pago


def generar_cuota_mensual(inscripcion, mes_anio=None):
    """
    Genera una cuota mensual para una inscripcion.
    Si no se especifica mes_anio, usa el mes actual.
    """
    if mes_anio is None:
        mes_anio = date.today().replace(day=1)

    # Verificar si ya existe la cuota
    if Cuota.objects.filter(inscripcion=inscripcion, mes_anio=mes_anio).exists():
        return None

    # Calcular fecha de vencimiento (dia 10 del mes siguiente)
    if mes_anio.month == 12:
        fecha_vencimiento = date(mes_anio.year + 1, 1, 10)
    else:
        fecha_vencimiento = date(mes_anio.year, mes_anio.month + 1, 10)

    cuota = Cuota.objects.create(
        inscripcion=inscripcion,
        mes_anio=mes_anio,
        monto=inscripcion.taller.cuota_mensual,
        fecha_vencimiento=fecha_vencimiento
    )

    return cuota


def generar_cuotas_mensuales():
    """
    Genera cuotas mensuales para todas las inscripciones activas.
    Retorna la cantidad de cuotas generadas.
    """
    from inscripciones.models import Inscripcion

    inscripciones = Inscripcion.objects.filter(activa=True, en_lista_espera=False)
    mes_actual = date.today().replace(day=1)
    cantidad = 0

    for inscripcion in inscripciones:
        cuota = generar_cuota_mensual(inscripcion, mes_actual)
        if cuota:
            cantidad += 1

    return cantidad


def calcular_estado_pago(alumno):
    """
    Calcula el estado de pago de un alumno.
    Retorna 'al_dia', 'pago_parcial' o 'adeudado'.
    """
    from inscripciones.models import Inscripcion

    inscripciones = Inscripcion.objects.filter(alumno=alumno, activa=True, en_lista_espera=False)

    tiene_pago_parcial = False
    tiene_adeudado = False

    for inscripcion in inscripciones:
        cuotas = Cuota.objects.filter(inscripcion=inscripcion)

        for cuota in cuotas:
            if cuota.estado == Cuota.VENCIDA:
                tiene_adeudado = True
            elif cuota.estado == Cuota.PARCIAL:
                tiene_pago_parcial = True

    if tiene_adeudado:
        return 'adeudado'
    elif tiene_pago_parcial:
        return 'pago_parcial'
    else:
        return 'al_dia'


def registrar_pago(cuota, monto, metodo, fecha_pago=None):
    """
    Registra un pago sobre una cuota.
    Retorna el objeto Pago creado.
    """
    if fecha_pago is None:
        fecha_pago = date.today()

    with transaction.atomic():
        pago = Pago.objects.create(
            cuota=cuota,
            monto=monto,
            fecha_pago=fecha_pago,
            metodo=metodo
        )

        # Enviar notificacion por email
        enviar_notificacion_pago(pago)

        return pago


def enviar_notificacion_pago(pago):
    """
    Envia un email al alumno notificando que se registro su pago.
    """
    from django.core.mail import send_mail
    from django.conf import settings

    alumno = pago.cuota.inscripcion.alumno
    taller = pago.cuota.inscripcion.taller

    subject = f'Pago registrado - {taller.nombre}'
    message = f'''
    Estimado/a {alumno.first_name} {alumno.last_name},

    Le informamos que su pago ha sido registrado correctamente en el sistema.

    Detalles del pago:
    - Taller: {taller.nombre}
    - Mes: {pago.cuota.mes_anio.strftime("%Y-%m")}
    - Monto: ${pago.monto}
    - Fecha: {pago.fecha_pago}
    - Metodo: {pago.get_metodo_display()}

    Si tiene alguna consulta, no dude en contactarnos.

    Saludos cordiales,
    Biblioteca
    '''

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[alumno.email],
        fail_silently=True
    )
