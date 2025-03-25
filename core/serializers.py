from rest_framework import serializers
from .models import Cliente, Membresia, Asistencia

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'


class MembresiaSerializer(serializers.ModelSerializer):
    dias_restantes = serializers.SerializerMethodField()
    esta_activa = serializers.SerializerMethodField()

    class Meta:
        model = Membresia
        fields = '__all__'

    def get_dias_restantes(self, obj):
        return obj.dias_restantes()

    def get_esta_activa(self, obj):
        return obj.esta_activa()


class AsistenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asistencia
        fields = '__all__'
