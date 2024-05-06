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

        # cambia el alto de la columna
        sheet.row_dimensions[1].height = 14
        sheet.row_dimensions[2].height = 14
        sheet.row_dimensions[4].height = 25
        sheet.row_dimensions[15].height = 25
        # cambia el ancho de la columna
        sheet.column_dimensions['A'].width = 2
        sheet.column_dimensions['B'].width = 40
        sheet.column_dimensions['C'].width = 9
        sheet.column_dimensions['D'].width = 9
        sheet.column_dimensions['E'].width = 10
        sheet.column_dimensions['F'].width = 9
        sheet.column_dimensions['G'].width = 9
        sheet.column_dimensions['H'].width = 9
        sheet.column_dimensions['I'].width = 9
        # linea de division
        sheet.freeze_panes = 'AL8'
        
        # Configuración del fondo y el borde
        fill = PatternFill(patternType='solid', fgColor='00B0F0')
        border = Border(left=Side(style='thin', color='00B0F0'),
                        right=Side(style='thin', color='00B0F0'),
                        top=Side(style='thin', color='00B0F0'),
                        bottom=Side(style='thin', color='00B0F0'))

        borde_plomo = Border(left=Side(style='thin', color='A9A9A9'), # Plomo
                right=Side(style='thin', color='A9A9A9'), # Plomo
                top=Side(style='thin', color='A9A9A9'), # Plomo
                bottom=Side(style='thin', color='A9A9A9')) # Plomo


        # crea titulo del reporte
        sheet['B1'].alignment = Alignment(horizontal= "left", vertical="center")
        sheet['B1'].font = Font(name = 'Arial', size= 7, bold = True)
        sheet['B1'] = 'OFICINA DE TECNOLOGIAS DE LA INFORMACION'
        
        sheet['B2'].alignment = Alignment(horizontal= "left", vertical="center")
        sheet['B2'].font = Font(name = 'Arial', size= 7, bold = True)
        sheet['B2'] = 'DIRECCION REGIONAL DE SALUD JUNIN'
        
        sheet['B4'].alignment = Alignment(horizontal= "left", vertical="center")
        sheet['B4'].font = Font(name = 'Arial', size= 12, bold = True)
        sheet['B4'] = 'REPORTE DE ACTIVIDADES DEL COMPONENTE DE DISCAPACIDAD'
        
        sheet['B6'].alignment = Alignment(horizontal= "right", vertical="center")
        sheet['B6'].font = Font(name = 'Arial', size= 7, bold = True)
        sheet['B6'] ='DIRESA / GERESA / DISA:'

        sheet['B7'].alignment = Alignment(horizontal= "right", vertical="center")
        sheet['B7'].font = Font(name = 'Arial', size= 7, bold = True)
        sheet['B7'] ='HOSPITAL Y/O RED DE SALUD'
        
        sheet['F6'].alignment = Alignment(horizontal= "center", vertical="center")
        sheet['F6'].font = Font(name = 'Arial', size= 7, bold = True)
        sheet['F6'] ='PERIODO'
        
        sheet['G6'].alignment = Alignment(horizontal= "right", vertical="center")
        sheet['G6'].font = Font(name = 'Arial', size= 7, bold = True)
        sheet['G6'] ='AÑO:'
        
        sheet['G7'].alignment = Alignment(horizontal= "right", vertical="center")
        sheet['G7'].font = Font(name = 'Arial', size= 7, bold = True)
        sheet['G7'] ='MES:'
        
        sheet['H6'].alignment = Alignment(horizontal= "center", vertical="center")
        sheet['H6'].font = Font(name = 'Arial', size= 8, bold = True, color='FFFFFF')
        sheet['H6'].border = borde_plomo
        sheet['H6'] = ''
        
        sheet['H7'].alignment = Alignment(horizontal= "center", vertical="center")
        sheet['H7'].font = Font(name = 'Arial', size= 8, bold = True, color='FFFFFF')
        sheet['H7'].border = borde_plomo
        sheet['H7'] = ''
        
        sheet['B9'].alignment = Alignment(horizontal= "left", vertical="center")
        sheet['B9'].font = Font(name = 'Arial', size= 9, bold = True)
        sheet['B9'] ='PERSONAS CON DISCAPACIDAD RECIBEN ATENCION DE REHABILITACION EN ESTABLECIMIENTOS DE SALUD (3000688)'
        
        sheet['B10'].alignment = Alignment(horizontal= "left", vertical="center")
        sheet['B10'].font = Font(name = 'Arial', size= 9, bold = True)
        sheet['B10'] ='Capacitación en medicina de rehabilitación integral (5004449)'
        
        sheet['B12'].alignment = Alignment(horizontal= "right", vertical="center")
        sheet['B12'].font = Font(name = 'Arial', size= 8,)
        sheet['B12'] ='Capacitación' 
        
        sheet['C11'].alignment = Alignment(horizontal= "center", vertical="center")
        sheet['C11'].font = Font(name = 'Arial', size= 8, bold = True, color='FFFFFF')
        sheet['C11'].fill = fill
        sheet['C11'].border = border
        sheet['C11'] = 'N°'
        
        sheet['C12'].alignment = Alignment(horizontal= "center", vertical="center")
        sheet['C12'].font = Font(name = 'Arial', size= 8, bold = True, color='FFFFFF')
        sheet['C12'].border = borde_plomo
        sheet['C12'] = ''
        
        sheet['D11'].alignment = Alignment(horizontal= "center", vertical="center")
        sheet['D11'].font = Font(name = 'Arial', size= 8, bold = True, color='FFFFFF')
        sheet['D11'].fill = fill
        sheet['D11'].border = border
        sheet['D11'] = 'Capacitados'
        
        sheet['D12'].alignment = Alignment(horizontal= "center", vertical="center")
        sheet['D12'].font = Font(name = 'Arial', size= 8, bold = True, color='FFFFFF')
        sheet['D12'].border = borde_plomo
        sheet['D12'] = ''
        
        ########## DISCAPACIDAD FISICA #########################
        
        sheet['B14'].alignment = Alignment(horizontal= "left", vertical="center")
        sheet['B14'].font = Font(name = 'Arial', size= 8, bold = True)
        sheet['B14'] ='Atención de Rehabilitación en Personas con Discapacidad de Tipo Física (5005150)' 
                
        sheet['B15'].alignment = Alignment(horizontal= "center", vertical="center")
        sheet['B15'].font = Font(name = 'Arial', size= 8, bold = True, color='FFFFFF')
        sheet['B15'].fill = fill
        sheet['B15'].border = border
        sheet['B15'] = 'Atenciones'
        
        sheet['C15'].alignment = Alignment(horizontal= "center", vertical="center")
        sheet['C15'].font = Font(name = 'Arial', size= 7, bold = True, color='FFFFFF')
        sheet['C15'].fill = fill
        sheet['C15'].border = border
        sheet['C15'] = 'Total'
        
        sheet['D15'].alignment = Alignment(horizontal= "center", vertical="center", wrap_text=True)
        sheet['D15'].font = Font(name = 'Arial', size= 7, bold = True, color='FFFFFF')
        sheet['D15'].fill = fill
        sheet['D15'].border = border
        sheet['D15'] = 'Niños         (1d - 11a)'
        
        sheet['E15'].alignment = Alignment(horizontal= "center", vertical="center", wrap_text=True)
        sheet['E15'].font = Font(name = 'Arial', size= 7, bold = True,color='FFFFFF')
        sheet['E15'].fill = fill
        sheet['E15'].border = border
        sheet['E15'] = 'Adolescentes (12a - 17a)'
        
        sheet['F15'].alignment = Alignment(horizontal= "center", vertical="center", wrap_text=True)
        sheet['F15'].font = Font(name = 'Arial', size= 7, bold = True, color='FFFFFF')
        sheet['F15'].fill = fill
        sheet['F15'].border = border
        sheet['F15'] = 'Jóvenes (18a - 29a)'
        
        sheet['G15'].alignment = Alignment(horizontal= "center", vertical="center", wrap_text=True)
        sheet['G15'].font = Font(name = 'Arial', size= 7, bold = True, color='FFFFFF')
        sheet['G15'].fill = fill
        sheet['G15'].border = border
        sheet['G15'] = 'Adultos (30a - 59a)'
        
        sheet['H15'].alignment = Alignment(horizontal= "center", vertical="center", wrap_text=True)
        sheet['H15'].font = Font(name = 'Arial', size= 7, bold = True, color='FFFFFF')
        sheet['H15'].fill = fill
        sheet['H15'].border = border
        sheet['H15'] = 'A. Mayores (60a +)'
        
        #borde plomo
        for row in sheet.iter_rows(min_row=16, max_row=27, min_col=2, max_col=8):
            for cell in row:
                # Aplicar estilos de alineación a cada celda
                cell.alignment = Alignment(horizontal="center", vertical="center")
                cell.border = borde_plomo
        
        sheet['B16'].alignment = Alignment(horizontal= "left", vertical="center")
        sheet['B16'].font = Font(name = 'Arial', size= 8)
        sheet['B16'] ='Lesiones medulares (0515001)' 
        
        sheet['B17'].alignment = Alignment(horizontal= "left", vertical="center")
        sheet['B17'].font = Font(name = 'Arial', size= 8)
        sheet['B17'] ='Amputados de miembro superior (0515002)' 
        
        sheet['B18'].alignment = Alignment(horizontal= "left", vertical="center")
        sheet['B18'].font = Font(name = 'Arial', size= 8)
        sheet['B18'] ='Amputados de miembro inferior (0515003)' 
        
        sheet['B19'].alignment = Alignment(horizontal= "left", vertical="center")
        sheet['B19'].font = Font(name = 'Arial', size= 8)
        sheet['B19'] ='Enfermedad muscular y unión mioneural (0515004)' 
        
        sheet['B20'].alignment = Alignment(horizontal= "left", vertical="center")
        sheet['B20'].font = Font(name = 'Arial', size= 8)
        sheet['B20'] ='Lesiones de nervio periférico (0515005)' 
        
        sheet['B21'].alignment = Alignment(horizontal= "left", vertical="center")
        sheet['B21'].font = Font(name = 'Arial', size= 8)
        sheet['B21'] ='Trastornos del desarrollo de la función motriz (0515006)' 
        
        sheet['B22'].alignment = Alignment(horizontal= "left", vertical="center")
        sheet['B22'].font = Font(name = 'Arial', size= 8)
        sheet['B22'] ='Enfermedad articular degenerativa (0515007)' 
        
        sheet['B23'].alignment = Alignment(horizontal= "left", vertical="center")
        sheet['B23'].font = Font(name = 'Arial', size= 8)
        sheet['B23'] ='Enfermedad cerebro vascular (0515008)' 
        
        sheet['B24'].alignment = Alignment(horizontal= "left", vertical="center")
        sheet['B24'].font = Font(name = 'Arial', size= 8)
        sheet['B24'] ='Encefalopatía infantil (0515009)' 
        
        sheet['B25'].alignment = Alignment(horizontal= "left", vertical="center")
        sheet['B25'].font = Font(name = 'Arial', size= 8)
        sheet['B25'] ='Enfermedad de Parkinson (0515010)' 
        
        sheet['B26'].alignment = Alignment(horizontal= "left", vertical="center")
        sheet['B26'].font = Font(name = 'Arial', size= 8)
        sheet['B26'] ='Síndrome de Down (0515011)' 
        
        sheet['B27'].alignment = Alignment(horizontal= "left", vertical="center")
        sheet['B27'].font = Font(name = 'Arial', size= 8)
        sheet['B27'] ='Trastornos posturales (0515012)' 
        
        
        ########## DISCAPACIDAD SENSORIAL #########################
        
        sheet['B30'].alignment = Alignment(horizontal= "left", vertical="center")
        sheet['B30'].font = Font(name = 'Arial', size= 8, bold = True)
        sheet['B30'] ='Atención de Rehabilitación en Personas con Discapacidad de Tipo Sensorial (5005151)' 
                
        sheet['B31'].alignment = Alignment(horizontal= "center", vertical="center")
        sheet['B31'].font = Font(name = 'Arial', size= 8, bold = True, color='FFFFFF')
        sheet['B31'].fill = fill
        sheet['B31'].border = border
        sheet['B31'] = 'Atenciones'
        
        sheet['C31'].alignment = Alignment(horizontal= "center", vertical="center")
        sheet['C31'].font = Font(name = 'Arial', size= 7, bold = True, color='FFFFFF')
        sheet['C31'].fill = fill
        sheet['C31'].border = border
        sheet['C31'] = 'Total'
        
        sheet['D31'].alignment = Alignment(horizontal= "center", vertical="center", wrap_text=True)
        sheet['D31'].font = Font(name = 'Arial', size= 7, bold = True, color='FFFFFF')
        sheet['D31'].fill = fill
        sheet['D31'].border = border
        sheet['D31'] = 'Niños         (1d - 11a)'
        
        sheet['E31'].alignment = Alignment(horizontal= "center", vertical="center", wrap_text=True)
        sheet['E31'].font = Font(name = 'Arial', size= 7, bold = True,color='FFFFFF')
        sheet['E31'].fill = fill
        sheet['E31'].border = border
        sheet['E31'] = 'Adolescentes (12a - 17a)'
        
        sheet['F31'].alignment = Alignment(horizontal= "center", vertical="center", wrap_text=True)
        sheet['F31'].font = Font(name = 'Arial', size= 7, bold = True, color='FFFFFF')
        sheet['F31'].fill = fill
        sheet['F31'].border = border
        sheet['F31'] = 'Jóvenes (18a - 29a)'
        
        sheet['G31'].alignment = Alignment(horizontal= "center", vertical="center", wrap_text=True)
        sheet['G31'].font = Font(name = 'Arial', size= 7, bold = True, color='FFFFFF')
        sheet['G31'].fill = fill
        sheet['G31'].border = border
        sheet['G31'] = 'Adultos (30a - 59a)'
        
        sheet['H31'].alignment = Alignment(horizontal= "center", vertical="center", wrap_text=True)
        sheet['H31'].font = Font(name = 'Arial', size= 7, bold = True, color='FFFFFF')
        sheet['H31'].fill = fill
        sheet['H31'].border = border
        sheet['H31'] = 'A. Mayores (60a +)'
        
        #borde plomo
        for row in sheet.iter_rows(min_row=32, max_row=36, min_col=2, max_col=8):
            for cell in row:
                # Aplicar estilos de alineación a cada celda
                cell.alignment = Alignment(horizontal="center", vertical="center")
                cell.border = borde_plomo
        
        sheet['B32'].alignment = Alignment(horizontal= "left", vertical="center")
        sheet['B32'].font = Font(name = 'Arial', size= 8)
        sheet['B32'] ='Hipoacusia y/o sordera (0515101)' 
        
        sheet['B33'].alignment = Alignment(horizontal= "left", vertical="center")
        sheet['B33'].font = Font(name = 'Arial', size= 8)
        sheet['B33'] ='Baja visión y/o ceguera (0515102)' 
        
        sheet['B34'].alignment = Alignment(horizontal= "left", vertical="center")
        sheet['B34'].font = Font(name = 'Arial', size= 8)
        sheet['B34'] ='Sordomudez (0515103)' 
        
        sheet['B35'].alignment = Alignment(horizontal= "left", vertical="center")
        sheet['B35'].font = Font(name = 'Arial', size= 8)
        sheet['B35'] ='Parálisis cerebral infantil (0515104)' 
        
        sheet['B36'].alignment = Alignment(horizontal= "left", vertical="center")
        sheet['B36'].font = Font(name = 'Arial', size= 8)
        sheet['B36'] ='Enfermedades cerebro vasculares (0515105)' 
        
        ########## DISCAPACIDAD MENTAL #########################
        
        sheet['B39'].alignment = Alignment(horizontal= "left", vertical="center")
        sheet['B39'].font = Font(name = 'Arial', size= 8, bold = True)
        sheet['B39'] ='Atención de Rehabilitación en Personas con Discapacidad de Tipo Mental (5005152)' 
                
        sheet['B40'].alignment = Alignment(horizontal= "center", vertical="center")
        sheet['B40'].font = Font(name = 'Arial', size= 8, bold = True, color='FFFFFF')
        sheet['B40'].fill = fill
        sheet['B40'].border = border
        sheet['B40'] = 'Atenciones'
        
        sheet['C40'].alignment = Alignment(horizontal= "center", vertical="center")
        sheet['C40'].font = Font(name = 'Arial', size= 7, bold = True, color='FFFFFF')
        sheet['C40'].fill = fill
        sheet['C40'].border = border
        sheet['C40'] = 'Total'
        
        sheet['D40'].alignment = Alignment(horizontal= "center", vertical="center", wrap_text=True)
        sheet['D40'].font = Font(name = 'Arial', size= 7, bold = True, color='FFFFFF')
        sheet['D40'].fill = fill
        sheet['D40'].border = border
        sheet['D40'] = 'Niños         (1d - 11a)'
        
        sheet['E40'].alignment = Alignment(horizontal= "center", vertical="center", wrap_text=True)
        sheet['E40'].font = Font(name = 'Arial', size= 7, bold = True,color='FFFFFF')
        sheet['E40'].fill = fill
        sheet['E40'].border = border
        sheet['E40'] = 'Adolescentes (12a - 17a)'
        
        sheet['F40'].alignment = Alignment(horizontal= "center", vertical="center", wrap_text=True)
        sheet['F40'].font = Font(name = 'Arial', size= 7, bold = True, color='FFFFFF')
        sheet['F40'].fill = fill
        sheet['F40'].border = border
        sheet['F40'] = 'Jóvenes (18a - 29a)'
        
        sheet['G40'].alignment = Alignment(horizontal= "center", vertical="center", wrap_text=True)
        sheet['G40'].font = Font(name = 'Arial', size= 7, bold = True, color='FFFFFF')
        sheet['G40'].fill = fill
        sheet['G40'].border = border
        sheet['G40'] = 'Adultos (30a - 59a)'
        
        sheet['H40'].alignment = Alignment(horizontal= "center", vertical="center", wrap_text=True)
        sheet['H40'].font = Font(name = 'Arial', size= 7, bold = True, color='FFFFFF')
        sheet['H40'].fill = fill
        sheet['H40'].border = border
        sheet['H40'] = 'A. Mayores (60a +)'
        
        #borde plomo
        for row in sheet.iter_rows(min_row=41, max_row=44, min_col=2, max_col=8):
            for cell in row:
                # Aplicar estilos de alineación a cada celda
                cell.alignment = Alignment(horizontal="center", vertical="center")
                cell.border = borde_plomo
        
        sheet['B41'].alignment = Alignment(horizontal= "left", vertical="center")
        sheet['B41'].font = Font(name = 'Arial', size= 8)
        sheet['B41'] ='Trastornos de aprendizaje (0515201)' 
        
        sheet['B42'].alignment = Alignment(horizontal= "left", vertical="center")
        sheet['B42'].font = Font(name = 'Arial', size= 8)
        sheet['B42'] ='Retraso mental: leve, moderado, severo (0515202)' 
        
        sheet['B43'].alignment = Alignment(horizontal= "left", vertical="center")
        sheet['B43'].font = Font(name = 'Arial', size= 8)
        sheet['B43'] ='Trastornos del espectro autista (0515203)' 
        
        sheet['B44'].alignment = Alignment(horizontal= "left", vertical="center")
        sheet['B44'].font = Font(name = 'Arial', size= 8)
        sheet['B44'] ='Otros trastornos de salud mental (0515204)' 
        
        ########## CERTIFICACION #########################
        
        sheet['B47'].alignment = Alignment(horizontal= "left", vertical="center")
        sheet['B47'].font = Font(name = 'Arial', size= 8, bold = True)
        sheet['B47'] ='PERSONAS CON DISCAPACIDAD CERTIFICADAS EN ESTABLECIMIENTOS DE SALUD (3000689)' 
                
        sheet['B48'].alignment = Alignment(horizontal= "center", vertical="center")
        sheet['B48'].font = Font(name = 'Arial', size= 8, bold = True, color='FFFFFF')
        sheet['B48'].fill = fill
        sheet['B48'].border = border
        sheet['B48'] = 'Atenciones'
        
        sheet['C48'].alignment = Alignment(horizontal= "center", vertical="center")
        sheet['C48'].font = Font(name = 'Arial', size= 7, bold = True, color='FFFFFF')
        sheet['C48'].fill = fill
        sheet['C48'].border = border
        sheet['C48'] = 'Total'
        
        sheet['D48'].alignment = Alignment(horizontal= "center", vertical="center", wrap_text=True)
        sheet['D48'].font = Font(name = 'Arial', size= 7, bold = True, color='FFFFFF')
        sheet['D48'].fill = fill
        sheet['D48'].border = border
        sheet['D48'] = 'Niños         (1d - 11a)'
        
        sheet['E48'].alignment = Alignment(horizontal= "center", vertical="center", wrap_text=True)
        sheet['E48'].font = Font(name = 'Arial', size= 7, bold = True,color='FFFFFF')
        sheet['E48'].fill = fill
        sheet['E48'].border = border
        sheet['E48'] = 'Adolescentes (12a - 17a)'
        
        sheet['F48'].alignment = Alignment(horizontal= "center", vertical="center", wrap_text=True)
        sheet['F48'].font = Font(name = 'Arial', size= 7, bold = True, color='FFFFFF')
        sheet['F48'].fill = fill
        sheet['F48'].border = border
        sheet['F48'] = 'Jóvenes (18a - 29a)'
        
        sheet['G48'].alignment = Alignment(horizontal= "center", vertical="center", wrap_text=True)
        sheet['G48'].font = Font(name = 'Arial', size= 7, bold = True, color='FFFFFF')
        sheet['G48'].fill = fill
        sheet['G48'].border = border
        sheet['G48'] = 'Adultos (30a - 59a)'
        
        sheet['H48'].alignment = Alignment(horizontal= "center", vertical="center", wrap_text=True)
        sheet['H48'].font = Font(name = 'Arial', size= 7, bold = True, color='FFFFFF')
        sheet['H48'].fill = fill
        sheet['H48'].border = border
        sheet['H48'] = 'A. Mayores (60a +)'
        
        #borde plomo
        for row in sheet.iter_rows(min_row=49, max_row=50, min_col=2, max_col=8):
            for cell in row:
                # Aplicar estilos de alineación a cada celda
                cell.alignment = Alignment(horizontal="center", vertical="center")
                cell.border = borde_plomo
        
        sheet['B49'].alignment = Alignment(horizontal= "left", vertical="center")
        sheet['B49'].font = Font(name = 'Arial', size= 8)
        sheet['B49'] ='Certificación de Discapacidad (0515204)' 
        
        sheet['B50'].alignment = Alignment(horizontal= "left", vertical="center")
        sheet['B50'].font = Font(name = 'Arial', size= 8)
        sheet['B50'] ='Certificación de Incapacidad (0515205)' 
        
        ########## VISITAS RBC #########################
        
        sheet['B52'].alignment = Alignment(horizontal= "left", vertical="center")
        sheet['B52'].font = Font(name = 'Arial', size= 8, bold = True)
        sheet['B52'] ='PERSONAS CON DISCAPACIDAD RECIBEN SERVICIOS DE REHABILITACIÓN BASADA EN LA COMUNIDAD (3000690)' 
                
        sheet['B53'].alignment = Alignment(horizontal= "center", vertical="center")
        sheet['B53'].font = Font(name = 'Arial', size= 8, bold = True, color='FFFFFF')
        sheet['B53'].fill = fill
        sheet['B53'].border = border
        sheet['B53'] = 'Visitas'
        
        sheet['C53'].alignment = Alignment(horizontal= "center", vertical="center")
        sheet['C53'].font = Font(name = 'Arial', size= 7, bold = True, color='FFFFFF')
        sheet['C53'].fill = fill
        sheet['C53'].border = border
        sheet['C53'] = 'Total'
        
        sheet['D53'].alignment = Alignment(horizontal= "center", vertical="center", wrap_text=True)
        sheet['D53'].font = Font(name = 'Arial', size= 7, bold = True, color='FFFFFF')
        sheet['D53'].fill = fill
        sheet['D53'].border = border
        sheet['D53'] = 'Niños         (1d - 11a)'
        
        sheet['E53'].alignment = Alignment(horizontal= "center", vertical="center", wrap_text=True)
        sheet['E53'].font = Font(name = 'Arial', size= 7, bold = True,color='FFFFFF')
        sheet['E53'].fill = fill
        sheet['E53'].border = border
        sheet['E53'] = 'Adolescentes (12a - 17a)'
        
        sheet['F53'].alignment = Alignment(horizontal= "center", vertical="center", wrap_text=True)
        sheet['F53'].font = Font(name = 'Arial', size= 7, bold = True, color='FFFFFF')
        sheet['F53'].fill = fill
        sheet['F53'].border = border
        sheet['F53'] = 'Jóvenes (18a - 29a)'
        
        sheet['G53'].alignment = Alignment(horizontal= "center", vertical="center", wrap_text=True)
        sheet['G53'].font = Font(name = 'Arial', size= 7, bold = True, color='FFFFFF')
        sheet['G53'].fill = fill
        sheet['G53'].border = border
        sheet['G53'] = 'Adultos (30a - 59a)'
        
        sheet['H53'].alignment = Alignment(horizontal= "center", vertical="center", wrap_text=True)
        sheet['H53'].font = Font(name = 'Arial', size= 7, bold = True, color='FFFFFF')
        sheet['H53'].fill = fill
        sheet['H53'].border = border
        sheet['H53'] = 'A. Mayores (60a +)'
        
        #borde plomo
        for row in sheet.iter_rows(min_row=54, max_row=57, min_col=2, max_col=8):
            for cell in row:
                # Aplicar estilos de alineación a cada celda
                cell.alignment = Alignment(horizontal="center", vertical="center")
                cell.border = borde_plomo
        
        sheet['B54'].alignment = Alignment(horizontal= "left", vertical="center")
        sheet['B54'].font = Font(name = 'Arial', size= 8)
        sheet['B54'] ='1º Visita' 
        
        sheet['B55'].alignment = Alignment(horizontal= "left", vertical="center")
        sheet['B55'].font = Font(name = 'Arial', size= 8)
        sheet['B55'] ='2º Visita' 
        
        sheet['B56'].alignment = Alignment(horizontal= "left", vertical="center")
        sheet['B56'].font = Font(name = 'Arial', size= 8)
        sheet['B56'] ='3º Visita' 
        
        sheet['B57'].alignment = Alignment(horizontal= "left", vertical="center")
        sheet['B57'].font = Font(name = 'Arial', size= 8)
        sheet['B57'] ='4º a + Visitas' 
        
        # cambina celdas
        sheet.merge_cells('C6:D6')
        sheet.merge_cells('C7:D7')
        
        # Definir ubicaciones específicas para cada columna y su suma total
        columnas_ubicaciones = {
            'PROVINCIA': 'D10',
            'DIS_1': 'D16', 
            'DIS_2': 'E16',
            'DIS_3': 'F16',
            'DIS_4': 'G16',
            'DIS_5': 'H16'
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
