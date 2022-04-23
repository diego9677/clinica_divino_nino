from django.urls import path
from django.views.generic import RedirectView
from .views import ReservaListView, ReservaCreateView

urlpatterns = [
    path('reservas/', ReservaListView.as_view(), name='reserva-list'),
    path('reservas-create/', ReservaCreateView.as_view(), name='reserva-create'),
    path('', RedirectView.as_view(pattern_name='reserva-list'), name='index')
]
