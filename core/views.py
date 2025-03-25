from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Cliente, Membresia, Asistencia
from .serializers import ClienteSerializer, MembresiaSerializer, AsistenciaSerializer

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer


class MembresiaViewSet(viewsets.ModelViewSet):
    queryset = Membresia.objects.all()
    serializer_class = MembresiaSerializer

    @action(detail=True, methods=['get'], url_path='dias-restantes')
    def dias_restantes(self, request, pk=None):
        membresia = self.get_object()
        return Response({
            'cliente': str(membresia.cliente),
            'dias_restantes': membresia.dias_restantes(),
            'esta_activa': membresia.esta_activa()
        })
        
    @action(detail=False, methods=['get'], url_path='activa-por-dni')
    def activa_por_dni(self, request):
        dni = request.query_params.get('dni')

        if not dni:
            return Response({'error': 'Debe proporcionar un DNI'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            cliente = Cliente.objects.get(dni=dni)
        except Cliente.DoesNotExist:
            return Response({'error': 'Cliente no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        membresia = Membresia.objects.filter(cliente=cliente).order_by('-fecha_fin').first()

        if not membresia or not membresia.esta_activa():
            return Response({'mensaje': 'No tiene una membresía activa'}, status=status.HTTP_200_OK)

        serializer = self.get_serializer(membresia)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'], url_path='historial-por-dni')
    def historial_por_dni(self, request):
        dni = request.query_params.get('dni')

        if not dni:
            return Response({'error': 'Debe proporcionar un DNI'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            cliente = Cliente.objects.get(dni=dni)
        except Cliente.DoesNotExist:
            return Response({'error': 'Cliente no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        historial = Membresia.objects.filter(cliente=cliente).order_by('-fecha_inicio')
        serializer = self.get_serializer(historial, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AsistenciaViewSet(viewsets.ModelViewSet):
    queryset = Asistencia.objects.all()
    serializer_class = AsistenciaSerializer

    @action(detail=False, methods=['post'], url_path='registrar-por-dni')
    def registrar_por_dni(self, request):
        dni = request.data.get('dni')

        if not dni:
            return Response({'error': 'DNI es requerido'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            cliente = Cliente.objects.get(dni=dni)
        except Cliente.DoesNotExist:
            return Response({'error': 'Cliente no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        # Buscar membresía activa
        membresia = Membresia.objects.filter(cliente=cliente).order_by('-fecha_fin').first()

        if not membresia or not membresia.esta_activa():
            return Response(
                {'error': 'El cliente no tiene una membresía activa. No se puede registrar la asistencia.'},
                status=status.HTTP_403_FORBIDDEN
            )

        # Registrar asistencia
        asistencia = Asistencia.objects.create(cliente=cliente)
        serializer = self.get_serializer(asistencia)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

