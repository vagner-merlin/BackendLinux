from app_Empresa.serializers import EmpresaSerializer, RegisterEmpresaUserSerializer, LoginSerializer, LogoutSerializer, SuscripcionSerializer , OnPremiseSerializer
from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from app_Empresa.models import Empresa, Suscripcion , on_premise

class EmpresaViewSet(viewsets.ModelViewSet):
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer
    permission_classes = [permissions.AllowAny]

class OnPremiseViewSet(viewsets.ModelViewSet):
    queryset = on_premise.objects.all()
    serializer_class = OnPremiseSerializer
    permission_classes = [permissions.AllowAny]


class SuscripcionViewSet(viewsets.ModelViewSet):
    """
    ViewSet completo para CRUD de Suscripciones
    
    Operaciones disponibles:
    - GET /api/suscripcion/ - Listar todas las suscripciones
    - POST /api/suscripcion/ - Crear nueva suscripción
    - GET /api/suscripcion/{id}/ - Obtener suscripción específica
    - PUT /api/suscripcion/{id}/ - Actualizar suscripción completa
    - PATCH /api/suscripcion/{id}/ - Actualizar parcialmente suscripción
    - DELETE /api/suscripcion/{id}/ - Eliminar suscripción
    """
    queryset = Suscripcion.objects.all().select_related('empresa')
    serializer_class = SuscripcionSerializer
    permission_classes = [permissions.AllowAny]  # Cambiar según tus necesidades de autenticación
    
    def get_queryset(self):
        """Personalizar queryset - opcional: filtrar por empresa del usuario"""
        queryset = Suscripcion.objects.all().select_related('empresa')
        
        # Opcional: Filtrar por empresa si se pasa como parámetro
        empresa_id = self.request.query_params.get('empresa_id')
        if empresa_id:
            queryset = queryset.filter(empresa_id=empresa_id)
            
        # Opcional: Filtrar por estado
        estado = self.request.query_params.get('estado')
        if estado:
            queryset = queryset.filter(enum_estado=estado)
            
        return queryset
    
    def create(self, request, *args, **kwargs):
        """Personalizar creación de suscripción"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Verificar si la empresa ya tiene una suscripción activa (opcional)
        empresa_id = serializer.validated_data.get('empresa').id
        suscripcion_activa = Suscripcion.objects.filter(
            empresa_id=empresa_id, 
            activo=True
        ).exists()
        
        if suscripcion_activa:
            return Response(
                {'error': 'La empresa ya tiene una suscripción activa'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        
        return Response(
            {
                'message': 'Suscripción creada exitosamente',
                'data': serializer.data
            }, 
            status=status.HTTP_201_CREATED, 
            headers=headers
        )
    
    def update(self, request, *args, **kwargs):
        """Personalizar actualización"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response(
            {
                'message': 'Suscripción actualizada exitosamente',
                'data': serializer.data
            }
        )
    
    def destroy(self, request, *args, **kwargs):
        """Personalizar eliminación"""
        instance = self.get_object()
        self.perform_destroy(instance)
        
        return Response(
            {'message': 'Suscripción eliminada exitosamente'}, 
            status=status.HTTP_200_OK
        )

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


