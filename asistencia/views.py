"""
Vistas del modulo de asistencia.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.db.models import Count, Q
from .models import Clase, Asistencia
from talleres.models import Taller
from inscripciones.models import Inscripcion
from usuarios.decorators import es_docente_required, es_alumno_required


@login_required
@es_docente_required
def tomar_asistencia(request, clase_pk):
    """
    Vista para que el docente tome asistencia de una clase.
    """
    clase = get_object_or_404(Clase, pk=clase_pk)
    inscripciones = Inscripcion.objects.filter(
        taller=clase.taller,
        activa=True,
        en_lista_espera=False
    ).select_related('alumno')

    if request.method == 'POST':
        for inscripcion in inscripciones:
            estado = request.POST.get(f'estado_{inscripcion.pk}', Asistencia.PRESENTE)
            justificacion = request.POST.get(f'justificacion_{inscripcion.pk}', '')

            Asistencia.objects.update_or_create(
                clase=clase,
                inscripcion=inscripcion,
                defaults={
                    'estado': estado,
                    'justificacion': justificacion if estado == Asistencia.JUSTIFICADO else ''
                }
            )

        messages.success(request, 'Asistencia registrada correctamente.')
        return redirect('lista_clases', taller_pk=clase.taller.pk)

    # Obtener asistencias existentes
    asistencias_existentes = {
        a.inscripcion_id: a for a in Asistencia.objects.filter(clase=clase)
    }

    # Crear lista de tuplas (inscripcion, asistencia) para la plantilla
    inscripciones_con_asistencia = [
        (inscripcion, asistencias_existentes.get(inscripcion.pk))
        for inscripcion in inscripciones
    ]

    return render(request, 'asistencia/tomar_asistencia.html', {
        'clase': clase,
        'inscripciones_con_asistencia': inscripciones_con_asistencia,
    })


@login_required
@es_docente_required
def lista_clases(request, taller_pk):
    """
    Vista para que el docente vea las clases de un taller.
    """
    taller = get_object_or_404(Taller, pk=taller_pk)
    clases = Clase.objects.filter(taller=taller).order_by('-fecha')

    return render(request, 'asistencia/lista_clases.html', {
        'taller': taller,
        'clases': clases,
    })


@login_required
@es_docente_required
@require_http_methods(["POST"])
def crear_clase(request, taller_pk):
    """
    Vista para que el docente cree una nueva clase.
    """
    taller = get_object_or_404(Taller, pk=taller_pk)
    fecha = request.POST.get('fecha')
    tema = request.POST.get('tema', '')

    if not fecha:
        messages.error(request, 'Debe indicar la fecha de la clase.')
        return redirect('lista_clases', taller_pk=taller.pk)

    from datetime import datetime
    fecha = datetime.strptime(fecha, '%Y-%m-%d').date()

    Clase.objects.get_or_create(
        taller=taller,
        fecha=fecha,
        defaults={'tema': tema}
    )

    messages.success(request, 'Clase creada correctamente.')
    return redirect('lista_clases', taller_pk=taller.pk)


@login_required
def mi_asistencia(request):
    """
    Vista para que el alumno consulte su asistencia.
    """
    asistencias = Asistencia.objects.filter(
        inscripcion__alumno=request.user
    ).select_related('clase', 'clase__taller', 'inscripcion__taller')

    # Calcular promedio por taller
    promedios = {}
    for taller_id in asistencias.values_list('clase__taller_id', flat=True).distinct():
        taller_asistencias = asistencias.filter(clase__taller_id=taller_id)
        total_clases = Clase.objects.filter(taller_id=taller_id).count()
        total_inscriptos = Inscripcion.objects.filter(taller_id=taller_id, activa=True).count()

        if total_clases > 0 and total_inscriptos > 0:
            presentes = taller_asistencias.filter(estado=Asistencia.PRESENTE).count()
            # Solo contar clases posteriores a la inscripcion de cada alumno
            total_posible = sum(
                max(0, Clase.objects.filter(taller_id=taller_id, fecha__gte=ins.fecha_inscripcion).count())
                for ins in Inscripcion.objects.filter(taller_id=taller_id, activa=True)
            )
            if total_posible > 0:
                promedios[taller_id] = (presentes / total_posible) * 100

    return render(request, 'asistencia/mi_asistencia.html', {
        'asistencias': asistencias,
        'promedios': promedios,
    })
