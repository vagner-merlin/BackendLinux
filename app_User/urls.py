from django.urls import include , path
from rest_framework import routers
<<<<<<< HEAD
from .api_user import UserViewSer , GroupViewSet , PermissionViewSer , ContentTypeViewSer, AdminLogViewSet
=======
from .api_user import UserViewSer , GroupViewSet , PermissionViewSer , ContentTypeViewSer
>>>>>>> a7d45e8 (api crada correctamente)

router = routers.DefaultRouter()
router.register(r'user', UserViewSer)
router.register(r'group', GroupViewSet)
router.register(r'permission', PermissionViewSer)
router.register(r'content-type', ContentTypeViewSer)
router.register(r'admin-log', AdminLogViewSet, basename='admin-log')

urlpatterns = [
    path('', include(router.urls)),
]