"""
Vistas del modulo de ingresos.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .models import Ingreso
from usuarios.models import Usuario
from inscripciones.models import Inscripcion
from usuarios.decorators import es_admin_required


@login_required
@es_admin_required
@require_http_methods(["GET", "POST"])
def registrar_ingreso(request):
    """
    Vista para que el administrador registre un ingreso por DNI.
    Muestra los talleres a los que esta inscripta la persona.
    """
    if request.method == 'POST':
        dni = request.POST.get('dni', '').strip()
        observacion = request.POST.get('observacion', '')

        if not dni:
            messages.error(request, 'Debe ingresar un DNI.')
            return render(request, 'ingresos/registrar_ingreso.html')

        try:
            usuario = Usuario.objects.get(dni=dni)
        except Usuario.DoesNotExist:
            messages.error(request, f'No se encontro ningun usuario con el DNI {dni}.')
            return render(request, 'ingresos/registrar_ingreso.html')

        # Registrar el ingreso
        ingreso = Ingreso.objects.create(
            usuario=usuario,
            observacion=observacion
        )

        # Obtener inscripciones activas del usuario
        inscripciones = Inscripcion.objects.filter(
            alumno=usuario,
            activa=True
        ).select_related('taller')

        messages.success(request, f'Ingreso registrado para {usuario.first_name} {usuario.last_name}.')

        return render(request, 'ingresos/registrar_ingreso.html', {
            'ingreso': ingreso,
            'usuario': usuario,
            'inscripciones': inscripciones,
        })

    return render(request, 'ingresos/registrar_ingreso.html')


@login_required
@es_admin_required
def historial_ingresos(request):
    """
    Vista para que el administrador vea el historial de ingresos.
    """
    ingresos = Ingreso.objects.all().select_related('usuario').order_by('-fecha_hora')[:50]

    return render(request, 'ingresos/historial_ingresos.html', {
        'ingresos': ingresos,
    })


@login_required
@es_admin_required
def detalle_ingreso(request, ingreso_pk):
    """
    Vista para que el administrador vea el detalle de un ingreso.
    """
    ingreso = get_object_or_404(Ingreso, pk=ingreso_pk)
    inscripciones = Inscripcion.objects.filter(
        alumno=ingreso.usuario,
        activa=True
    ).select_related('taller')

    return render(request, 'ingresos/detalle_ingreso.html', {
        'ingreso': ingreso,
        'inscripciones': inscripciones,
    })
