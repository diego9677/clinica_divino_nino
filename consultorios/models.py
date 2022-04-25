from django.db import models
from core.models import Especialidad, Doctor

ESTADO_CHOICES = (
    ('a', 'Activo'),
    ('i', 'Inactivo')
)


class Piso(models.Model):
    nombre = models.CharField(max_length=255, verbose_name='Nombre')
    descripcion = models.TextField(blank=True, null=True, verbose_name='Descripción')

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Piso'
        verbose_name_plural = 'Pisos'
        ordering = ['pk']


class Consultorio(models.Model):
    piso = models.ForeignKey(Piso, related_name='consultorios', on_delete=models.CASCADE)
    especialidad = models.ForeignKey(Especialidad, related_name='consultorios', on_delete=models.CASCADE)
    nombre = models.CharField(max_length=255, verbose_name='Nombre')
    estado = models.CharField(max_length=2, choices=ESTADO_CHOICES)
    doctores = models.ManyToManyField(Doctor, related_name='consultorios', through='Asociacion')

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Consultorio'
        verbose_name_plural = 'Consultorios'


class Asociacion(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    consultorio = models.ForeignKey(Consultorio, on_delete=models.CASCADE)
    hora_inicio = models.TimeField(verbose_name='Hora Inicio')
    hora_fin = models.TimeField(verbose_name='Hora Fin')

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name = 'Asociacion'
        verbose_name_plural = 'Asociacones'
