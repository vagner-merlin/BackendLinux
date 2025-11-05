from django.urls import path , include  
from . import views
from rest_framework import routers
from .api_cliente import ClienteViewSet, DocumentacionViewSet , DomicilioViewSet ,TrabajoViewSet 

router = routers.DefaultRouter()
router.register(r'clientes', ClienteViewSet)
router.register(r'documentacion', DocumentacionViewSet)
router.register(r'domicilios', DomicilioViewSet)
router.register(r'trabajo', TrabajoViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 
