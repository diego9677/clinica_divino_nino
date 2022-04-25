from django.db import models
from django.contrib.auth.models import AbstractUser


class Especialidad(models.Model):
    nombre = models.CharField(max_length=255, verbose_name='Nombre')
    descripcion = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Especialidad'
        verbose_name_plural = 'Especialidades'
        ordering = ['pk']


class Persona(models.Model):
    ci = models.CharField(max_length=20, unique=True, verbose_name='CI')
    nombres = models.CharField(max_length=255, verbose_name='Nombres')
    apellidos = models.CharField(max_length=255, verbose_name='Apellidos')
    fecha_nacimiento = models.DateField(verbose_name='Fecha de nacimiento')

    def __str__(self):
        return self.ci

    class Meta:
        verbose_name = 'Persona'
        verbose_name_plural = 'Personas'


class Usuario(AbstractUser):
    USERNAME_FIELD = 'username'

    persona = models.OneToOneField(Persona, unique=True, related_name='usuario', null=True, on_delete=models.CASCADE)


class Doctor(models.Model):
    persona = models.OneToOneField(Persona, unique=True, related_name='doctor', on_delete=models.CASCADE)
    especialidad = models.ForeignKey(Especialidad, related_name='doctores', on_delete=models.CASCADE)
    cod_interno = models.CharField(max_length=200, verbose_name='Codigo Interno')

    def __str__(self):
        return self.cod_interno

    class Meta:
        verbose_name = 'Doctor'
        verbose_name_plural = 'Doctores'


class Paciente(models.Model):
    persona = models.OneToOneField(Persona, unique=True, related_name='paciente', on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, related_name='Pacientes', on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    doctores = models.ManyToManyField(Doctor, related_name='pacientes', through='Reserva')

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name = 'Pacientes'
        verbose_name_plural = 'Pacientes'


class Reserva(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    fecha_reserva = models.DateField(verbose_name='Fecha Reserva')
    hora_reserva = models.TimeField(verbose_name='Hora Reserva')
    activo = models.BooleanField(default=True, verbose_name='Activo')

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'
