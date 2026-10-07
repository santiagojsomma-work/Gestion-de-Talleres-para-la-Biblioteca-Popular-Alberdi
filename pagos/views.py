"""
Vistas del modulo de pagos.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.db import transaction
from .models import Cuota, Pago
from .services import registrar_pago, calcular_estado_pago
from usuarios.decorators import es_admin_required, es_docente_required


@login_required
@es_admin_required
def cuotas_pendientes(request):
    """
    Vista para que el administrador vea las cuotas pendientes y vencidas.
    """
    cuotas = Cuota.objects.filter(estado__in=[Cuota.PENDIENTE, Cuota.VENCIDA, Cuota.PARCIAL]).select_related(
        'inscripcion__alumno', 'inscripcion__taller'
    ).order_by('fecha_vencimiento')

    return render(request, 'pagos/cuotas_pendientes.html', {'cuotas': cuotas})


@login_required
@es_admin_required
@require_http_methods(["GET", "POST"])
def registrar_pago_view(request, cuota_pk):
    """
    Vista para que el administrador registre un pago.
    """
    cuota = get_object_or_404(Cuota, pk=cuota_pk)

    if request.method == 'POST':
        try:
            monto = request.POST.get('monto')
            metodo = request.POST.get('metodo')
            fecha_pago = request.POST.get('fecha_pago')

            if not monto or not metodo:
                messages.error(request, 'Debe completar todos los campos.')
                return redirect('registrar_pago', cuota_pk=cuota.pk)

            from datetime import datetime
            fecha_pago = datetime.strptime(fecha_pago, '%Y-%m-%d').date() if fecha_pago else None

            pago = registrar_pago(cuota, monto, metodo, fecha_pago)
            messages.success(request, f'Pago de ${monto} registrado correctamente.')

        except Exception as e:
            messages.error(request, f'No se pudo registrar el pago: {str(e)}')

        return redirect('cuotas_pendientes')

    return render(request, 'pagos/registrar_pago.html', {'cuota': cuota})


@login_required
@es_admin_required
@require_http_methods(["POST"])
def anular_pago(request, pago_pk):
    """
    Vista para que el administrador anule un pago con motivo.
    """
    pago = get_object_or_404(Pago, pk=pago_pk)
    motivo = request.POST.get('motivo', '')

    if not motivo:
        messages.error(request, 'Debe indicar el motivo de la anulacion.')
        return redirect('cuotas_pendientes')

    pago.anular(motivo)
    messages.success(request, 'Pago anulado correctamente.')
    return redirect('cuotas_pendientes')


@login_required
def mis_pagos(request):
    """
    Vista para que el alumno consulte su estado de pagos.
    """
    estado = calcular_estado_pago(request.user)
    cuotas = Cuota.objects.filter(inscripcion__alumno=request.user).select_related(
        'inscripcion__taller'
    ).order_by('-mes_anio')

    return render(request, 'pagos/mis_pagos.html', {
        'estado': estado,
        'cuotas': cuotas
    })
