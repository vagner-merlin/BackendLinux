from django.contrib.auth.models import User , Group , Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import LogEntry
from .serializers import (
    UserSerializers , GroupSerializers , PermissionSerializers , ContentTypeSerializers,
    AdminLogSerializer,
)
from rest_framework import viewsets , permissions, status
from rest_framework.response import Response


# drf-spectacular is optional; if not installed, provide a no-op decorator.
try:
    from drf_spectacular.utils import extend_schema
except Exception:
    def extend_schema(*args, **kwargs):
        def _decorator(obj):
            return obj
        return _decorator


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


class AdminLogViewSet(viewsets.ReadOnlyModelViewSet):
    """API read-only que expone las entradas del log de administrador en el formato solicitado.

    GET /api/User/admin-log/  -> lista paginada por defecto (si DRF lo aplica)
    """
    queryset = LogEntry.objects.select_related('user', 'content_type').order_by('-action_time')
    serializer_class = AdminLogSerializer
    permission_classes = [permissions.AllowAny]

