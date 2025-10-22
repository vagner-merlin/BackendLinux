from django.db import models
from app_Empresa.models import Empresa
from django.contrib.auth.models import User

class Perfiluser(models.Model):
    imagen_url = models.URLField(
        max_length=200,
        blank=True,
        null=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.usuario.username} - {self.empresa.razon_social}"
