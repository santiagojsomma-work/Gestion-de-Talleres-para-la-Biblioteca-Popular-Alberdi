"""
Servicios del modulo de estadisticas.
Incluye funciones de calculo de indicadores.
"""

from django.db.models import Count, Q, Avg
from talleres.models import Taller
from inscripciones.models import Inscripcion
from asistencia.models import Asistencia, Clase
from pagos.models import Cuota


def calcular_porcentaje_al_dia(taller):
    """
    Calcula el porcentaje de alumnos al dia en un taller.
    Formula: (alumnos activos al dia / alumnos activos) x 100
    """
    inscripciones = Inscripcion.objects.filter(taller=taller, activa=True, en_lista_espera=False)
    total = inscripciones.count()

    if total == 0:
        return 0

    alumnos_al_dia = 0
    for inscripcion in inscripciones:
        # Verificar si tiene cuotas vencidas sin pagar
        cuotas_vencidas = Cuota.objects.filter(
            inscripcion=inscripcion,
            estado__in=[Cuota.VENCIDA, Cuota.PARCIAL]
        ).count()
        if cuotas_vencidas == 0:
            alumnos_al_dia += 1

    return (alumnos_al_dia / total) * 100


def calcular_promedio_asistencia(taller):
    """
    Calcula el promedio de asistencia de un taller.
    Formula: presentes / (clases dictadas x alumnos inscriptos)
    Solo se cuentan las clases posteriores a la inscripcion de cada alumno.
    """
    inscripciones = Inscripcion.objects.filter(taller=taller, activa=True, en_lista_espera=False)
    total_inscriptos = inscripciones.count()

    if total_inscriptos == 0:
        return 0

    clases = Clase.objects.filter(taller=taller)
    total_clases = clases.count()

    if total_clases == 0:
        return 0

    # Calcular el total de posibles asistencias (clases posteriores a cada inscripcion)
    total_posible = 0
    for inscripcion in inscripciones:
        clases_posteriores = clases.filter(fecha__gte=inscripcion.fecha_inscripcion).count()
        total_posible += clases_posteriores

    if total_posible == 0:
        return 0

    # Contar presentes
    presentes = Asistencia.objects.filter(
        clase__taller=taller,
        estado=Asistencia.PRESENTE
    ).count()

    # Calcular promedio
    promedio = (presentes / total_posible) * 100
    return promedio


def calcular_cantidad_alumnos(taller):
    """
    Calcula la cantidad de alumnos activos en un taller.
    """
    return Inscripcion.objects.filter(taller=taller, activa=True, en_lista_espera=False).count()


def obtener_estadisticas_talleres():
    """
    Obtiene las estadisticas de todos los talleres activos.
    Retorna una lista de diccionarios con los datos de cada taller.
    """
    talleres = Taller.objects.filter(activo=True)
    estadisticas = []

    for taller in talleres:
        estadisticas.append({
            'id': taller.id,
            'nombre': taller.nombre,
            'docente': str(taller.docente) if taller.docente else 'Sin asignar',
            'cantidad_alumnos': calcular_cantidad_alumnos(taller),
            'porcentaje_al_dia': round(calcular_porcentaje_al_dia(taller), 2),
            'promedio_asistencia': round(calcular_promedio_asistencia(taller), 2),
        })

    return estadisticas


def exportar_csv(estadisticas, filename='estadisticas.csv'):
    """
    Exporta las estadisticas a un archivo CSV.
    """
    import csv
    from django.http import HttpResponse

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    writer = csv.writer(response)
    writer.writerow(['Taller', 'Docente', 'Cantidad de Alumnos', '% Al Dia', 'Promedio de Asistencia'])

    for estadistica in estadisticas:
        writer.writerow([
            estadistica['nombre'],
            estadistica['docente'],
            estadistica['cantidad_alumnos'],
            estadistica['porcentaje_al_dia'],
            estadistica['promedio_asistencia'],
        ])

    return response
