from django.contrib import admin
from .models import HistoriaClinica, Consulta, Factura, DetalleFactura 

@admin.register(HistoriaClinica)
class HistoriaClinicaAdmin(admin.ModelAdmin):
    pass


@admin.register(Consulta)
class ConsultaAdmin(admin.ModelAdmin):
    pass


@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    pass

@admin.register(DetalleFactura)
class DetalleFacturaAdmin(admin.ModelAdmin):
    pass
