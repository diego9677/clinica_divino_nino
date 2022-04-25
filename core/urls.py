from django.urls import path
from django.views.generic import RedirectView
from .views import ReservaListView, ReservaCreateView, DoctorListView, DoctorCreateView, DoctorDeleteView, \
    DoctorUpdateView

urlpatterns = [
    path('doctores-update/<int:pk>/', DoctorUpdateView.as_view(), name='doctor-update'),
    path('doctores-delete/<int:pk>/', DoctorDeleteView.as_view(), name='doctor-delete'),
    path('doctores/', DoctorListView.as_view(), name='doctor-list'),
    path('doctores-create/', DoctorCreateView.as_view(), name='doctor-create'),
    path('reservas/', ReservaListView.as_view(), name='reserva-list'),
    path('reservas-create/', ReservaCreateView.as_view(), name='reserva-create'),
    path('', RedirectView.as_view(pattern_name='reserva-list'), name='index'),
]
