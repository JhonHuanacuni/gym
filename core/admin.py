from django.contrib import admin
from .models import Cliente, Membresia, Asistencia, Administrador
from django.contrib.auth.admin import UserAdmin

""" admin.site.register(Administrador) """

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombres', 'apellidos', 'dni', 'email', 'telefono', 'fecha_registro')
    search_fields = ('dni', 'nombres', 'apellidos')
    list_filter = ('fecha_registro',)


@admin.register(Membresia)
class MembresiaAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'fecha_inicio', 'fecha_fin', 'monto_pagado', 'dias_restantes', 'esta_activa')
    list_filter = ('fecha_inicio', 'fecha_fin')
    search_fields = ('cliente__nombres', 'cliente__apellidos')


@admin.register(Asistencia)
class AsistenciaAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'fecha_hora')
    list_filter = ('fecha_hora',)
    search_fields = ('cliente__dni', 'cliente__nombres', 'cliente__apellidos')


@admin.register(Administrador)
class AdministradorAdmin(UserAdmin):
    pass  # usa la gestión por defecto de usuarios de Django
