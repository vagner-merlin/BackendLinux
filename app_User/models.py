from django.db import models
from app_Empresa.models import Empresa
from django.contrib.auth.models import User

class Perfiluser(models.Model):
    imagen_url = models.URLField(max_length=200)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)


# Create your models here.
