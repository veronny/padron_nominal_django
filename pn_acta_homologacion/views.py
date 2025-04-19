import logging
from django.shortcuts import render
from django.http import JsonResponse
from .queries import (obtener_tabla_acta,obtener_distritos, obtener_provincias)

from base.models import MAESTRO_HIS_ESTABLECIMIENTO, Actualizacion

from django.db.models.functions import Substr

from django.db import connection
from django.http import JsonResponse
from base.models import MAESTRO_HIS_ESTABLECIMIENTO, DimPeriodo, Actualizacion
from django.db.models.functions import Substr

# REPORTE EXCEL
from django.http.response import HttpResponse
from django.views.generic.base import TemplateView
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
import openpyxl
from openpyxl.utils import get_column_letter

from django.db.models.functions import Substr

from datetime import datetime
import locale

from django.db.models import IntegerField  # Importar IntegerField
from django.db.models.functions import Cast, Substr  # Importar Cast y Substr
# linea de border 
from openpyxl.utils import column_index_from_string

# Reporte excel
from datetime import datetime
import getpass  # Para obtener el nombre del usuario
from django.contrib.auth.models import User  # O tu modelo de usuario personalizado
from django.http import HttpResponse
from io import BytesIO
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

User = get_user_model()

from django.db.models import IntegerField             # Importar IntegerField
from django.db.models.functions import Cast, Substr     # Importar Cast y Substr

logger = logging.getLogger(__name__)


def index_acta_padron(request):
    actualizacion = Actualizacion.objects.all()

    # Provincias para el primer <select>
    provincias = (MAESTRO_HIS_ESTABLECIMIENTO.objects
                    .values_list('Provincia', flat=True)
                    .distinct()
                    .order_by('Provincia'))
    
    # Obtener parámetros
    departamento_selecionado = request.GET.get('departamento')
    provincia_seleccionada = request.GET.get('provincia')
    distrito_seleccionado = request.GET.get('distrito')

    # -- Manejo de distritos via HTMX (retorna template parcial) --
    if 'get_distritos' in request.GET:
        if provincia_seleccionada:
            distritos = obtener_distritos(provincia_seleccionada)
        else:
            distritos = []
        
        return render(request, "pn_situacion_actual/partials/_distritos_options.html", {
            "distritos": distritos
        })

    # -- Si es una solicitud AJAX, devolvemos JsonResponse con la data --
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # Intentamos procesar la data sin mostrar errores
        try:
            # Llamada redundante a get_distritos (por si la plantilla antigua lo usara)
            if 'get_distritos' in request.GET:
                distritos = obtener_distritos(provincia_seleccionada)
                return JsonResponse(distritos, safe=False)
            
            # AVANCE GRAFICO POR EDAD
            resultados_tabla_acta = obtener_tabla_acta(
                departamento_selecionado, provincia_seleccionada, distrito_seleccionado
            )

            # Estructura de datos inicial
            data = {
                # EDAD
                'departamento': [],
                'provincia': [],
                'distrito': [],
                'municipio': [],
                'mes_enero': [],
                'mes_febrero': [],
                'mes_marzo': [],
                'mes_abril': [],
                'mes_mayo': [],
                'mes_junio': [],
                'mes_julio': [],
                'mes_agosto': [],
                'mes_septiembre': [],
                'mes_octubre': [],
                'mes_noviembre': [],
                'mes_diciembre': []
            }

            # ----------------------------------------------------------------------------
            # 1) Avance Situacion Padron (EDAD)
            # ----------------------------------------------------------------------------
            for row in resultados_tabla_acta:
                # En lugar de lanzar error, checamos si la tupla es la longitud esperada:
                if len(row) == 16:
                    data['departamento'].append(row[0])
                    data['provincia'].append(row[1])
                    data['distrito'].append(row[2])
                    data['municipio'].append(row[3])
                    
                    # Convertir fechas a string y manejar None
                    data['mes_enero'].append(str(row[4]) if row[4] else None)
                    data['mes_febrero'].append(str(row[5]) if row[5] else None)
                    data['mes_marzo'].append(str(row[6]) if row[6] else None)
                    data['mes_abril'].append(str(row[7]) if row[7] else None)
                    data['mes_mayo'].append(str(row[8]) if row[8] else None)
                    data['mes_junio'].append(str(row[9]) if row[9] else None)
                    data['mes_julio'].append(str(row[10]) if row[10] else None)
                    data['mes_agosto'].append(str(row[11]) if row[11] else None)
                    data['mes_septiembre'].append(str(row[12]) if row[12] else None)
                    data['mes_octubre'].append(str(row[13]) if row[13] else None)
                    data['mes_noviembre'].append(str(row[14]) if row[14] else None)
                    data['mes_diciembre'].append(str(row[15]) if row[15] else None)
                else:
                    logger.warning(f"Fila con estructura inválida: {row}")
                    print("Ejemplo de datos enviados:", {k: v[:2] for k, v in data.items() if v})
            return JsonResponse(data)
        except:
            # Si ocurre alguna excepción global, la silenciamos (no mostramos nada)
            return JsonResponse({}, status=200)

    # -- Si no es AJAX, render normal de la plantilla --
    return render(request, 'pn_acta_homologacion/index_pn_acta_homologacion.html', {
        'actualizacion': actualizacion,
        'provincias': provincias,
    })
