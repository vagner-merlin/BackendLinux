from app_Empresa.serializers import EmpresaSerializer, RegisterEmpresaUserSerializer, LoginSerializer, LogoutSerializer, SuscripcionSerializer , OnPremiseSerializer , ConfiguracionSerializer
from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from app_Empresa.models import Empresa, Suscripcion , on_premise , Configuracion

class ConfiguracionViewSet(viewsets.ModelViewSet):
    queryset = Configuracion.objects.all()
    serializer_class = ConfiguracionSerializer
    permission_classes = [permissions.AllowAny]

class EmpresaViewSet(viewsets.ModelViewSet):
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer
    permission_classes = [permissions.AllowAny]

class OnPremiseViewSet(viewsets.ModelViewSet):
    queryset = on_premise.objects.all()
    serializer_class = OnPremiseSerializer
    permission_classes = [permissions.AllowAny]


class SuscripcionViewSet(viewsets.ModelViewSet):
    queryset = Suscripcion.objects.all()
    serializer_class = SuscripcionSerializer
    permission_classes = [permissions.AllowAny]


class RegisterView(APIView):
    """
    API independiente para registrar empresa, usuario y perfil en una sola petición
    """
    permission_classes = [permissions.AllowAny]
    parser_classes = [JSONParser, FormParser, MultiPartParser]
    
    def post(self, request):
        serializer = RegisterEmpresaUserSerializer(data=request.data)
        
        if serializer.is_valid():
            try:
                result = serializer.save()
                
                response_data = {
                    'message': 'Registro exitoso',
                    'empresa': {
                        'id': result['empresa'].id,
                        'razon_social': result['empresa'].razon_social,
                        'email_contacto': result['empresa'].email_contacto,
                        'nombre_comercial': result['empresa'].nombre_comercial,
                        'fecha_registro': result['empresa'].fecha_registro,
                        'activo': result['empresa'].activo,
                        'imagen_url': result['empresa'].Imagen_url,
                    },
                    'user': {
                        'id': result['user'].id,
                        'username': result['user'].username,
                        'first_name': result['user'].first_name,
                        'last_name': result['user'].last_name,
                        'email': result['user'].email,
                        'date_joined': result['user'].date_joined,
                        'is_superuser': result['user'].is_superuser,
                    },
                    'perfil_user': {
                        'id': result['perfil_user'].id,
                        'empresa_id': result['perfil_user'].empresa.id,
                        'usuario_id': result['perfil_user'].usuario.id,
                        'imagen_url': result['perfil_user'].imagen_url,
                    },
                    'token': result['token']
                }
                
                return Response(response_data, status=status.HTTP_201_CREATED)
                
            except Exception as e:
                return Response(
                    {'error': f'Error interno del servidor: {str(e)}'}, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        else:
            return Response(
                {'errors': serializer.errors}, 
                status=status.HTTP_400_BAD_REQUEST
            )


class LoginView(APIView):
    """
    API para login con email y password, devuelve token
    """
    permission_classes = [permissions.AllowAny]
    parser_classes = [JSONParser, FormParser, MultiPartParser]
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        
        if serializer.is_valid():
            try:
                result = serializer.save()
                
                response_data = {
                    'message': 'Login exitoso',
                    'token': result['token'],
                    'user_id': result['user_id'],
                    'email': result['email'],
                    'is_superuser': result['is_superuser'],
                    'empresa_id': result['empresa_id'],
                    'empresa_nombre': result['empresa_nombre']
                }
                
                return Response(response_data, status=status.HTTP_200_OK)
                
            except Exception as e:
                return Response(
                    {'error': f'Error interno del servidor: {str(e)}'}, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        else:
            return Response(
                {'errors': serializer.errors}, 
                status=status.HTTP_400_BAD_REQUEST
            )


class LogoutView(APIView):
    """
    API para logout, elimina el token
    """
    permission_classes = [permissions.AllowAny]
    parser_classes = [JSONParser, FormParser, MultiPartParser]
    
    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        
        if serializer.is_valid():
            try:
                result = serializer.save()
                return Response(
                    {'message': 'Logout exitoso'}, 
                    status=status.HTTP_200_OK
                )
                
            except Exception as e:
                return Response(
                    {'error': f'Error interno del servidor: {str(e)}'}, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        else:
            return Response(
                {'errors': serializer.errors}, 
                status=status.HTTP_400_BAD_REQUEST
            )


