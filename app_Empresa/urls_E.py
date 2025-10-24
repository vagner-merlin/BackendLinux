from django.urls import path , include
from rest_framework import routers
from app_Empresa.api_E import EmpresaViewSet, SuscripcionViewSet, RegisterView, LoginView, LogoutView , OnPremiseViewSet , ConfiguracionViewSet
 
 
router = routers.DefaultRouter()
router.register(r'empresa', EmpresaViewSet)
router.register(r'suscripcion', SuscripcionViewSet)
router.register(r'on-premise', OnPremiseViewSet)
router.register(r'configuracion', ConfiguracionViewSet)

urlpatterns = [
    path('', include(router.urls)),

    path('register/empresa-user/', RegisterView.as_view(), name='register'),

    path('auth/login/', LoginView.as_view(), name='login'),
 
    path('auth/logout/', LogoutView.as_view(), name='logout'),



#aa