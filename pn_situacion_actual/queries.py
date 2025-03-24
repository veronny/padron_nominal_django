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



def obtener_avance_situacion_padron(departamento,provincia, distrito):
    with connection.cursor() as cursor:
        cursor.execute(
            '''
            SELECT 
                SUM("N28_dias") AS N28_dias,
                SUM("N0a5meses") AS N0a5meses,
                SUM("N6a11meses") AS N6a11meses,
                SUM("cero_anios") AS cero_anios,
                SUM("un_anios") AS un_anios,
                SUM("dos_anios") AS dos_anios,
                SUM("tres_anios") AS tres_anios,
                SUM("cuatro_anio") AS cuatro_anio,
                SUM("cinco_anios") AS cinco_anios,
                SUM("total_den") AS total_den
            FROM public."SITUACION_PADRON" 
            WHERE
                (COALESCE(%s, '') = '' OR "DEPARTAMENTO" = %s) AND
                (COALESCE(%s, '') = '' OR "PROVINCIA" = %s) AND
                (COALESCE(%s, '') = '' OR "DISTRITO" = %s);
            ''',
            [   
                departamento, departamento,
                provincia, provincia,
                distrito, distrito
            ]
        )
        return cursor.fetchall()

def obtener_cumple_situacion_dni(departamento, provincia, distrito):
    with connection.cursor() as cursor:
        cursor.execute(
            '''
            SELECT  
                SUM("total_cumple_dni") AS total_cumple_dni,
                SUM("brecha_dni") AS brecha_dni,
                SUM("cob_dni") AS cob_dni
            FROM public."SITUACION_PADRON"
            WHERE 
                (COALESCE(%s, '') = '' OR "DEPARTAMENTO" = %s) AND
                (COALESCE(%s, '') = '' OR "PROVINCIA" = %s) AND
                (COALESCE(%s, '') = '' OR "DISTRITO" = %s);
            ''',
            [
                departamento, departamento,
                provincia, provincia,
                distrito, distrito
            ]
        )
        return cursor.fetchall()


def obtener_cumple_situacion_cnv(departamento, provincia, distrito):
    with connection.cursor() as cursor:
        cursor.execute(
            '''
            SELECT  
                SUM("total_cumple_cnv") AS total_cumple_cnv,
                SUM("brecha_cumple_cnv") AS brecha_cumple_cnv,
                SUM("cob_cnv") AS cob_cnv
            FROM public."SITUACION_PADRON"
            WHERE 
                (COALESCE(%s, '') = '' OR "DEPARTAMENTO" = %s) AND
                (COALESCE(%s, '') = '' OR "PROVINCIA" = %s) AND
                (COALESCE(%s, '') = '' OR "DISTRITO" = %s);
            ''',
            [
                departamento, departamento,
                provincia, provincia,
                distrito, distrito
            ]
        )
        return cursor.fetchall()
    
def obtener_cumple_situacion_eje_vial(departamento, provincia, distrito):
    with connection.cursor() as cursor:
        cursor.execute(
            '''
            SELECT  
                SUM("total_cumple_eje_vial") AS total_cumple_eje_vial,
                SUM("brecha_eje_vial") AS brecha_eje_vial,
                SUM("cob_eje_vial") AS cob_eje_vial
            FROM public."SITUACION_PADRON"
            WHERE 
                (COALESCE(%s, '') = '' OR "DEPARTAMENTO" = %s) AND
                (COALESCE(%s, '') = '' OR "PROVINCIA" = %s) AND
                (COALESCE(%s, '') = '' OR "DISTRITO" = %s);
            ''',
            [
                departamento, departamento,
                provincia, provincia,
                distrito, distrito
            ]
        )
        return cursor.fetchall()

def obtener_cumple_situacion_direccion(departamento, provincia, distrito):
    with connection.cursor() as cursor:
        cursor.execute(
            '''
            SELECT  
                SUM("total_cumple_direccion") AS total_cumple_direccion,
                SUM("brecha_direccion") AS brecha_direccion,
                SUM("cob_direccion") AS cob_direccion
            FROM public."SITUACION_PADRON"
            WHERE 
                (COALESCE(%s, '') = '' OR "DEPARTAMENTO" = %s) AND
                (COALESCE(%s, '') = '' OR "PROVINCIA" = %s) AND
                (COALESCE(%s, '') = '' OR "DISTRITO" = %s);
            ''',
            [
                departamento, departamento,
                provincia, provincia,
                distrito, distrito
            ]
        )
        return cursor.fetchall()
    
def obtener_cumple_situacion_referencia(departamento, provincia, distrito):
    with connection.cursor() as cursor:
        cursor.execute(
            '''
            SELECT  
                SUM("total_cumple_referencia") AS total_cumple_referencia,
                SUM("brecha_referencia") AS brecha_referencia,
                SUM("cob_referencia") AS cob_referencia
            FROM public."SITUACION_PADRON"
            WHERE 
                (COALESCE(%s, '') = '' OR "DEPARTAMENTO" = %s) AND
                (COALESCE(%s, '') = '' OR "PROVINCIA" = %s) AND
                (COALESCE(%s, '') = '' OR "DISTRITO" = %s);
            ''',
            [
                departamento, departamento,
                provincia, provincia,
                distrito, distrito
            ]
        )
        return cursor.fetchall()

def obtener_cumple_situacion_visitado(departamento, provincia, distrito):
    with connection.cursor() as cursor:
        cursor.execute(
            '''
            SELECT  
                SUM("total_cumple_visitado") AS total_cumple_visitado,
                SUM("brecha_visitado") AS brecha_visitado,
                SUM("cob_visitado") AS cob_visitado
            FROM public."SITUACION_PADRON"
            WHERE 
                (COALESCE(%s, '') = '' OR "DEPARTAMENTO" = %s) AND
                (COALESCE(%s, '') = '' OR "PROVINCIA" = %s) AND
                (COALESCE(%s, '') = '' OR "DISTRITO" = %s);
            ''',
            [
                departamento, departamento,
                provincia, provincia,
                distrito, distrito
            ]
        )
        return cursor.fetchall()

def obtener_cumple_situacion_encontrado(departamento, provincia, distrito):
    with connection.cursor() as cursor:
        cursor.execute(
            '''
            SELECT  
                SUM("total_cumple_encontrado") AS total_cumple_encontrado,
                SUM("brecha_encontrado") AS brecha_encontrado,
                SUM("cob_encontrado") AS cob_encontrado
            FROM public."SITUACION_PADRON"
            WHERE 
                (COALESCE(%s, '') = '' OR "DEPARTAMENTO" = %s) AND
                (COALESCE(%s, '') = '' OR "PROVINCIA" = %s) AND
                (COALESCE(%s, '') = '' OR "DISTRITO" = %s);
            ''',
            [
                departamento, departamento,
                provincia, provincia,
                distrito, distrito
            ]
        )
        return cursor.fetchall()

def obtener_cumple_situacion_celular(departamento, provincia, distrito):
    with connection.cursor() as cursor:
        cursor.execute(
            '''
            SELECT  
                SUM("total_cumple_celular") AS total_cumple_celular,
                SUM("brecha_celular") AS brecha_celular,
                SUM("cob_celular") AS cob_celular
            FROM public."SITUACION_PADRON"
            WHERE 
                (COALESCE(%s, '') = '' OR "DEPARTAMENTO" = %s) AND
                (COALESCE(%s, '') = '' OR "PROVINCIA" = %s) AND
                (COALESCE(%s, '') = '' OR "DISTRITO" = %s);
            ''',
            [
                departamento, departamento,
                provincia, provincia,
                distrito, distrito
            ]
        )
        return cursor.fetchall()
    
def obtener_cumple_situacion_sexo(departamento, provincia, distrito):
    with connection.cursor() as cursor:
        cursor.execute(
            '''
            SELECT  
                SUM("total_cumple_sexo_masculino") AS total_cumple_sexo_masculino,
                SUM("total_cumple_sexo_femenino") AS total_cumple_sexo_femenino,
                SUM("cob_sexo") AS cob_sexo
            FROM public."SITUACION_PADRON"
            WHERE 
                (COALESCE(%s, '') = '' OR "DEPARTAMENTO" = %s) AND
                (COALESCE(%s, '') = '' OR "PROVINCIA" = %s) AND
                (COALESCE(%s, '') = '' OR "DISTRITO" = %s);
            ''',
            [
                departamento, departamento,
                provincia, provincia,
                distrito, distrito
            ]
        )
        return cursor.fetchall()

def obtener_cumple_situacion_seguro(departamento, provincia, distrito):
    with connection.cursor() as cursor:
        cursor.execute(
            '''
            SELECT  
                SUM("total_cumple_seguro") AS total_cumple_seguro,
                SUM("brecha_seguro") AS brecha_seguro,
                SUM("cob_seguro") AS cob_seguro
            FROM public."SITUACION_PADRON"
            WHERE 
                (COALESCE(%s, '') = '' OR "DEPARTAMENTO" = %s) AND
                (COALESCE(%s, '') = '' OR "PROVINCIA" = %s) AND
                (COALESCE(%s, '') = '' OR "DISTRITO" = %s);
            ''',
            [
                departamento, departamento,
                provincia, provincia,
                distrito, distrito
            ]
        )
        return cursor.fetchall()

def obtener_cumple_situacion_eess(departamento, provincia, distrito):
    with connection.cursor() as cursor:
        cursor.execute(
            '''
            SELECT  
                SUM("total_eess") AS total_eess,
                SUM("brecha_eess") AS brecha_eess,
                SUM("cob_eess") AS cob_eess
            FROM public."SITUACION_PADRON"
            WHERE 
                (COALESCE(%s, '') = '' OR "DEPARTAMENTO" = %s) AND
                (COALESCE(%s, '') = '' OR "PROVINCIA" = %s) AND
                (COALESCE(%s, '') = '' OR "DISTRITO" = %s);
            ''',
            [
                departamento, departamento,
                provincia, provincia,
                distrito, distrito
            ]
        )
        return cursor.fetchall()

def obtener_cumple_situacion_frecuencia(departamento, provincia, distrito):
    with connection.cursor() as cursor:
        cursor.execute(
            '''
            SELECT  
                SUM("total_frecuencia") AS total_frecuencia,
                SUM("brecha_frecuencia") AS brecha_frecuencia,
                SUM("cob_frecuencia") AS cob_frecuencia
            FROM public."SITUACION_PADRON"
            WHERE 
                (COALESCE(%s, '') = '' OR "DEPARTAMENTO" = %s) AND
                (COALESCE(%s, '') = '' OR "PROVINCIA" = %s) AND
                (COALESCE(%s, '') = '' OR "DISTRITO" = %s);
            ''',
            [
                departamento, departamento,
                provincia, provincia,
                distrito, distrito
            ]
        )
        return cursor.fetchall()
    
def obtener_cumple_situacion_direccion_completa(departamento, provincia, distrito):
    with connection.cursor() as cursor:
        cursor.execute(
            '''
            SELECT  
                SUM("total_direccion_completa") AS total_direccion_completa,
                SUM("brecha_direccion_completa") AS brecha_direccion_completa,
                SUM("cob_direccion_completa") AS cob_direccion_completa
            FROM public."SITUACION_PADRON"
            WHERE 
                (COALESCE(%s, '') = '' OR "DEPARTAMENTO" = %s) AND
                (COALESCE(%s, '') = '' OR "PROVINCIA" = %s) AND
                (COALESCE(%s, '') = '' OR "DISTRITO" = %s);
            ''',
            [
                departamento, departamento,
                provincia, provincia,
                distrito, distrito
            ]
        )
        return cursor.fetchall()
    
def obtener_cumple_situacion_visitado_no_encontrado(departamento, provincia, distrito):
    with connection.cursor() as cursor:
        cursor.execute(
            '''
            SELECT  
                SUM("total_visitado_no_encontrado") AS total_visitado_no_encontrado,
                SUM("brecha_visitado_no_encontrado") AS brecha_visitado_no_encontrado,
                SUM("cob_visitado_no_encontrado") AS cob_visitado_no_encontrado
            FROM public."SITUACION_PADRON"
            WHERE 
                (COALESCE(%s, '') = '' OR "DEPARTAMENTO" = %s) AND
                (COALESCE(%s, '') = '' OR "PROVINCIA" = %s) AND
                (COALESCE(%s, '') = '' OR "DISTRITO" = %s);
            ''',
            [
                departamento, departamento,
                provincia, provincia,
                distrito, distrito
            ]
        )
        return cursor.fetchall()