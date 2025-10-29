from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.contrib.auth.models import User  , Group , Permission 
from django.contrib.contenttypes.models import ContentType

class UserSerializers(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class GroupSerializers(ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Group
        fields = ['id', 'name']
        
    def create(self, validated_data):
        group = Group.objects.create(name=validated_data['name'])
        return group

class PermissionSerializers(ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'


class ContentTypeSerializers(ModelSerializer):
    class Meta:
        model = ContentType
        fields = '__all__'


class AdminLogSerializer(serializers.Serializer):
    """Serializer de solo-lectura para mostrar los campos del LogEntry
    en el formato solicitado: usuario, tipo_contenido, objeto, accion (texto), mensaje y action_time.
    """
    id = serializers.IntegerField(read_only=True)
    usuario = serializers.CharField(source='user.username', read_only=True, allow_null=True)
    tipo_contenido = serializers.CharField(source='content_type.model', read_only=True, allow_null=True)
    objeto = serializers.CharField(source='object_repr', read_only=True, allow_null=True)
    accion = serializers.SerializerMethodField()
    mensaje = serializers.CharField(source='change_message', read_only=True, allow_null=True)
    action_time = serializers.DateTimeField(read_only=True)

    def get_accion(self, obj):
        """Mapea action_flag a un nombre legible en español."""
        mapping = {
            1: 'Adición',
            2: 'Cambio',
            3: 'Eliminación',
        }
        return mapping.get(getattr(obj, 'action_flag', None), getattr(obj, 'action_flag', None))