from django.contrib import admin
from .models import Consultorio, Piso, Asociacion


@admin.register(Piso)
class PisoAdmin(admin.ModelAdmin):
    pass


@admin.register(Consultorio)
class ConsultorioAdmin(admin.ModelAdmin):
    pass


@admin.register(Asociacion)
class AsociacionAdmin(admin.ModelAdmin):
    pass

