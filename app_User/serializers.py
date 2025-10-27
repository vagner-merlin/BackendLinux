from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.contrib.auth.models import User  , Group , Permission 
from django.contrib.contenttypes.models import ContentType

class UserSerializers(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class GroupSerializers(ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Group
        fields = ['id', 'name']
        
    def create(self, validated_data):
        group = Group.objects.create(name=validated_data['name'])
        return group

class PermissionSerializers(ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'


class ContentTypeSerializers(ModelSerializer):
    class Meta:
        model = ContentType
        fields = '__all__'