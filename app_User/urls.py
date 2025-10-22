from django.urls import include , path
from rest_framework import routers
from .api_user import UserViewSer , GroupViewSer , PermissionViewSer , ContentTypeViewSer

router = routers.DefaultRouter()
router.register(r'user', UserViewSer)
router.register(r'group', GroupViewSer)
router.register(r'permission', PermissionViewSer)
router.register(r'content-type', ContentTypeViewSer)

urlpatterns = [
    path('', include(router.urls)),
]