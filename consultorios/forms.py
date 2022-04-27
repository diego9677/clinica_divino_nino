from django import forms
from core.forms import TimePickerInput
from .models import Consultorio, Asociacion, Doctor


class ConsultorioForm(forms.ModelForm):
    class Meta:
        model = Consultorio
        fields = ['piso', 'especialidad', 'nombre', 'estado']


class AsociacionForm(forms.ModelForm):
    class Meta:
        model = Asociacion
        fields = ['consultorio', 'doctor', 'hora_inicio', 'hora_fin']
        widgets = {
            'hora_inicio': TimePickerInput(),
            'hora_fin': TimePickerInput()
        }

    def __init__(self, *args, **kwargs):
        super(AsociacionForm, self).__init__(*args, **kwargs)
        consultorio = self.initial.get('consultorio')
        self.fields['doctor'] = forms.ModelChoiceField(
            queryset=Doctor.objects.filter(especialidad=consultorio.especialidad))

    def clean_doctor(self):
        doctor = self.cleaned_data.get('doctor')
        consultorio = self.cleaned_data.get('consultorio')
        if Asociacion.objects.filter(doctor=doctor, consultorio=consultorio).exists():
            raise forms.ValidationError('El doctor ya esta asociado')
        return doctor

    def clean_hora_inicio(self):
        hora_inicio = self.cleaned_data.get('hora_inicio')
        consultorio = self.cleaned_data.get('consultorio')
        if Asociacion.objects.filter(consultorio=consultorio, hora_fin__gte=hora_inicio).exists():
            raise forms.ValidationError('El consultorio esta ocupado.')
        return hora_inicio

    def clean_hora_fin(self):
        hora_inicio = self.cleaned_data.get('hora_inicio')
        hora_fin = self.cleaned_data.get('hora_fin')
        # consultorio = self.cleaned_data.get('consultorio')
        if hora_inicio and hora_fin <= hora_inicio:
            raise forms.ValidationError('Hora fin incorrecta')
        return hora_fin
