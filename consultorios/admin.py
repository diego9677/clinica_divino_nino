from django.contrib import admin
from .models import Consultorio, Piso, Asociacion, Turno


@admin.register(Turno)
class TurnoAdmin(admin.ModelAdmin):
    pass


@admin.register(Piso)
class PisoAdmin(admin.ModelAdmin):
    pass


@admin.register(Consultorio)
class ConsultorioAdmin(admin.ModelAdmin):
    pass


@admin.register(Asociacion)
class AsociacionAdmin(admin.ModelAdmin):
    pass

