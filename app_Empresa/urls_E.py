from django.urls import path , include
from rest_framework import routers
from app_Empresa.api_E import EmpresaViewSet

router = routers.DefaultRouter()
router.register(r'empresa', EmpresaViewSet)

urlpatterns = [
    path('', include(router.urls)),
]