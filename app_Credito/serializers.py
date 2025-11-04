from rest_framework.serializers import ModelSerializer
from .models import Credito , Tipo_Credito


class CreditoSerializer(ModelSerializer):
    class Meta:
        model = Credito
        fields = '__all__'

class TipoCreditoSerializer(ModelSerializer):
    class Meta:
        model = Tipo_Credito
        fields = '__all__'
