from django.db import models
from core.models import Paciente, Doctor, Usuario


class HistoriaClinica(models.Model):
    paciente = models.ForeignKey(Paciente, related_name='historia_clinica', on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha Creación')
    activo = models.BooleanField(default=True, verbose_name='Activo')
    doctores = models.ManyToManyField(Doctor, related_name='historia_clinica', through='Consulta')

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name = 'Historia Clinica'
        verbose_name_plural = 'Historias Clinicas'


class Consulta(models.Model):
    historia_clinica = models.ForeignKey(HistoriaClinica, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    descripcion = models.TextField(verbose_name='Descripción')
    fecha_atencion = models.DateTimeField(verbose_name='Fecha Atención')
    hora_atencion = models.TimeField(verbose_name='Hora Atención')


class Factura(models.Model):
    consulta = models.OneToOneField(Consulta, related_name='factura', on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, related_name='facturas', on_delete=models.CASCADE)
    nit = models.CharField(max_length=20, verbose_name='Nit')
    fecha = models.DateTimeField(auto_now_add=True, verbose_name='Fecha')


class DetalleFactura(models.Model):
    factura = models.ForeignKey(Factura, related_name='detalle_factura', on_delete=models.CASCADE)
    descripcion = models.TextField(verbose_name='Descripción')
    precio = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Precio')
