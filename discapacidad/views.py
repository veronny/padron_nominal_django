from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.db import connection


# filtros
from base.models import DimPeriodo, DimDiscapacidadEtapa, MAESTRO_HIS_ESTABLECIMIENTO
from .models import DimDisFisicaCie,TramaBaseDiscapacidadRpt02FisicaNominal
from django.db.models import Case, When, Value, IntegerField, Sum, OuterRef, Subquery, Value
from django.db.models.functions import Substr, Cast, Concat
from django.db.models import CharField

# report excel
from django.http.response import HttpResponse
from django.views.generic.base import TemplateView
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
import openpyxl
from openpyxl.utils import get_column_letter

from .utils import generar_operacional

# Create your views here.
@login_required
def operacional(request):
    return render(request, 'discapacidad/index.html')

################################################
# REPORTE DE SEGUIMIENTO
################################################
#--- PROVINCIAS -------------------------------------------------------------
def get_provincias(request,provincias_id):
    provincias = (
                 MAESTRO_HIS_ESTABLECIMIENTO
                 .objects.filter(Descripcion_Sector='GOBIERNO REGIONAL')
                 .annotate(ubigueo_filtrado=Substr('Ubigueo_Establecimiento', 1, 4))
                 .values('Provincia','ubigueo_filtrado')
                 .distinct()
    )
    mes_inicio = (
                DimPeriodo
                .objects.filter(Anio='2024')
                .annotate(periodo_filtrado=Substr('Periodo', 1, 6))
                .values('Mes','periodo_filtrado')
                .order_by('NroMes')
                .distinct()
    ) 
    mes_fin = (
                DimPeriodo
                .objects.filter(Anio='2024')
                .annotate(periodo_filtrado=Substr('Periodo', 1, 6))
                .values('Mes','periodo_filtrado')
                .order_by('NroMes')
                .distinct()
    ) 
    context = {
                'provincias': provincias,
                'mes_inicio':mes_inicio,
                'mes_fin':mes_fin,
              }
    
    return render(request, 'discapacidad/provincias.html', context)


def rpt_operacional_fisico(ubigeo, fecha_inicio, fecha_fin):
    with connection.cursor() as cursor:
        # Crear una tabla temporal
        cursor.execute("""
            CREATE TABLE #temp_resultados (
                ubigeo_filtrado VARCHAR(4),
                renaes VARCHAR(20),
                dis_1 INT,
                dis_2 INT,
                dis_3 INT,
                dis_4 INT,
                dis_5 INT
            )
        """)

        # Insertar los datos agrupados y las sumas en la tabla temporal
        cursor.execute("""
            INSERT INTO #temp_resultados
            SELECT
                SUBSTRING(CAST(ubigeo AS VARCHAR(10)), 1, 4) AS ubigeo_filtrado,
                renaes,
                SUM(CASE WHEN Categoria = 1 AND gedad = 1 THEN 1 ELSE 0 END) AS dis_1,
                SUM(CASE WHEN Categoria = 1 AND gedad = 2 THEN 1 ELSE 0 END) AS dis_2,
                SUM(CASE WHEN Categoria = 1 AND gedad = 3 THEN 1 ELSE 0 END) AS dis_3,
                SUM(CASE WHEN Categoria = 1 AND gedad = 4 THEN 1 ELSE 0 END) AS dis_4,
                SUM(CASE WHEN Categoria = 1 AND gedad = 5 THEN 1 ELSE 0 END) AS dis_5
            FROM TRAMA_BASE_DISCAPACIDAD_RPT_02_FISICA_NOMINAL
            WHERE SUBSTRING(CAST(ubigeo AS VARCHAR(10)), 1, 4) = %s
                AND periodo BETWEEN %s AND %s
            GROUP BY SUBSTRING(CAST(ubigeo AS VARCHAR(10)), 1, 4), renaes
        """, [str(ubigeo)[:4], fecha_inicio, fecha_fin])

        # Consultar los resultados finales desde la tabla temporal
        cursor.execute("""
            SELECT
                CONCAT(#temp_resultados.ubigeo_filtrado, '-',MAESTRO_HIS_ESTABLECIMIENTO.Provincia) AS nombre_provincia_ubigeo_filtrado,
                #temp_resultados.dis_1,
                #temp_resultados.dis_2,
                #temp_resultados.dis_3,
                #temp_resultados.dis_4,
                #temp_resultados.dis_5
            FROM #temp_resultados
            JOIN MAESTRO_HIS_ESTABLECIMIENTO ON MAESTRO_HIS_ESTABLECIMIENTO.Codigo_Unico = #temp_resultados.renaes
        """)

        resultado_prov = cursor.fetchall()

    return resultado_prov
# validar matriz
def crear_matriz(request):
    
    ubigeo = '1201'
    fecha_inicio = '20240102'# Ejemplo de ubigeo
    fecha_fin = '20240110'# Ejemplo de ubigeo
    matriz = rpt_operacional_fisico(ubigeo,fecha_inicio,fecha_fin)
    
    # Puedes renderizar la matriz en una plantilla HTML o hacer cualquier otro procesamiento necesario
    return render(request, 'discapacidad/matrizes.html', {'matriz': matriz})


#--- PROVINCIAS EXCEL -------------------------------------------------------------
class RptOperacinalProv(TemplateView):
    def get(self, request, *args, **kwargs):
        # Variables ingresadas
        fecha_inicio = request.GET.get('fecha_inicio')
        fecha_fin = request.GET.get('fecha_fin')
        provincia = request.GET.get('provincia')

        # Creación de la consulta
        resultado_prov = rpt_operacional_fisico(provincia, fecha_inicio, fecha_fin)

        # Crear un nuevo libro de Excel
        workbook = openpyxl.Workbook()
        sheet = workbook.active

        # Definir ubicaciones específicas para cada columna y su suma total
        columnas_ubicaciones = {
            'PROVINCIA': 'D10',
            'DIS_1': 'K15',
            'DIS_2': 'J5',
            'DIS_3': 'P7',
            'DIS_4': 'R17',
            'DIS_5': 'S27'
        }

        # Inicializar diccionario para almacenar sumas por columna
        column_sums = {
            'DIS_1': 0,
            'DIS_2': 0,
            'DIS_3': 0,
            'DIS_4': 0,
            'DIS_5': 0
        }

        # Procesar los datos y calcular las sumas por columna
        for row in resultado_prov:
            for col_name in column_sums:
                # Obtener el índice de la columna según el nombre (DIS_1 -> 1, DIS_2 -> 2, etc.)
                col_index = list(columnas_ubicaciones.keys()).index(col_name)
                column_sums[col_name] += row[col_index]

        # Escribir las sumas totales por columna en la hoja de cálculo
        for col_name, total_cell in columnas_ubicaciones.items():
            if col_name in column_sums:
                sheet[total_cell] = str(column_sums[col_name])     

        # Establecer el nombre del archivo
        nombre_archivo = "rpt_operacional_fisico.xlsx"

        # Definir el tipo de respuesta que se va a dar
        response = HttpResponse(content_type="application/ms-excel")
        contenido = "attachment; filename={}".format(nombre_archivo)
        response["Content-Disposition"] = contenido
        workbook.save(response)

        return response
