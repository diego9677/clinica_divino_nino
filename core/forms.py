from django import forms
from django.db.models import Q
from .models import Persona, Reserva, Doctor, Especialidad, Paciente


class DatePickerInput(forms.DateInput):
    input_type = 'date'


class TimePickerInput(forms.TimeInput):
    input_type = 'time'


class DateTimePickerInput(forms.DateTimeInput):
    input_type = 'datetime'


class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['paciente', 'doctor', 'fecha_reserva', 'hora_reserva', 'activo']
        widgets = {
            'fecha_reserva': DatePickerInput(),
            'hora_reserva': TimePickerInput()
        }


class DoctorForm(forms.ModelForm):
    ci = forms.CharField(max_length=20, label='CI', required=True)
    nombres = forms.CharField(max_length=255, label='Nombres', required=True)
    apellidos = forms.CharField(max_length=255, label='Apellidos', required=True)
    fecha_nacimiento = forms.DateField(label='Fecha Nacimiento', widget=DatePickerInput(), required=True)

    class Meta:
        model = Doctor
        fields = ['ci', 'nombres', 'apellidos', 'fecha_nacimiento', 'especialidad', 'cod_interno']

    def clean_ci(self):
        ci = self.cleaned_data.get('ci')
        if Persona.objects.filter(Q(ci=ci) & ~Q(doctor__pk=self.instance.pk)).exists():
            raise forms.ValidationError('El ci ya se encuentra registrado')
        return ci


class PacienteForm(forms.ModelForm):
    ci = forms.CharField(max_length=20, label='CI', required=True)
    nombres = forms.CharField(max_length=255, label='Nombres', required=True)
    apellidos = forms.CharField(max_length=255, label='Apellidos', required=True)
    fecha_nacimiento = forms.DateField(label='Fecha Nacimiento', widget=DatePickerInput(), required=True)

    class Meta:
        model = Paciente
        fields = ['ci', 'nombres', 'apellidos', 'fecha_nacimiento']

    def clean_ci(self):
        ci = self.cleaned_data.get('ci')
        if Persona.objects.filter(Q(ci=ci) & ~Q(paciente__pk=self.instance.pk)).exists():
            raise forms.ValidationError('El ci ya se encuentra registrado')
        return ci
