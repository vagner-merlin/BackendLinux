from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions , status
from django.db import connection

class HistorialCreditoView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    d.ci AS ci_cliente,
                    c.nombre AS nombre_cliente,
                    c.apellido AS apellido_cliente,
                    t.cargo AS cargo,
                    t.empresa AS empresa_trabajo,
                    t.salario AS salario,
                    cr."Monto_Solicitado" AS monto_prestamo,
                    cr."enum_estado" AS estado_prestamo,
                    cr."Moneda" AS moneda
                FROM 
                    "app_Cliente_cliente" c
                    LEFT JOIN "app_Cliente_documentacion" d ON d.id_cliente_id = c.id
                    LEFT JOIN "app_Cliente_trabajo" t ON t.id_cliente_id = c.id
                    LEFT JOIN "app_Credito_credito" cr ON cr.cliente_id = c.id
                ORDER BY 
                    c.nombre, cr."Fecha_Aprobacion" DESC
            """)
            columns = [col[0] for col in cursor.description]
            records = [dict(zip(columns, row)) for row in cursor.fetchall()]
            
        return Response(records)

class HistorialCreditoCIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, ci):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    d.ci AS ci_cliente,
                    c.nombre AS nombre_cliente,
                    c.apellido AS apellido_cliente,
                    t.cargo AS cargo,
                    t.empresa AS empresa_trabajo,
                    t.salario AS salario,
                    cr."Monto_Solicitado" AS monto_prestamo,
                    cr."enum_estado" AS estado_prestamo,
                    cr."Moneda" AS moneda
                FROM 
                    "app_Cliente_cliente" c
                    LEFT JOIN "app_Cliente_documentacion" d ON d.id_cliente_id = c.id
                    LEFT JOIN "app_Cliente_trabajo" t ON t.id_cliente_id = c.id
                    LEFT JOIN "app_Credito_credito" cr ON cr.cliente_id = c.id
                WHERE 
                    d.ci = %s
                ORDER BY 
                    c.nombre, cr."Fecha_Aprobacion" DESC
            """, [ci])
            columns = [col[0] for col in cursor.description]
            records = [dict(zip(columns, row)) for row in cursor.fetchall()]
            
        return Response(records)
    

class EstadoCreditoCIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, ci):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    d.ci AS ci_cliente,
                    c.nombre AS nombre_cliente,
                    c.apellido AS apellido_cliente,
                    cr."enum_estado" AS estado_credito,
                    cr."Monto_Solicitado" AS monto,
                    cr."Moneda" AS moneda,
                    cr."Fecha_Aprobacion" AS fecha_aprobacion
                FROM 
                    "app_Cliente_cliente" c
                    INNER JOIN "app_Cliente_documentacion" d ON d.id_cliente_id = c.id
                    INNER JOIN "app_Credito_credito" cr ON cr.cliente_id = c.id
                WHERE 
                    d.ci = %s
                ORDER BY 
                    cr."Fecha_Aprobacion" DESC
            """, [ci])
            columns = [col[0] for col in cursor.description]
            records = [dict(zip(columns, row)) for row in cursor.fetchall()]
            
        if not records:
            return Response(
                {"message": "No se encontraron créditos para el CI proporcionado"}, 
                status=status.HTTP_404_NOT_FOUND
            )
            
        return Response(records)