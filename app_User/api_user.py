from django.contrib.auth.models import User , Group , Permission
from django.contrib.contenttypes.models import ContentType
from .serializers import UserSerializers , GroupSerializers , PermissionSerializers , ContentTypeSerializers
from rest_framework import viewsets , permissions



class UserViewSer(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializers
    permission_classes = [permissions.AllowAny]

class GroupViewSer(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializers
    permission_classes = [permissions.AllowAny]

class PermissionViewSer(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializers
    permission_classes = [permissions.AllowAny]

class ContentTypeViewSer(viewsets.ModelViewSet):
    queryset = ContentType.objects.all()
    serializer_class = ContentTypeSerializers
    permission_classes = [permissions.AllowAny]

