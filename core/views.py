from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from .models import Doctor, Reserva, Persona
from .forms import ReservaForm, DoctorForm


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


class ReservaCreateView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    model = Reserva
    form_class = ReservaForm
    success_url = reverse_lazy('reserva-list')

    # def form_valid(self, form):
    #     reserva = form.save(commit=False)
    #     return super().form_valid(form)


class DoctorListView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = Doctor

    def get_queryset(self):
        word = self.request.GET.get('word', '')
        return Doctor.objects.select_related('persona').filter(
            Q(persona__nombres__icontains=word) | Q(persona__apellidos__icontains=word))


# class DoctorFormView(LoginRequiredMixin, FormView):
#     form_class = DoctorForm
#     template_name = 'core/doctor_form.html'
#     success_url = reverse_lazy('doctor-list')
#     initial = {}
#
#     def get_context_data(self, **kwargs):
#         pk = self.kwargs.get('pk', None)
#         context = super().get_context_data(**kwargs)
#         try:
#             doctor = Doctor.objects.get(pk=pk)
#             context['object'] = doctor
#         except Doctor.DoesNotExist:
#             pass
#         return context
#
#     def get_initial(self, **kwargs):
#         initial = super().get_initial()
#         pk = self.kwargs.get('pk', None)
#         try:
#             doctor = Doctor.objects.select_related('persona').get(pk=pk)
#             initial['pk'] = doctor.pk
#             initial['ci'] = doctor.persona.ci
#             initial['nombres'] = doctor.persona.nombres
#             initial['apellidos'] = doctor.persona.apellidos
#             initial['fecha_nacimiento'] = doctor.persona.fecha_nacimiento.isoformat()
#             initial['especialidad'] = doctor.especialidad
#             initial['cod_interno'] = doctor.cod_interno
#         except Doctor.DoesNotExist:
#             pass
#         return initial
#
#     def form_valid(self, form):
#         form.save()
#         return super().form_valid(form)


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
