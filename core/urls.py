from django.urls import path
from django.views.generic import RedirectView
from .views import ReservaListView, DoctorListView, DoctorCreateView, DoctorDeleteView, \
    DoctorUpdateView, PacienteListView, PacienteCreateView, PacienteUpdateView, PacienteDeleteView, create_reserva, ReservaDeleteView

urlpatterns = [
    path('reservas-delete/<int:pk>/', ReservaDeleteView.as_view(), name='reserva-delete'),
    path('reservas-create/<int:paciente_id>/', create_reserva, name='reserva-create'),
    path('pacientes-update/<int:pk>/', PacienteUpdateView.as_view(), name='paciente-update'),
    path('pacientes-delete/<int:pk>/', PacienteDeleteView.as_view(), name='paciente-delete'),
    path('doctores-update/<int:pk>/', DoctorUpdateView.as_view(), name='doctor-update'),
    path('doctores-delete/<int:pk>/', DoctorDeleteView.as_view(), name='doctor-delete'),
    path('doctores/', DoctorListView.as_view(), name='doctor-list'),
    path('doctores-create/', DoctorCreateView.as_view(), name='doctor-create'),
    path('reservas/', ReservaListView.as_view(), name='reserva-list'),
    path('pacientes-create/', PacienteCreateView.as_view(), name='paciente-create'),
    path('pacientes-list/', PacienteListView.as_view(), name='paciente-list'),
    path('', RedirectView.as_view(pattern_name='reserva-list'), name='index'),
]

