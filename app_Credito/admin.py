from django.contrib import admin
from .models import Tipo_Credito, Credito, Ganancia_Credito

@admin.register(Tipo_Credito)
class TipoCreditoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'monto_minimo', 'monto_maximo')
    search_fields = ('nombre', 'descripcion')
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'descripcion')
        }),
        ('Límites de Monto', {
            'fields': ('monto_minimo', 'monto_maximo')
        }),
    )

@admin.register(Credito)
class CreditoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente_nombre', 'empresa_nombre', 'Monto_Solicitado', 'enum_estado', 'Moneda', 'Numero_Cuotas', 'Fecha_Aprobacion')
    list_filter = ('enum_estado', 'Moneda', 'empresa', 'tipo_credito', 'Fecha_Aprobacion', 'Fecha_Desembolso')
    search_fields = ('cliente__nombre', 'cliente__apellido', 'empresa__razon_social', 'usuario__username')
    autocomplete_fields = ('empresa', 'usuario', 'cliente', 'tipo_credito')
    date_hierarchy = 'Fecha_Aprobacion'
    ordering = ('-Fecha_Aprobacion',)
    
    def cliente_nombre(self, obj):
        return f"{obj.cliente.nombre} {obj.cliente.apellido}"
    cliente_nombre.short_description = 'Cliente'
    cliente_nombre.admin_order_field = 'cliente__nombre'
    
    def empresa_nombre(self, obj):
        return obj.empresa.razon_social
    empresa_nombre.short_description = 'Empresa'
    empresa_nombre.admin_order_field = 'empresa__razon_social'
    
    fieldsets = (
        ('Relaciones', {
            'fields': ('empresa', 'usuario', 'cliente', 'tipo_credito')
        }),
        ('Detalles del Crédito', {
            'fields': ('Monto_Solicitado', 'Monto_Pagar', 'Numero_Cuotas', 'Monto_Cuota', 'Moneda', 'Tasa_Interes')
        }),
        ('Estado y Fechas', {
            'fields': ('enum_estado', 'Fecha_Aprobacion', 'Fecha_Desembolso', 'Fecha_Finalizacion')
        }),
    )

@admin.register(Ganancia_Credito)
class GananciaCreditoAdmin(admin.ModelAdmin):
    list_display = ('id', 'credito_id', 'cliente_nombre', 'monto_prestado', 'tasa_interes', 'duracion_meses', 'ganacia_esperada')
    list_filter = ('tasa_interes', 'duracion_meses')
    search_fields = ('Cliente__nombre', 'Cliente__apellido', 'Credito__id')
    autocomplete_fields = ('Cliente', 'Credito')
    
    def credito_id(self, obj):
        return f"Crédito #{obj.Credito.id}"
    credito_id.short_description = 'Crédito'
    credito_id.admin_order_field = 'Credito__id'
    
    def cliente_nombre(self, obj):
        return f"{obj.Cliente.nombre} {obj.Cliente.apellido}"
    cliente_nombre.short_description = 'Cliente'
    cliente_nombre.admin_order_field = 'Cliente__nombre'
    
    fieldsets = (
        ('Relaciones', {
            'fields': ('Credito', 'Cliente')
        }),
        ('Detalles Financieros', {
            'fields': ('monto_prestado', 'tasa_interes', 'duracion_meses', 'ganacia_esperada')
        }),
    )
