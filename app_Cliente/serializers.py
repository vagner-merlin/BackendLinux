from rest_framework.serializers import ModelSerializer, Serializer
from .models import Cliente , Documentacion , Trabajo , Domicilio

class ClienteSerializer(ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'

class DocumentacionSerializer(ModelSerializer):
    class Meta:
        model = Documentacion
        fields = '__all__'

class TrabajoSerializer(ModelSerializer):
    class Meta:
        model = Trabajo
        fields = '__all__'

class DomicilioSerializer(ModelSerializer):
    class Meta:
        model = Domicilio
        fields = '__all__'

