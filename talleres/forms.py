"""
Formularios del modulo de talleres.
"""

from django import forms
from .models import Taller, Horario


class TallerForm(forms.ModelForm):
    """
    Formulario para crear y editar talleres.
    """

    class Meta:
        model = Taller
        fields = ['nombre', 'descripcion', 'docente', 'cupo', 'cuota_mensual', 'activo']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_cupo(self):
        """Valida que el cupo sea mayor a 0."""
        cupo = self.cleaned_data.get('cupo')
        if cupo <= 0:
            raise forms.ValidationError('El cupo debe ser mayor a 0.')
        return cupo

    def clean_cuota_mensual(self):
        """Valida que la cuota mensual no sea negativa."""
        cuota = self.cleaned_data.get('cuota_mensual')
        if cuota < 0:
            raise forms.ValidationError('La cuota mensual no puede ser negativa.')
        return cuota


class HorarioForm(forms.ModelForm):
    """
    Formulario para crear y editar horarios.
    """

    class Meta:
        model = Horario
        fields = ['taller', 'dia_semana', 'hora_inicio', 'hora_fin']

    def clean(self):
        """Valida que la hora de inicio sea anterior a la hora de fin."""
        cleaned_data = super().clean()
        hora_inicio = cleaned_data.get('hora_inicio')
        hora_fin = cleaned_data.get('hora_fin')

        if hora_inicio and hora_fin:
            if hora_inicio >= hora_fin:
                raise forms.ValidationError('La hora de inicio debe ser anterior a la hora de fin.')

        return cleaned_data
