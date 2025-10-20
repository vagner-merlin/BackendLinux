from django.db import models

# Create your models here.
class Trabajo(models.Model):
    cargo = models.CharField(max_length=100)
    empresa = models.CharField(max_length=100)
    extracto_url = models.URLField(max_length=200)
    salario = models.DecimalField(max_digits=10, decimal_places=2)
    ubicacion = models.CharField(max_length=100)
    descripcion = models.TextField()

class Documentacion(models.Model):
    ci = models.CharField(max_length=20)
    documento_url = models.URLField(max_length=200)
    fecha_registro = models.DateField(auto_now_add=True)

class Garante(models.Model):
    nombrecompleto = models.CharField(max_length=100)
    ci = models.CharField(max_length=20)
    telefono = models.CharField(max_length=15)

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    fecha_registro = models.DateField(auto_now_add=True)

class Domicilio(models.Model):
    descripcion = models.CharField(max_length=200)
    croquis_url = models.URLField(max_length=200)
    es_propietario = models.BooleanField()
    numero_ref = models.CharField(max_length=50)

