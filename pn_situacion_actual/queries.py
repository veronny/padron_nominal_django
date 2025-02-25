from django.http import JsonResponse, HttpResponse
from base.models import MAESTRO_HIS_ESTABLECIMIENTO, DimPeriodo
from django.db.models.functions import Substr
from django.db.models import IntegerField
from django.db.models.functions import Cast

from django.db import connection

# ===========================================================
# Funciones auxiliares de obtención de datos
# ===========================================================
def obtener_provincias(request):
    provincias = (
                MAESTRO_HIS_ESTABLECIMIENTO
                .objects.filter(Descripcion_Sector='GOBIERNO REGIONAL')
                .annotate(ubigueo_filtrado=Substr('Ubigueo_Establecimiento', 1, 4))
                .values('Provincia','ubigueo_filtrado')
                .distinct()
                .order_by('Provincia')
    )    
    return list(provincias)

def obtener_distritos(provincia):
    distritos = MAESTRO_HIS_ESTABLECIMIENTO.objects.filter(Provincia=provincia).values('Distrito').distinct().order_by('Distrito')
    return list(distritos)

def obtener_avance_situacion_padron(provincia, distrito):
    with connection.cursor() as cursor:
        cursor.execute(
            '''
            SELECT "N28_dias"
                    ,"N0a5meses"
                    ,"N6a11meses"
                    ,"cero_anios"
                    ,"un_anios"
                    ,"dos_anios"
                    ,"tres_anios"
                    ,"cuatro_anio"
                    ,"cinco_anios"
                    ,"total_den"
            FROM public."SITUACION_PADRON" 
            WHERE "DEPARTAMENTO" = 'JUNIN' AND "PROVINCIA" = %s AND "DISTRITO" = %s
            ORDER BY "DEPARTAMENTO", "PROVINCIA", "DISTRITO";
            ''',
            [provincia, distrito]
        )
        return cursor.fetchall()

def obtener_cumple_situacion_dni(provincia, distrito):
    with connection.cursor() as cursor:
        cursor.execute(
            '''
            SELECT  "total_cumple_dni",
                    "brecha_dni",
                    "cob_dni"
            FROM public."SITUACION_PADRON"
            WHERE "DEPARTAMENTO" = 'JUNIN' AND "PROVINCIA" = %s AND "DISTRITO" = %s
            ORDER BY "DEPARTAMENTO", "PROVINCIA", "DISTRITO";
            ''',
            [provincia, distrito]
        )
        return cursor.fetchall()


def obtener_cumple_situacion_cnv(provincia, distrito):
    with connection.cursor() as cursor:
        cursor.execute(
            '''
            SELECT  "total_cumple_cnv",
                    "brecha_cumple_cnv",
                    "cob_cnv"
            FROM public."SITUACION_PADRON"
            WHERE "DEPARTAMENTO" = 'JUNIN' AND "PROVINCIA" = %s AND "DISTRITO" = %s
            ORDER BY "DEPARTAMENTO", "PROVINCIA", "DISTRITO";
            ''',
            [provincia, distrito]
        )
        return cursor.fetchall()
    
def obtener_cumple_situacion_eje_vial(provincia, distrito):
    with connection.cursor() as cursor:
        cursor.execute(
            '''
            SELECT  "total_cumple_eje_vial",
                    "brecha_eje_vial",
                    "cob_eje_vial"
            FROM public."SITUACION_PADRON"
            WHERE "DEPARTAMENTO" = 'JUNIN' AND "PROVINCIA" = %s AND "DISTRITO" = %s
            ORDER BY "DEPARTAMENTO", "PROVINCIA", "DISTRITO";
            ''',
            [provincia, distrito]
        )
        return cursor.fetchall()

def obtener_cumple_situacion_direccion(provincia, distrito):
    with connection.cursor() as cursor:
        cursor.execute(
            '''
            SELECT  "total_cumple_direccion",
                    "brecha_direccion",
                    "cob_direccion"
            FROM public."SITUACION_PADRON"
            WHERE "DEPARTAMENTO" = 'JUNIN' AND "PROVINCIA" = %s AND "DISTRITO" = %s
            ORDER BY "DEPARTAMENTO", "PROVINCIA", "DISTRITO";
            ''',
            [provincia, distrito]
        )
        return cursor.fetchall()
    
def obtener_cumple_situacion_referencia(provincia, distrito):
    with connection.cursor() as cursor:
        cursor.execute(
            '''
            SELECT  "total_cumple_referencia",
                    "brecha_referencia",
                    "cob_referencia"
            FROM public."SITUACION_PADRON"
            WHERE "DEPARTAMENTO" = 'JUNIN' AND "PROVINCIA" = %s AND "DISTRITO" = %s
            ORDER BY "DEPARTAMENTO", "PROVINCIA", "DISTRITO";
            ''',
            [provincia, distrito]
        )
        return cursor.fetchall()

def obtener_cumple_situacion_visitado(provincia, distrito):
    with connection.cursor() as cursor:
        cursor.execute(
            '''
            SELECT  "total_cumple_visitado",
                    "brecha_visitado",
                    "cob_visitado"
            FROM public."SITUACION_PADRON"
            WHERE "DEPARTAMENTO" = 'JUNIN' AND "PROVINCIA" = %s AND "DISTRITO" = %s
            ORDER BY "DEPARTAMENTO", "PROVINCIA", "DISTRITO";
            ''',
            [provincia, distrito]
        )
        return cursor.fetchall()

def obtener_cumple_situacion_encontrado(provincia, distrito):
    with connection.cursor() as cursor:
        cursor.execute(
            '''
            SELECT  "total_cumple_encontrado",
                    "brecha_encontrado",
                    "cob_encontrado"
            FROM public."SITUACION_PADRON"
            WHERE "DEPARTAMENTO" = 'JUNIN' AND "PROVINCIA" = %s AND "DISTRITO" = %s
            ORDER BY "DEPARTAMENTO", "PROVINCIA", "DISTRITO";
            ''',
            [provincia, distrito]
        )
        return cursor.fetchall()

def obtener_cumple_situacion_celular(provincia, distrito):
    with connection.cursor() as cursor:
        cursor.execute(
            '''
            SELECT  "total_cumple_celular",
                    "brecha_celular",
                    "cob_celular"
            FROM public."SITUACION_PADRON"
            WHERE "DEPARTAMENTO" = 'JUNIN' AND "PROVINCIA" = %s AND "DISTRITO" = %s
            ORDER BY "DEPARTAMENTO", "PROVINCIA", "DISTRITO";
            ''',
            [provincia, distrito]
        )
        return cursor.fetchall()
    
def obtener_cumple_situacion_sexo(provincia, distrito):
    with connection.cursor() as cursor:
        cursor.execute(
            '''
            SELECT  "total_cumple_sexo_masculino",
                    "total_cumple_sexo_femenino",
                    "cob_sexo"
            FROM public."SITUACION_PADRON"
            WHERE "DEPARTAMENTO" = 'JUNIN' AND "PROVINCIA" = %s AND "DISTRITO" = %s
            ORDER BY "DEPARTAMENTO", "PROVINCIA", "DISTRITO";
            ''',
            [provincia, distrito]
        )
        return cursor.fetchall()

def obtener_cumple_situacion_seguro(provincia, distrito):
    with connection.cursor() as cursor:
        cursor.execute(
            '''
            SELECT  "total_cumple_seguro",
                    "brecha_seguro",
                    "cob_seguro"
            FROM public."SITUACION_PADRON"
            WHERE "DEPARTAMENTO" = 'JUNIN' AND "PROVINCIA" = %s AND "DISTRITO" = %s
            ORDER BY "DEPARTAMENTO", "PROVINCIA", "DISTRITO";
            ''',
            [provincia, distrito]
        )
        return cursor.fetchall()

def obtener_cumple_situacion_eess(provincia, distrito):
    with connection.cursor() as cursor:
        cursor.execute(
            '''
            SELECT  "total_eess",
                    "brecha_eess",
                    "cob_eess"
            FROM public."SITUACION_PADRON"
            WHERE "DEPARTAMENTO" = 'JUNIN' AND "PROVINCIA" = %s AND "DISTRITO" = %s
            ORDER BY "DEPARTAMENTO", "PROVINCIA", "DISTRITO";
            ''',
            [provincia, distrito]
        )
        return cursor.fetchall()

def obtener_cumple_situacion_frecuencia(provincia, distrito):
    with connection.cursor() as cursor:
        cursor.execute(
            '''
            SELECT  "total_frecuencia",
                    "brecha_frecuencia",
                    "cob_frecuencia"
            FROM public."SITUACION_PADRON"
            WHERE "DEPARTAMENTO" = 'JUNIN' AND "PROVINCIA" = %s AND "DISTRITO" = %s
            ORDER BY "DEPARTAMENTO", "PROVINCIA", "DISTRITO";
            ''',
            [provincia, distrito]
        )
        return cursor.fetchall()
    
def obtener_cumple_situacion_direccion_completa(provincia, distrito):
    with connection.cursor() as cursor:
        cursor.execute(
            '''
            SELECT  "total_direccion_completa",
                    "brecha_direccion_completa",
                    "cob_direccion_completa"
            FROM public."SITUACION_PADRON"
            WHERE "DEPARTAMENTO" = 'JUNIN' AND "PROVINCIA" = %s AND "DISTRITO" = %s
            ORDER BY "DEPARTAMENTO", "PROVINCIA", "DISTRITO";
            ''',
            [provincia, distrito]
        )
        return cursor.fetchall()
    
def obtener_cumple_situacion_visitado_no_encontrado(provincia, distrito):
    with connection.cursor() as cursor:
        cursor.execute(
            '''
            SELECT  "total_visitado_no_encontrado",
                    "brecha_visitado_no_encontrado",
                    "cob_visitado_no_encontrado"
            FROM public."SITUACION_PADRON"
            WHERE "DEPARTAMENTO" = 'JUNIN' AND "PROVINCIA" = %s AND "DISTRITO" = %s
            ORDER BY "DEPARTAMENTO", "PROVINCIA", "DISTRITO";
            ''',
            [provincia, distrito]
        )
        return cursor.fetchall()