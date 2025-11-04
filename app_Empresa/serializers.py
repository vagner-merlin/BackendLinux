from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework import serializers
from app_Empresa.models import Empresa, Suscripcion , on_premise
from django.contrib.auth.models import User
from app_User.models import Perfiluser
from django.contrib.auth.hashers import make_password
from rest_framework.authtoken.models import Token
from django.db import transaction
from django.contrib.auth import authenticate
from datetime import timedelta
from django.utils import timezone
from .models import Configuracion 

class ConfiguracionSerializer(ModelSerializer):
    class Meta:
        model = Configuracion
        fields = '__all__'



class EmpresaSerializer(ModelSerializer):
    class Meta:
        model = Empresa
        fields = '__all__'

class OnPremiseSerializer(ModelSerializer):
    class Meta:
        model = on_premise
        fields = '__all__'



class SuscripcionSerializer(ModelSerializer):
    # Mostrar información de la empresa en las consultas GET
    empresa_info = serializers.SerializerMethodField(read_only=True)
    # Hacer fecha_fin de solo lectura para que se calcule automáticamente
    fecha_fin = serializers.DateTimeField(read_only=True)
    
    class Meta:
        model = Suscripcion
        fields = '__all__'
        
    def get_empresa_info(self, obj):
        return {
            'id': obj.empresa.id,
            'razon_social': obj.empresa.razon_social,
            'nombre_comercial': obj.empresa.nombre_comercial
        }
    
    def validate_empresa(self, value):
        """Validar que la empresa existe y está activa"""
        if not value.activo:
            raise serializers.ValidationError("La empresa debe estar activa para crear una suscripción")
        return value
    
    def create(self, validated_data):
        """Crear suscripción con fecha_fin automática (fecha_inicio + 30 días)"""
        # La fecha_inicio se crea automáticamente por auto_now_add=True en el modelo
        # Pero necesitamos calcular fecha_fin antes de guardar
        
        # Crear la instancia sin guardar
        suscripcion = Suscripcion(**validated_data)
        
        # Calcular fecha_fin: fecha_inicio + 30 días
        if not suscripcion.fecha_inicio:
            suscripcion.fecha_inicio = timezone.now()
        
        suscripcion.fecha_fin = suscripcion.fecha_inicio + timedelta(days=30)
        
        # Ahora sí guardar
        suscripcion.save()
        
        return suscripcion

class RegisterEmpresaUserSerializer(Serializer):
    # Campos de Empresa
    razon_social = serializers.CharField(max_length=255)
    email_contacto = serializers.EmailField()
    nombre_comercial = serializers.CharField(max_length=255)
    imagen_url_empresa = serializers.URLField(required=False, allow_blank=True, allow_null=True)
    
    # Campos de Usuario
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True, min_length=8)
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    
    
    # Campo de Perfil de Usuario
    imagen_url_perfil = serializers.URLField(required=False, allow_blank=True, allow_null=True)
    
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("El username ya existe")
        return value
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("El email ya está registrado")
        return value
    
    @transaction.atomic
    def create(self, validated_data):
        # Crear empresa
        empresa_data = {
            'razon_social': validated_data['razon_social'],
            'email_contacto': validated_data['email_contacto'],
            'nombre_comercial': validated_data['nombre_comercial'],
            'activo': True,
        }
        
        if validated_data.get('imagen_url_empresa'):
            empresa_data['Imagen_url'] = validated_data['imagen_url_empresa']
            
        empresa = Empresa.objects.create(**empresa_data)
        
        # Crear usuario
        user_data = {
            'username': validated_data['username'],
            'password': make_password(validated_data['password']),
            'first_name': validated_data['first_name'],
            'last_name': validated_data['last_name'],
            'email': validated_data['email'],
            'is_superuser': False,
            'is_staff': True,
        }
        
        user = User.objects.create(**user_data)
        
        # Crear perfil de usuario
        perfil_data = {
            'empresa': empresa,
            'usuario': user,
            'imagen_url': validated_data.get('imagen_url_perfil', '')
        }
        
        perfil_user = Perfiluser.objects.create(**perfil_data)
        
        # Crear token para el usuario
        token, created = Token.objects.get_or_create(user=user)
        
        return {
            'empresa': empresa,
            'user': user,
            'perfil_user': perfil_user,
            'token': token.key
        }


class LoginSerializer(Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        
        if email and password:
            # Buscar usuario por email
            try:
                user = User.objects.get(email=email)
                username = user.username
            except User.DoesNotExist:
                raise serializers.ValidationError("Credenciales inválidas")
            
            # Autenticar con username y password
            user = authenticate(username=username, password=password)
            
            if user:
                if user.is_active:
                    data['user'] = user
                else:
                    raise serializers.ValidationError("Usuario inactivo")
            else:
                raise serializers.ValidationError("Credenciales inválidas")
        else:
            raise serializers.ValidationError("Email y password son requeridos")
            
        return data
    
    def create(self, validated_data):
        user = validated_data['user']
        
        # Crear o obtener token
        token, created = Token.objects.get_or_create(user=user)
        
        # Obtener perfil de usuario y empresa
        try:
            perfil_user = Perfiluser.objects.get(usuario=user)
            empresa = perfil_user.empresa
            empresa_id = empresa.id
            empresa_nombre = empresa.razon_social
        except Perfiluser.DoesNotExist:
            empresa_id = None
            empresa_nombre = None
        
        return {
            'token': token.key,
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'nombre_completo': f"{user.first_name} {user.last_name}".strip(),
            'is_superuser': user.is_superuser,
            'is_staff': user.is_staff,
            'empresa_id': empresa_id,
            'empresa_nombre': empresa_nombre
        }


class LogoutSerializer(Serializer):
    token = serializers.CharField()
    
    def validate_token(self, value):
        try:
            token = Token.objects.get(key=value)
            return token
        except Token.DoesNotExist:
            raise serializers.ValidationError("Token inválido")
    
    def create(self, validated_data):
        token = validated_data['token']
        token.delete()
        return {'message': 'Logout exitoso'}


