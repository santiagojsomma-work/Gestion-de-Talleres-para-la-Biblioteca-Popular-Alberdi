"""
Vistas del modulo de talleres.
Incluye CRUD para el administrador y grilla semanal publica.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .models import Taller, Horario
from .forms import TallerForm, HorarioForm
from usuarios.decorators import es_admin_required


@login_required
@es_admin_required
def lista_talleres(request):
    """
    Vista para que el administrador vea la lista de talleres.
    """
    talleres = Taller.objects.all().order_by('-activo', 'nombre')
    return render(request, 'talleres/lista_talleres.html', {'talleres': talleres})


@login_required
@es_admin_required
@require_http_methods(["GET", "POST"])
def crear_taller(request):
    """
    Vista para que el administrador cree un nuevo taller.
    """
    if request.method == 'POST':
        form = TallerForm(request.POST)
        if form.is_valid():
            taller = form.save()
            messages.success(request, f'El taller "{taller.nombre}" fue creado correctamente.')
            return redirect('lista_talleres')
    else:
        form = TallerForm()

    return render(request, 'talleres/formulario_taller.html', {'form': form, 'titulo': 'Crear Taller'})


@login_required
@es_admin_required
@require_http_methods(["GET", "POST"])
def editar_taller(request, pk):
    """
    Vista para que el administrador edite un taller.
    """
    taller = get_object_or_404(Taller, pk=pk)

    if request.method == 'POST':
        form = TallerForm(request.POST, instance=taller)
        if form.is_valid():
            taller = form.save()
            messages.success(request, f'El taller "{taller.nombre}" fue actualizado correctamente.')
            return redirect('lista_talleres')
    else:
        form = TallerForm(instance=taller)

    return render(request, 'talleres/formulario_taller.html', {'form': form, 'titulo': 'Editar Taller', 'taller': taller})


@login_required
@es_admin_required
def dar_baja_taller(request, pk):
    """
    Vista para que el administrador de de baja un taller (baja logica).
    """
    taller = get_object_or_404(Taller, pk=pk)
    taller.activo = False
    taller.save()
    messages.success(request, f'El taller "{taller.nombre}" fue dado de baja correctamente.')
    return redirect('lista_talleres')


@login_required
@es_admin_required
def dar_alta_taller(request, pk):
    """
    Vista para que el administrador reactive un taller dado de baja.
    """
    taller = get_object_or_404(Taller, pk=pk)
    taller.activo = True
    taller.save()
    messages.success(request, f'El taller "{taller.nombre}" fue reactivado correctamente.')
    return redirect('lista_talleres')


def grilla_semanal(request):
    """
    Vista publica que muestra la grilla semanal de horarios de todos los talleres activos.
    """
    talleres_activos = Taller.objects.filter(activo=True).prefetch_related('horarios', 'docente')

    # Organizar horarios por dia de la semana
    horarios_por_dia = {i: [] for i in range(7)}
    for taller in talleres_activos:
        for horario in taller.horarios.all():
            horarios_por_dia[horario.dia_semana].append({
                'taller': taller,
                'horario': horario,
            })

    dias_semana = Taller._meta.get_field('horarios').related_model.DIAS_SEMANA

    return render(request, 'talleres/grilla_semanal.html', {
        'horarios_por_dia': horarios_por_dia,
        'dias_semana': dias_semana,
    })
