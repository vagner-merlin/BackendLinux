from .models import Credito , Tipo_Credito
from .serializers import CreditoSerializer , TipoCreditoSerializer
from rest_framework import viewsets , permissions


class CreditoViewSet(viewsets.ModelViewSet):
    queryset = Credito.objects.all()
    serializer_class = CreditoSerializer
    permission_classes = [permissions.AllowAny]


class TipoCreditoViewSet(viewsets.ModelViewSet):
    queryset = Tipo_Credito.objects.all()
    serializer_class = TipoCreditoSerializer
    permission_classes = [permissions.AllowAny]
