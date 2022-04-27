from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Consultorio, Asociacion
from .forms import ConsultorioForm, AsociacionForm


class ConsultorioListView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = Consultorio

    def get_queryset(self):
        word = self.request.GET.get('word', '')
        queryset = Consultorio.objects.filter(nombre__icontains=word)
        return queryset


class ConsultorioCreateView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    model = Consultorio
    form_class = ConsultorioForm
    success_url = reverse_lazy('consultorio-list')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class ConsultorioUpdateView(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    model = Consultorio
    form_class = ConsultorioForm
    success_url = reverse_lazy('consultorio-list')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class ConsultorioDeleteView(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    model = Consultorio
    success_url = reverse_lazy('consultorio-list')


class AsociacionCreateView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    model = Asociacion
    form_class = AsociacionForm
    initial = {}

    def get_success_url(self):
        return reverse_lazy('asociacion-create', kwargs={'consultorio_id': self.kwargs.get('consultorio_id')})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            consultorio = Consultorio.objects.get(pk=self.kwargs.get('consultorio_id'))
            context['consultorio'] = consultorio
            context['asociaciones'] = Asociacion.objects.filter(consultorio=consultorio)
        except Consultorio.DoesNotExist:
            pass
        return context

    def get_initial(self):
        initial = {}
        try:
            initial['consultorio'] = Consultorio.objects.get(pk=self.kwargs.get('consultorio_id'))
        except Consultorio.DoesNotExist:
            pass
        return initial

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class AsociacionDeleteView(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    model = Asociacion

    def get_success_url(self):
        self.object = self.get_object()
        return reverse_lazy('asociacion-create', kwargs={'consultorio_id': self.object.consultorio.id})
