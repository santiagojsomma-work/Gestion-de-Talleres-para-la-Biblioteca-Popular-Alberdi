"""
Vistas del modulo de estadisticas.
"""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .services import obtener_estadisticas_talleres, exportar_csv
from usuarios.decorators import es_admin_required


@login_required
@es_admin_required
def panel_estadisticas(request):
    """
    Vista para que el administrador vea el panel de estadisticas.
    """
    estadisticas = obtener_estadisticas_talleres()

    # Preparar datos para los graficos
    nombres = [e['nombre'] for e in estadisticas]
    alumnos = [e['cantidad_alumnos'] for e in estadisticas]
    porcentajes_al_dia = [e['porcentaje_al_dia'] for e in estadisticas]
    promedios_asistencia = [e['promedio_asistencia'] for e in estadisticas]

    return render(request, 'estadisticas/panel.html', {
        'estadisticas': estadisticas,
        'nombres': nombres,
        'alumnos': alumnos,
        'porcentajes_al_dia': porcentajes_al_dia,
        'promedios_asistencia': promedios_asistencia,
    })


@login_required
@es_admin_required
def exportar_estadisticas_csv(request):
    """
    Vista para exportar las estadisticas a CSV.
    """
    estadisticas = obtener_estadisticas_talleres()
    return exportar_csv(estadisticas)
