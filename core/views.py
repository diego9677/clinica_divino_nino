from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from datetime import datetime, timedelta
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from .models import Doctor, Reserva, Persona, Paciente, Especialidad
from .forms import ReservaForm, DoctorForm, PacienteForm


def add_minutes(dt, time_add):
    date = datetime(100, 1, 1, dt.hour, dt.minute, dt.second)
    return (date + timedelta(minutes=time_add)).time()


class ReservaListView(LoginRequiredMixin, ListView):
    # login required
    login_url = reverse_lazy('login')
    # list view
    model = Reserva

    def get_queryset(self):
        word = self.request.GET.get('word', '')
        return Reserva.objects.select_related('paciente', 'doctor').filter(
            Q(paciente__persona__nombres__icontains=word) | Q(paciente__persona__apellidos__icontains=word) | Q(
                doctor__persona__nombres__icontains=word) | Q(paciente__persona__apellidos__icontains=word))


class DoctorListView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = Doctor

    def get_queryset(self):
        word = self.request.GET.get('word', '')
        return Doctor.objects.select_related('persona').filter(
            Q(persona__nombres__icontains=word) | Q(persona__apellidos__icontains=word))


class DoctorDeleteView(LoginRequiredMixin, DeleteView):
    model = Doctor
    success_url = reverse_lazy('doctor-list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.persona.delete()
        self.object.delete()
        return HttpResponseRedirect(success_url)


class DoctorCreateView(LoginRequiredMixin, CreateView):
    model = Doctor
    form_class = DoctorForm
    success_url = reverse_lazy('doctor-list')

    def form_valid(self, form):
        persona = Persona()
        persona.ci = form.cleaned_data.get('ci')
        persona.nombres = form.cleaned_data.get('nombres')
        persona.apellidos = form.cleaned_data.get('apellidos')
        persona.fecha_nacimiento = form.cleaned_data.get('fecha_nacimiento')
        persona.save()
        doctor = form.save(commit=False)
        doctor.persona = persona
        doctor.save()
        return super().form_valid(form)


class DoctorUpdateView(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    model = Doctor
    form_class = DoctorForm
    initial = {}
    success_url = reverse_lazy('doctor-list')

    def get_initial(self):
        initial = super().get_initial()
        doctor = self.get_object()
        initial['ci'] = doctor.persona.ci
        initial['nombres'] = doctor.persona.nombres
        initial['apellidos'] = doctor.persona.apellidos
        initial['fecha_nacimiento'] = doctor.persona.fecha_nacimiento.isoformat()
        return initial

    def form_valid(self, form):
        doctor = form.save(commit=False)
        doctor.persona.ci = form.cleaned_data.get('ci')
        doctor.persona.nombres = form.cleaned_data.get('nombres')
        doctor.persona.apellidos = form.cleaned_data.get('apellidos')
        doctor.persona.fecha_nacimiento = form.cleaned_data.get('fecha_nacimiento')
        doctor.persona.save()
        doctor.save()
        return super().form_valid(form)


class PacienteListView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = Paciente

    def get_queryset(self):
        word = self.request.GET.get('word', '')
        queryset = Paciente.objects.filter(Q(persona__nombres__icontains=word) | Q(persona__apellidos__icontains=word))
        return queryset


class PacienteCreateView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    model = Paciente
    form_class = PacienteForm
    success_url = reverse_lazy('paciente-list')

    def form_valid(self, form):
        persona = Persona()
        persona.ci = form.cleaned_data.get('ci')
        persona.nombres = form.cleaned_data.get('nombres')
        persona.apellidos = form.cleaned_data.get('apellidos')
        persona.fecha_nacimiento = form.cleaned_data.get('fecha_nacimiento')
        persona.save()
        paciente = form.save(commit=False)
        paciente.persona = persona
        paciente.usuario = self.request.user
        paciente.save()
        return super().form_valid(form)


class PacienteUpdateView(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    model = Paciente
    form_class = PacienteForm
    initial = {}
    success_url = reverse_lazy('paciente-list')

    def get_initial(self):
        initial = super().get_initial()
        paciente = self.get_object()
        initial['ci'] = paciente.persona.ci
        initial['nombres'] = paciente.persona.nombres
        initial['apellidos'] = paciente.persona.apellidos
        initial['fecha_nacimiento'] = paciente.persona.fecha_nacimiento.isoformat()
        return initial

    def form_valid(self, form):
        paciente = form.save(commit=False)
        paciente.persona.ci = form.cleaned_data.get('ci')
        paciente.persona.nombres = form.cleaned_data.get('nombres')
        paciente.persona.apellidos = form.cleaned_data.get('apellidos')
        paciente.persona.fecha_nacimiento = form.cleaned_data.get('fecha_nacimiento')
        paciente.persona.save()
        paciente.save()
        return super().form_valid(form)


class PacienteDeleteView(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    model = Paciente
    success_url = reverse_lazy('paciente-list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.persona.delete()
        self.object.delete()
        return HttpResponseRedirect(success_url)


def get_cupos(doctor, fecha):
    cupos = []
    for asociacion in doctor.asociacion_set.all():
        hora_current = asociacion.turno.hora_inicio
        hora_fin = asociacion.turno.hora_fin
        tiempo_min = asociacion.turno.tiempo_min
        turno_cupos = {'turno': asociacion.turno.nombre, 'cupos': []}
        cont = 0
        while hora_current < hora_fin:
            cont += 1
            active = True
            if Reserva.objects.filter(doctor=doctor, fecha_reserva=fecha, hora_reserva=hora_current).exists():
                active = False
            turno_cupos['cupos'].append(
                {'id': f'cupo_{cont}', 'nombre': f'Cupo {cont}', 'value': hora_current, 'active': active})
            hora_current = add_minutes(hora_current, tiempo_min)
        cupos.append(turno_cupos)
    return cupos


def create_reserva(request, paciente_id):
    context = {}
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            paciente = form.cleaned_data.get('paciente')
            fecha_reserva = form.cleaned_data.get('fecha_reserva')
            if Reserva.objects.filter(paciente=paciente, fecha_reserva=fecha_reserva).exists():
                messages.error(request, 'El paciente ya tiene una reserva pendiente')
                return redirect(reverse_lazy('reserva-create', kwargs={'paciente_id': paciente_id}))
            form.save()
            return redirect(reverse_lazy('reserva-list'))
        return render(request, 'core/reserva_form.html', {'form': form})
    especialidad_id = request.GET.get('especialidad', None)
    doctor_id = request.GET.get('doctor', None)
    fecha = request.GET.get('fecha', None)
    paciente = get_object_or_404(Paciente, pk=paciente_id)
    especialidades = Especialidad.objects.all()
    if especialidad_id:
        doctores = Doctor.objects.filter(especialidad_id=especialidad_id)
    else:
        doctores = Doctor.objects.all()
    context['doctores'] = doctores
    context['especialidades'] = especialidades
    if not doctor_id:
        return render(request, 'core/reserva_form.html', context)
    doctor = get_object_or_404(Doctor, pk=doctor_id)
    cupos = get_cupos(doctor, fecha)
    form = ReservaForm(initial={'doctor': doctor, 'paciente': paciente, 'fecha_reserva': fecha})
    context['form'] = form
    context['cupos'] = cupos
    return render(request, 'core/reserva_form.html', context)
