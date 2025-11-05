from .serializers import ClienteSerializer , DomicilioSerializer , TrabajoSerializer , DocumentacionSerializer
from .models import Cliente , Domicilio , Trabajo , Documentacion
from rest_framework import viewsets, permissions, status 

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = [permissions.AllowAny]

class DomicilioViewSet(viewsets.ModelViewSet):
    queryset = Domicilio.objects.all()
    serializer_class = DomicilioSerializer
    permission_classes = [permissions.AllowAny]

class TrabajoViewSet(viewsets.ModelViewSet):
    queryset = Trabajo.objects.all()
    serializer_class = TrabajoSerializer
    permission_classes = [permissions.AllowAny]

class DocumentacionViewSet(viewsets.ModelViewSet):
    queryset = Documentacion.objects.all()
    serializer_class = DocumentacionSerializer
    permission_classes = [permissions.AllowAny]

