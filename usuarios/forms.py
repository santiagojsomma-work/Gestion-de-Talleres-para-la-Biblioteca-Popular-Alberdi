"""
Formularios del modulo de usuarios.
Incluye formularios de registro, login y edicion de perfil.
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from .models import Usuario, Tutor


class RegistroAlumnoForm(UserCreationForm):
    """
    Formulario de registro para alumnos.
    Incluye campos adicionales: DNI, telefono, fecha de nacimiento.
    Si el alumno es menor de edad, exige datos del tutor.
    """

    email = forms.EmailField(required=True, label='Email')
    first_name = forms.CharField(max_length=100, required=True, label='Nombre')
    last_name = forms.CharField(max_length=100, required=True, label='Apellido')
    dni = forms.CharField(max_length=20, required=True, label='DNI')
    telefono = forms.CharField(max_length=30, required=False, label='Telefono')
    fecha_nacimiento = forms.DateField(
        required=True,
        label='Fecha de nacimiento',
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    # Campos del tutor (obligatorios si es menor de edad)
    tutor_nombre = forms.CharField(max_length=100, required=False, label='Nombre del tutor')
    tutor_apellido = forms.CharField(max_length=100, required=False, label='Apellido del tutor')
    tutor_dni = forms.CharField(max_length=20, required=False, label='DNI del tutor')
    tutor_telefono = forms.CharField(max_length=30, required=False, label='Telefono del tutor')
    tutor_email = forms.EmailField(required=False, label='Email del tutor')
    tutor_parentesco = forms.ChoiceField(
        choices=Tutor.PARENTESCOS,
        required=False,
        label='Parentesco'
    )

    class Meta:
        model = Usuario
        fields = ['email', 'first_name', 'last_name', 'dni', 'telefono', 'fecha_nacimiento']

    def clean_dni(self):
        """Valida que el DNI no este registrado."""
        dni = self.cleaned_data.get('dni')
        if Usuario.objects.filter(dni=dni).exists():
            raise ValidationError('Ya existe un usuario con este DNI.')
        return dni

    def clean_email(self):
        """Valida que el email no este registrado."""
        email = self.cleaned_data.get('email')
        if Usuario.objects.filter(email=email).exists():
            raise ValidationError('Ya existe un usuario con este email.')
        return email

    def clean(self):
        """Valida que si el alumno es menor de edad, se carguen los datos del tutor."""
        cleaned_data = super().clean()
        fecha_nacimiento = cleaned_data.get('fecha_nacimiento')

        if fecha_nacimiento:
            from datetime import date
            hoy = date.today()
            edad = hoy.year - fecha_nacimiento.year - (
                (hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day)
            )

            if edad < 18:
                # Es menor de edad: validar datos del tutor
                campos_tutor = ['tutor_nombre', 'tutor_apellido', 'tutor_dni', 'tutor_telefono', 'tutor_parentesco']
                for campo in campos_tutor:
                    if not cleaned_data.get(campo):
                        self.add_error(campo, 'Este campo es obligatorio para menores de edad.')

        return cleaned_data

    def save(self, commit=True):
        """Guarda el usuario y crea el tutor si es necesario."""
        usuario = super().save(commit=False)
        usuario.rol = Usuario.ROL_ALUMNO
        usuario.aprobado = True  # Los alumnos se aprueban automaticamente

        if commit:
            usuario.save()

            # Crear el tutor si es menor de edad
            if usuario.es_menor_de_edad:
                Tutor.objects.create(
                    usuario_alumno=usuario,
                    nombre=self.cleaned_data.get('tutor_nombre'),
                    apellido=self.cleaned_data.get('tutor_apellido'),
                    dni=self.cleaned_data.get('tutor_dni'),
                    telefono=self.cleaned_data.get('tutor_telefono'),
                    email=self.cleaned_data.get('tutor_email', ''),
                    parentesco=self.cleaned_data.get('tutor_parentesco')
                )

        return usuario


class RegistroDocenteForm(UserCreationForm):
    """
    Formulario de registro para docentes.
    Los docentes quedan pendientes de aprobacion del administrador.
    """

    email = forms.EmailField(required=True, label='Email')
    first_name = forms.CharField(max_length=100, required=True, label='Nombre')
    last_name = forms.CharField(max_length=100, required=True, label='Apellido')
    dni = forms.CharField(max_length=20, required=True, label='DNI')
    telefono = forms.CharField(max_length=30, required=False, label='Telefono')
    fecha_nacimiento = forms.DateField(
        required=True,
        label='Fecha de nacimiento',
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Usuario
        fields = ['email', 'first_name', 'last_name', 'dni', 'telefono', 'fecha_nacimiento']

    def clean_dni(self):
        """Valida que el DNI no este registrado."""
        dni = self.cleaned_data.get('dni')
        if Usuario.objects.filter(dni=dni).exists():
            raise ValidationError('Ya existe un usuario con este DNI.')
        return dni

    def clean_email(self):
        """Valida que el email no este registrado."""
        email = self.cleaned_data.get('email')
        if Usuario.objects.filter(email=email).exists():
            raise ValidationError('Ya existe un usuario con este email.')
        return email

    def save(self, commit=True):
        """Guarda el docente con estado pendiente de aprobacion."""
        usuario = super().save(commit=False)
        usuario.rol = Usuario.ROL_DOCENTE
        usuario.aprobado = False  # Pendiente de aprobacion

        if commit:
            usuario.save()

        return usuario


class LoginForm(AuthenticationForm):
    """
    Formulario de inicio de sesion.
    """

    username = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'autofocus': True}))


class PerfilForm(forms.ModelForm):
    """
    Formulario para editar el perfil de usuario.
    """

    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'email', 'telefono', 'fecha_nacimiento']
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
        }
