from rest_framework.serializers import ModelSerializer
from app_Empresa.models import Empresa

class EmpresaSerializer(ModelSerializer):
    class Meta:
        model = Empresa
        fields = '__all__'

