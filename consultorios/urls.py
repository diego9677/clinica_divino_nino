from django.urls import path
from .views import ConsultorioListView, ConsultorioCreateView, ConsultorioUpdateView, ConsultorioDeleteView, \
    AsociacionCreateView, AsociacionDeleteView

urlpatterns = [
    path('asociacion/<int:consultorio_id>/', AsociacionCreateView.as_view(), name='asociacion-create'),
    path('asociacion/delete/<int:pk>/', AsociacionDeleteView.as_view(), name='asociacion-delete'),
    path('editar/<int:pk>/', ConsultorioUpdateView.as_view(), name='consultorio-update'),
    path('eliminar/<int:pk>/', ConsultorioDeleteView.as_view(), name='consultorio-delete'),
    path('crear/', ConsultorioCreateView.as_view(), name='consultorio-create'),
    path('', ConsultorioListView.as_view(), name='consultorio-list'),
]
