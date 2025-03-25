from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from datetime import date
from django.utils.timezone import now
from .models import Cliente, Membresia, Asistencia
from django.db.models import Sum

class DashboardStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        hoy = date.today()
        mes_actual = hoy.month
        anio_actual = hoy.year

        total_clientes = Cliente.objects.count()
        membresias_activas = Membresia.objects.filter(
            fecha_inicio__lte=hoy,
            fecha_fin__gte=hoy
        ).count()
        asistencias_hoy = Asistencia.objects.filter(
            fecha_hora__date=hoy
        ).count()
        membresias_vencidas = Membresia.objects.filter(
            fecha_fin__lt=hoy
        ).count()
        ingresos_mes = Membresia.objects.filter(
            fecha_inicio__month=mes_actual,
            fecha_inicio__year=anio_actual
        ).aggregate(total=Sum('monto_pagado'))['total'] or 0

        return Response({
            "total_clientes": total_clientes,
            "membresias_activas": membresias_activas,
            "asistencias_hoy": asistencias_hoy,
            "membresias_vencidas": membresias_vencidas,
            "ingresos_mes": float(ingresos_mes),
        })
