"""
Vistas del modulo de usuarios.
Incluye registro, login, logout, perfil y aprobacion de docentes.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .forms import RegistroAlumnoForm, RegistroDocenteForm, LoginForm, PerfilForm
from .models import Usuario
from .decorators import es_admin_required, es_docente_required


@require_http_methods(["GET", "POST"])
def registro_alumno(request):
    """
    Vista para el registro de alumnos.
    Si el alumno es menor de edad, se crea tambien el registro del tutor.
    """
    if request.method == 'POST':
        form = RegistroAlumnoForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            messages.success(request, 'Registro exitoso. Bienvenido/a!')
            return redirect('home')
    else:
        form = RegistroAlumnoForm()

    return render(request, 'usuarios/registro_alumno.html', {'form': form})


@require_http_methods(["GET", "POST"])
def registro_docente(request):
    """
    Vista para el registro de docentes.
    Los docentes quedan pendientes de aprobacion del administrador.
    """
    if request.method == 'POST':
        form = RegistroDocenteForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            messages.success(request, 'Registro exitoso. Su cuenta esta pendiente de aprobacion por el administrador.')
            return redirect('login')
    else:
        form = RegistroDocenteForm()

    return render(request, 'usuarios/registro_docente.html', {'form': form})


@require_http_methods(["GET", "POST"])
def login_view(request):
    """
    Vista para el inicio de sesion.
    """
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            usuario = authenticate(request, username=email, password=password)
            if usuario is not None:
                # Verificar si el docente esta aprobado
                if usuario.es_docente and not usuario.aprobado:
                    messages.error(request, 'Su cuenta esta pendiente de aprobacion por el administrador.')
                    return render(request, 'registration/login.html', {'form': form})
                login(request, usuario)
                messages.success(request, f'Bienvenido/a, {usuario.first_name}!')
                return redirect('home')
    else:
        form = LoginForm()

    return render(request, 'registration/login.html', {'form': form})


@require_http_methods(["POST"])
def logout_view(request):
    """
    Vista para el cierre de sesion.
    """
    logout(request)
    messages.success(request, 'Sesion cerrada correctamente.')
    return redirect('home')


@login_required
@require_http_methods(["GET", "POST"])
def perfil(request):
    """
    Vista para ver y editar el perfil de usuario.
    """
    if request.method == 'POST':
        form = PerfilForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado correctamente.')
            return redirect('perfil')
    else:
        form = PerfilForm(instance=request.user)

    return render(request, 'usuarios/perfil.html', {'form': form})


@login_required
@es_admin_required
def aprobar_docente(request, pk):
    """
    Vista para que el administrador apruebe un docente.
    """
    docente = get_object_or_404(Usuario, pk=pk, rol=Usuario.ROL_DOCENTE)
    docente.aprobado = True
    docente.save()
    messages.success(request, f'El docente {docente.first_name} {docente.last_name} ha sido aprobado.')
    return redirect('lista_docentes_pendientes')


@login_required
@es_admin_required
def rechazar_docente(request, pk):
    """
    Vista para que el administrador rechace un docente.
    """
    docente = get_object_or_404(Usuario, pk=pk, rol=Usuario.ROL_DOCENTE)
    docente.delete()
    messages.success(request, f'El docente {docente.first_name} {docente.last_name} ha sido rechazado.')
    return redirect('lista_docentes_pendientes')


@login_required
@es_admin_required
def lista_docentes_pendientes(request):
    """
    Vista para que el administrador vea la lista de docentes pendientes de aprobacion.
    """
    docentes_pendientes = Usuario.objects.filter(rol=Usuario.ROL_DOCENTE, aprobado=False)
    return render(request, 'usuarios/lista_docentes_pendientes.html', {
        'docentes_pendientes': docentes_pendientes
    })
