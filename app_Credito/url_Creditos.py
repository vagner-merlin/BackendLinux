from django.urls import path , include
from rest_framework.routers import DefaultRouter
from .api_rest import CreditoViewSet , TipoCreditoViewSet

router = DefaultRouter()
router.register(r'creditos', CreditoViewSet, basename='credito')
router.register(r'tipo-creditos', TipoCreditoViewSet, basename='tipo-credito')

urlpatterns = [
    path('', include(router.urls)),
]
