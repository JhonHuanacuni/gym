from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date

class Administrador(AbstractUser):
    # Puedes extender más adelante con otros campos
    pass


class Cliente(models.Model):
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    dni = models.CharField(max_length=10, unique=True)
    email = models.EmailField(blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    fecha_registro = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.apellidos}, {self.nombres}"


class Membresia(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    monto_pagado = models.DecimalField(max_digits=8, decimal_places=2)

    def dias_restantes(self):
        hoy = date.today()
        return (self.fecha_fin - hoy).days

    def esta_activa(self):
        hoy = date.today()
        return self.fecha_inicio <= hoy <= self.fecha_fin

    def __str__(self):
        return f"Membresía de {self.cliente} ({self.fecha_inicio} - {self.fecha_fin})"


class Asistencia(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha_hora = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Asistencia - {self.cliente} - {self.fecha_hora.strftime('%Y-%m-%d %H:%M')}"
