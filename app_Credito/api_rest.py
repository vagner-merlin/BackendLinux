from .models import Credito
from .serializers import CreditoSerializer
from rest_framework import viewsets , permissions


class CreditoViewSet(viewsets.ModelViewSet):
    queryset = Credito.objects.all()
    serializer_class = CreditoSerializer
    permission_classes = [permissions.AllowAny]

