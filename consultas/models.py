from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from core.models import Paciente, Doctor, Usuario


class HistoriaClinica(models.Model):
    paciente = models.OneToOneField(Paciente, unique=True, related_name='historia_clinica', on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha Creación')
    activo = models.BooleanField(default=True, verbose_name='Activo')
    doctores = models.ManyToManyField(Doctor, related_name='historia_clinica', through='Consulta')

    def __str__(self):
        return str(self.pk)

    class Meta:
        db_table = 'historia_clinica'
        verbose_name = 'Historia Clinica'
        verbose_name_plural = 'Historias Clinicas'


class Consulta(models.Model):
    historia_clinica = models.ForeignKey(HistoriaClinica, related_name='consultas', on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    descripcion = models.TextField(verbose_name='Descripción')
    fecha_atencion = models.DateTimeField(verbose_name='Fecha Atención')
    hora_atencion = models.TimeField(verbose_name='Hora Atención')

    def __str__(self):
        return self.doctor.persona.nombres

    class Meta:
        db_table = 'consulta'
        verbose_name = 'Consulta'
        verbose_name_plural = 'Consultas'


class Factura(models.Model):
    consulta = models.OneToOneField(Consulta, related_name='factura', on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, related_name='facturas', on_delete=models.CASCADE)
    nit = models.CharField(max_length=20, verbose_name='Nit')
    fecha = models.DateTimeField(auto_now_add=True, verbose_name='Fecha')

    def __str__(self):
        return self.nit

    class Meta:
        db_table = 'factura'
        verbose_name = 'Factura'
        verbose_name_plural = 'Facturas'


class DetalleFactura(models.Model):
    factura = models.ForeignKey(Factura, related_name='detalle_factura', on_delete=models.CASCADE)
    descripcion = models.TextField(verbose_name='Descripción')
    precio = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Precio')

    def __str__(self):
        return self.descripcion

    class Meta:
        db_table = 'detalle_factura'
        verbose_name = 'Detalle de factura'
        verbose_name_plural = 'Detalle de facturas'


@receiver(post_save, sender=Paciente)
def crear_historia_clinica(sender, instance, **kwargs):
    print(instance)
