from app_Empresa.serializers import EmpresaSerializer
from rest_framework import viewsets , permissions
from app_Empresa.models import Empresa

class EmpresaViewSet(viewsets.ModelViewSet):
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer
    permission_classes = [permissions.AllowAny]


