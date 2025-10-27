from django.contrib.auth.models import User , Group , Permission
from django.contrib.contenttypes.models import ContentType
from .serializers import UserSerializers , GroupSerializers , PermissionSerializers , ContentTypeSerializers
from rest_framework import viewsets , permissions, status
from rest_framework.response import Response



class UserViewSer(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializers
    permission_classes = [permissions.AllowAny]

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all().order_by("id")
    serializer_class = GroupSerializers
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class PermissionViewSer(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializers
    permission_classes = [permissions.AllowAny]

class ContentTypeViewSer(viewsets.ModelViewSet):
    queryset = ContentType.objects.all()
    serializer_class = ContentTypeSerializers
    permission_classes = [permissions.AllowAny]

