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
