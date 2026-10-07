"""
Vistas del modulo de inscripciones.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.db import transaction
from .models import Inscripcion
from talleres.models import Taller
from usuarios.decorators import es_alumno_required


@login_required
@es_alumno_required
def mis_inscripciones(request):
    """
    Vista para que el alumno vea sus inscripciones activas.
    """
    inscripciones = Inscripcion.objects.filter(alumno=request.user, activa=True).select_related('taller')
    return render(request, 'inscripciones/mis_inscripciones.html', {'inscripciones': inscripciones})


@login_required
@es_alumno_required
@require_http_methods(["POST"])
def inscribirse(request, taller_pk):
    """
    Vista para que un alumno se inscriba a un taller.
    Si no hay cupo, se anota en lista de espera.
    """
    taller = get_object_or_404(Taller, pk=taller_pk, activo=True)

    try:
        with transaction.atomic():
            # Verificar que no este ya inscripto
            if Inscripcion.objects.filter(alumno=request.user, taller=taller, activa=True).exists():
                messages.warning(request, 'Ya estas inscripto en este taller.')
                return redirect('grilla_semanal')

            # Crear la inscripcion
            inscripcion = Inscripcion(alumno=request.user, taller=taller)
            inscripcion.full_clean()
            inscripcion.save()

            if inscripcion.en_lista_espera:
                messages.info(request, f'No hay cupo disponible. Te anotaste en lista de espera para "{taller.nombre}".')
            else:
                messages.success(request, f'Te inscribiste correctamente a "{taller.nombre}".')

    except Exception as e:
        messages.error(request, f'No se pudo completar la inscripcion: {str(e)}')

    return redirect('grilla_semanal')


@login_required
@es_alumno_required
@require_http_methods(["POST"])
def darse_de_baja(request, inscripcion_pk):
    """
    Vista para que un alumno se de de baja de un taller.
    Si hay alumnos en lista de espera, notifica al primero.
    """
    inscripcion = get_object_or_404(Inscripcion, pk=inscripcion_pk, alumno=request.user, activa=True)

    with transaction.atomic():
        taller = inscripcion.taller
        inscripcion.activa = False
        inscripcion.save()

        # Notificar a lista de espera si no estaba en lista de espera
        if not inscripcion.en_lista_espera:
            Inscripcion.notificar_lista_espera(taller)

        messages.success(request, f'Te diste de baja de "{taller.nombre}".')

    return redirect('mis_inscripciones')
