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
        return Consultorio.objects.filter(nombre__icontains=word)


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

    def get_initial(self):
        initial = {}
        try:
            initial['consultorio'] = Consultorio.objects.get(pk=self.kwargs.get('pk'))
        except Consultorio.DoesNotExist:
            pass
        return initial

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
