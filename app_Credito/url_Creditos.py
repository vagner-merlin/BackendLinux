from django.urls import path , include
from rest_framework.routers import DefaultRouter
from .api_rest import CreditoViewSet

router = DefaultRouter()
router.register(r'creditos', CreditoViewSet, basename='credito')

urlpatterns = [
    path('', include(router.urls)),
]
