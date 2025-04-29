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

def obtener_cards_observados():
    with connection.cursor() as cursor:       
        # Ejecutar el query con crosstab y parámetros dinámicos
        cursor.execute(
            '''
            SELECT
                estado,
                SUM(cant_registros) AS cantidad
            FROM public."OBSERVADOS"
            GROUP BY estado
            ''',
        )
        return cursor.fetchall()

def obtener_grafico_barras():
    with connection.cursor() as cursor:
        cursor.execute(
            '''
            SELECT 
                edad edad_ranking,
                SUM(estado) as estado_ranking,
                SUM(cant_registros) AS cantidad_ranking
            FROM 
                public."OBSERVADOS"
            WHERE 
                estado IN ('2','3','4')
            GROUP BY 
                edad
            ''',
        )
        return cursor.fetchall()


def obtener_ranking_observados():
    with connection.cursor() as cursor:
        cursor.execute(
            '''
            SELECT 
                provincia as provincia_ranking,
                distrito as distrito_ranking,
                edad edad_ranking,
                SUM(estado) as estado_ranking,
                SUM(cant_registros) AS cantidad_ranking
            FROM 
                public."OBSERVADOS"
            WHERE 
                estado IN ('2','3','4')
            GROUP BY 
                provincia,
                distrito,
                edad
            ORDER BY cantidad_ranking DESC
            ''',
        )
        return cursor.fetchall()



def obtener_detalle_acta():
    with connection.cursor() as cursor:
        cursor.execute(
            '''
                SELECT  
                provincia as provincia_detalle, 
                distrito as distrito_detalle, 
                municipio as municipio_detalle, 
                mes as mes_detalle, 
                fecha_inicial as fecha_inicial_detalle, 
                fecha_final as fecha_final_detalle, 
                fecha_envio as fecha_envio_detalle, 
                dni as dni_detalle, 
                primer_apellido as primer_apellido_detalle, 
                segundo_apellido as segundo_apellido_detalle, 
                nombres as nombres_detalle
                FROM public."indicador_acta"
                WHERE fecha_inicial is not null
            ''',
        )
        return cursor.fetchall()


# ===========================================================
# Funciones para el seguimiento
# ===========================================================   
def obtener_seguimiento_observados():
    with connection.cursor() as cursor:
        cursor.execute(
            '''
                SELECT 
                    "COD_PAD" as cod_pad, 
                    "TIPO_DOC" as tipo_doc, 
                    "CNV" as cnv, 
                    "CUI" as cui, 
                    "DNI" as dni, 
                    "NOMBRE_COMPLETO_NINO" as nombre_completo_nino, 
                    "SEXO_LETRA" as sexo_letra, 
                    "SEGURO" as seguro, 
                    "FECHA_NACIMIENTO_DATE" as fecha_nacimiento_date, 
                    "EDAD_LETRAS" as edad_letras, 
                    "DESCRIPCION" as descripcion, 
                    "PROVINCIA" as provincia_seguimiento, 
                    "DISTRITO" as distrito_seguimiento, 
                    "MENOR_VISITADO" as menor_visitado, 
                    "MENOR_ENCONTRADO" as menor_encontrado, 
                    "CODIGO_EESS" as codigo_eess, 
                    "NOMBRE_EESS" as nombre_eess, 
                    "FRECUENCIA_ATENCION" as frecuencia_atencion, 
                    "DNI_MADRE" as dni_madre, 
                    "NOMBRE_COMPLETO_MADRE" as nombre_completo_madre, 
                    "NUMERO_CELULAR" as numero_celular, 
                    "ESTADO_REGISTRO" as estado_registro, 
                    renaes, 
                    "Nombre_Establecimiento" as nombre_establecimiento, 
                    "Ubigueo_Establecimiento" as ubigueo_establecimiento,  
                    "Codigo_Red" as codigo_red, 
                    "Red" as red, 
                    "Codigo_MicroRed" as codigo_microred, 
                    "MicroRed" as microred
                FROM 
                    public."SEGUIMIENTO_SITUACION_PADRON"
                WHERE 
                    "ESTADO_REGISTRO" IN ('2','3','4','5','6')
                ORDER BY 
                    "PROVINCIA", "DISTRITO"
            ''',
        )
        return cursor.fetchall()