from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User  , Group , Permission 
from django.contrib.contenttypes.models import ContentType

class UserSerializers(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class GroupSerializers(ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'

class PermissionSerializers(ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'


class ContentTypeSerializers(ModelSerializer):
    class Meta:
        model = ContentType
        fields = '__all__'