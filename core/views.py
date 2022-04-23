from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views.generic import ListView, CreateView
from .models import Reserva
from .forms import ReservaForm


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
