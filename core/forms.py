from django import forms
from .models import Reserva


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
