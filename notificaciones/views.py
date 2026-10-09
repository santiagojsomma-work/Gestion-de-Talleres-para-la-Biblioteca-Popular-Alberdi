"""
Vistas del modulo de notificaciones.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .models import Notificacion, Novedad
from usuarios.decorators import es_admin_required


@login_required
def mis_notificaciones(request):
    """
    Vista para que el usuario vea sus notificaciones.
    """
    notificaciones = Notificacion.objects.filter(usuario_destinatario=request.user)
    no_leidas = notificaciones.filter(leida=False).count()

    return render(request, 'notificaciones/mis_notificaciones.html', {
        'notificaciones': notificaciones,
        'no_leidas': no_leidas,
    })


@login_required
@require_http_methods(["POST"])
def marcar_notificacion_leida(request, notificacion_pk):
    """
    Vista para marcar una notificacion como leida.
    """
    notificacion = get_object_or_404(Notificacion, pk=notificacion_pk, usuario_destinatario=request.user)
    notificacion.marcar_como_leida()
    return redirect('mis_notificaciones')


@login_required
@es_admin_required
@require_http_methods(["GET", "POST"])
def crear_novedad(request):
    """
    Vista para que el administrador cree una novedad o evento.
    """
    if request.method == 'POST':
        titulo = request.POST.get('titulo', '')
        contenido = request.POST.get('contenido', '')
        tipo = request.POST.get('tipo', Novedad.NOVEDAD)

        if not titulo or not contenido:
            messages.error(request, 'Debe completar todos los campos.')
            return render(request, 'notificaciones/crear_novedad.html')

        novedad = Novedad.objects.create(
            titulo=titulo,
            contenido=contenido,
            tipo=tipo
        )

        # Crear notificacion para todos los usuarios
        from usuarios.models import Usuario
        for usuario in Usuario.objects.all():
            Notificacion.objects.create(
                usuario_destinatario=usuario,
                titulo=titulo,
                mensaje=contenido,
                tipo=Notificacion.NOVEDAD
            )

        messages.success(request, 'Novedad creada y notificada a todos los usuarios.')
        return redirect('lista_novedades')

    return render(request, 'notificaciones/crear_novedad.html')


@login_required
@es_admin_required
def lista_novedades(request):
    """
    Vista para que el administrador vea la lista de novedades.
    """
    novedades = Novedad.objects.all()
    return render(request, 'notificaciones/lista_novedades.html', {
        'novedades': novedades,
    })


@login_required
def novedades_publicas(request):
    """
    Vista publica para ver las novedades y eventos.
    """
    novedades = Novedad.objects.all()
    return render(request, 'notificaciones/novedades_publicas.html', {
        'novedades': novedades,
    })
