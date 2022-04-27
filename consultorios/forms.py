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
        fields = ['consultorio', 'doctor', 'turno']
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

    def clean_turno(self):
        turno = self.cleaned_data.get('turno')
        consultorio = self.cleaned_data.get('consultorio')
        if Asociacion.objects.filter(consultorio=consultorio, turno=turno).exists():
            raise forms.ValidationError('El consultorio esta ocupado.')
        return turno
