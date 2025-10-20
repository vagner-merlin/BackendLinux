from django.db import models
from django.contrib.auth.models import User
from app_Cliente.models import Cliente
from app_User.models import Perfiluser
from app_Empresa.models import Empresa

# Create your models here.
ENUM_ESTADO_CREDITO = [
    ('Pendiente', 'Pendiente'),
    ('Aprobado', 'Aprobado'),
    ('Rechazado', 'Rechazado'),
    ('SOLICITADO', 'SOLICITADO'),
    ('DESENBOLSADO', 'DESENBOLSADO'),
    ('FINALIZADO', 'FINALIZADO'),
]
class Tipo_Credito(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    monto_minimo = models.DecimalField(max_digits=10, decimal_places=2)
    monto_maximo = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nombre
    

class Credito(models.Model): 
    Monto_Solicitado = models.DecimalField(max_digits=10, decimal_places=2)
    enum_estado = models.CharField(max_length=20, choices=ENUM_ESTADO_CREDITO, default='Pendiente')
    Numero_Cuotas = models.IntegerField()
    Monto_Cuota = models.DecimalField(max_digits=10, decimal_places=2)
    Moneda = models.CharField(max_length=10)
    Tasa_Interes = models.DecimalField(max_digits=5, decimal_places=2)
    Fecha_Aprobacion = models.DateField(null=True, blank=True)
    Fecha_Desembolso = models.DateField(null=True, blank=True)
    Fecha_Finalizacion = models.DateField(null=True, blank=True)
    Monto_Pagar = models.DecimalField(max_digits=10, decimal_places=2)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    tipo_credito = models.ForeignKey(Tipo_Credito, on_delete=models.CASCADE)

    def __str__(self):
        return f"Crédito {self.id} - Cliente: {self.cliente.nombre} - Monto Solicitado: {self.Monto_Solicitado} {self.Moneda}"
    
class Ganancia_Credito(models.Model):
    monto_prestado = models.DecimalField(max_digits=10, decimal_places=2)
    tasa_interes = models.DecimalField(max_digits=5, decimal_places=2)
    duracion_meses = models.IntegerField()
    ganacia_esperada = models.DecimalField(max_digits=10, decimal_places=2)
    Cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    Credito = models.ForeignKey(Credito, on_delete=models.CASCADE)

    def __str__(self):
        return f"Ganancia Crédito {self.Credito.id} - Cliente: {self.Cliente.nombre}"       


