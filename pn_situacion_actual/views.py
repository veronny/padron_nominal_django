import logging
from django.shortcuts import render
from django.http import JsonResponse
from .queries import (obtener_distritos, obtener_avance_situacion_padron, obtener_cumple_situacion_cnv,
                      obtener_cumple_situacion_dni, obtener_cumple_situacion_eje_vial,
                      obtener_cumple_situacion_direccion, obtener_cumple_situacion_referencia,
                      obtener_cumple_situacion_visitado, obtener_cumple_situacion_encontrado,
                      obtener_cumple_situacion_celular, obtener_cumple_situacion_sexo,
                      obtener_cumple_situacion_seguro, obtener_cumple_situacion_eess,
                      obtener_cumple_situacion_frecuencia, obtener_cumple_situacion_direccion_completa,
                      obtener_cumple_situacion_visitado_no_encontrado)

from base.models import MAESTRO_HIS_ESTABLECIMIENTO, Actualizacion

logger = logging.getLogger(__name__)

from django.db.models.functions import Substr

def index_situacion_padron(request):
    actualizacion = Actualizacion.objects.all()

    # Provincias para el primer <select>
    provincias = (MAESTRO_HIS_ESTABLECIMIENTO.objects
                  .values_list('Provincia', flat=True)
                  .distinct()
                  .order_by('Provincia'))
    
    # Obtener parámetros
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
            resultados_avance_situacion_padron = obtener_avance_situacion_padron(
                provincia_seleccionada, distrito_seleccionado
            )
            # AVANCE POR CNV
            resultados_cumple_situacion_cnv = obtener_cumple_situacion_cnv(
                provincia_seleccionada, distrito_seleccionado
            )
            # (y así con el resto de consultas...)
            resultados_cumple_situacion_dni = obtener_cumple_situacion_dni(
                provincia_seleccionada, distrito_seleccionado
            )
            resultados_cumple_situacion_eje_vial = obtener_cumple_situacion_eje_vial(
                provincia_seleccionada, distrito_seleccionado
            )
            resultados_cumple_situacion_direccion = obtener_cumple_situacion_direccion(
                provincia_seleccionada, distrito_seleccionado
            )
            resultados_cumple_situacion_referencia = obtener_cumple_situacion_referencia(
                provincia_seleccionada, distrito_seleccionado
            )
            resultados_cumple_situacion_visitado = obtener_cumple_situacion_visitado(
                provincia_seleccionada, distrito_seleccionado
            )
            resultados_cumple_situacion_encontrado = obtener_cumple_situacion_encontrado(
                provincia_seleccionada, distrito_seleccionado
            )
            resultados_cumple_situacion_celular = obtener_cumple_situacion_celular(
                provincia_seleccionada, distrito_seleccionado
            )
            resultados_cumple_situacion_sexo = obtener_cumple_situacion_sexo(
                provincia_seleccionada, distrito_seleccionado
            )
            resultados_cumple_situacion_seguro = obtener_cumple_situacion_seguro(
                provincia_seleccionada, distrito_seleccionado
            )
            resultados_cumple_situacion_eess = obtener_cumple_situacion_eess(
                provincia_seleccionada, distrito_seleccionado
            )
            resultados_cumple_situacion_frecuencia = obtener_cumple_situacion_frecuencia(
                provincia_seleccionada, distrito_seleccionado
            )
            resultados_cumple_situacion_direccion_completa = obtener_cumple_situacion_direccion_completa(
                provincia_seleccionada, distrito_seleccionado
            )
            resultados_cumple_situacion_visitado_no_encontrado = obtener_cumple_situacion_visitado_no_encontrado(
                provincia_seleccionada, distrito_seleccionado
            )

            # Estructura de datos inicial
            data = {
                # EDAD
                'N28_dias': [],
                'N0a5meses': [],
                'N6a11meses': [],
                'cero_anios': [],
                'un_anios': [],
                'dos_anios': [],
                'tres_anios': [],
                'cuatro_anios': [],
                'cinco_anios': [],
                'total_den': [],
                # CNV
                'total_cumple_cnv': [],
                'brecha_cumple_cnv': [],
                'cob_cnv': [],
                # DNI
                'total_cumple_dni': [],
                'brecha_cumple_dni': [],
                'cob_dni': [],
                # EJE VIAL
                'total_cumple_eje_vial': [],
                'brecha_eje_vial': [],
                'cob_eje_vial': [],
                # DIRECCION
                'total_cumple_direccion': [],
                'brecha_direccion': [],
                'cob_direccion': [],
                # REFERENCIA
                'total_cumple_referencia': [],
                'brecha_referencia': [],
                'cob_referencia': [],
                # VISITADO
                'total_cumple_visitado': [],
                'brecha_visitado': [],
                'cob_visitado': [],
                # ENCONTRADO
                'total_cumple_encontrado': [],
                'brecha_encontrado': [],
                'cob_encontrado': [],
                # CELULAR
                'total_cumple_celular': [],
                'brecha_celular': [],
                'cob_celular': [],
                # SEXO
                'total_cumple_sexo_masculino': [],
                'total_cumple_sexo_femenino': [],
                'cob_sexo': [],
                # SEGURO
                'total_cumple_seguro': [],
                'brecha_seguro': [],
                'cob_seguro': [],
                # EESS
                'total_eess': [],
                'brecha_eess': [],
                'cob_eess': [],
                # FRECUENCIA
                'total_frecuencia': [],
                'brecha_frecuencia': [],
                'cob_frecuencia': [],
                # DIRECCION COMPLETA
                'total_direccion_completa': [],
                'brecha_direccion_completa': [],
                'cob_direccion_completa': [],
                # VISITADO NO ENCONTRADO
                'total_visitado_no_encontrado': [],
                'brecha_visitado_no_encontrado': [],
                'cob_visitado_no_encontrado': [],
            }

            # ----------------------------------------------------------------------------
            # 1) Avance Situacion Padron (EDAD)
            # ----------------------------------------------------------------------------
            for row in resultados_avance_situacion_padron:
                # En lugar de lanzar error, checamos si la tupla es la longitud esperada:
                if len(row) == 10:
                    data['N28_dias'].append(row[0])
                    data['N0a5meses'].append(row[1])
                    data['N6a11meses'].append(row[2])
                    data['cero_anios'].append(row[3])
                    data['un_anios'].append(row[4])
                    data['dos_anios'].append(row[5])
                    data['tres_anios'].append(row[6])
                    data['cuatro_anios'].append(row[7])
                    data['cinco_anios'].append(row[8])
                    data['total_den'].append(row[9])
                # Si no, lo ignoramos silenciosamente

            # ----------------------------------------------------------------------------
            # 2) CNV
            # ----------------------------------------------------------------------------
            for row in resultados_cumple_situacion_cnv:
                if len(row) == 3:
                    data['total_cumple_cnv'].append(row[0])
                    data['brecha_cumple_cnv'].append(row[1])
                    data['cob_cnv'].append(row[2])
                # Si no, no hacemos nada

            # ----------------------------------------------------------------------------
            # 3) DNI
            # ----------------------------------------------------------------------------
            for row in resultados_cumple_situacion_dni:
                if len(row) == 3:
                    data['total_cumple_dni'].append(row[0])
                    data['brecha_cumple_dni'].append(row[1])
                    data['cob_dni'].append(row[2])

            # (Repite el mismo patrón para eje vial, direccion, referencia, etc.)
            # ----------------------------------------------------------------------------
            for row in resultados_cumple_situacion_eje_vial:
                if len(row) == 3:
                    data['total_cumple_eje_vial'].append(row[0])
                    data['brecha_eje_vial'].append(row[1])
                    data['cob_eje_vial'].append(row[2])

            for row in resultados_cumple_situacion_direccion:
                if len(row) == 3:
                    data['total_cumple_direccion'].append(row[0])
                    data['brecha_direccion'].append(row[1])
                    data['cob_direccion'].append(row[2])

            for row in resultados_cumple_situacion_referencia:
                if len(row) == 3:
                    data['total_cumple_referencia'].append(row[0])
                    data['brecha_referencia'].append(row[1])
                    data['cob_referencia'].append(row[2])

            for row in resultados_cumple_situacion_visitado:
                if len(row) == 3:
                    data['total_cumple_visitado'].append(row[0])
                    data['brecha_visitado'].append(row[1])
                    data['cob_visitado'].append(row[2])

            for row in resultados_cumple_situacion_encontrado:
                if len(row) == 3:
                    data['total_cumple_encontrado'].append(row[0])
                    data['brecha_encontrado'].append(row[1])
                    data['cob_encontrado'].append(row[2])

            for row in resultados_cumple_situacion_celular:
                if len(row) == 3:
                    data['total_cumple_celular'].append(row[0])
                    data['brecha_celular'].append(row[1])
                    data['cob_celular'].append(row[2])

            for row in resultados_cumple_situacion_sexo:
                if len(row) == 3:
                    data['total_cumple_sexo_masculino'].append(row[0])
                    data['total_cumple_sexo_femenino'].append(row[1])
                    data['cob_sexo'].append(row[2])

            for row in resultados_cumple_situacion_seguro:
                if len(row) == 3:
                    data['total_cumple_seguro'].append(row[0])
                    data['brecha_seguro'].append(row[1])
                    data['cob_seguro'].append(row[2])

            for row in resultados_cumple_situacion_eess:
                if len(row) == 3:
                    data['total_eess'].append(row[0])
                    data['brecha_eess'].append(row[1])
                    data['cob_eess'].append(row[2])

            for row in resultados_cumple_situacion_frecuencia:
                if len(row) == 3:
                    data['total_frecuencia'].append(row[0])
                    data['brecha_frecuencia'].append(row[1])
                    data['cob_frecuencia'].append(row[2])

            for row in resultados_cumple_situacion_direccion_completa:
                if len(row) == 3:
                    data['total_direccion_completa'].append(row[0])
                    data['brecha_direccion_completa'].append(row[1])
                    data['cob_direccion_completa'].append(row[2])

            for row in resultados_cumple_situacion_visitado_no_encontrado:
                if len(row) == 3:
                    data['total_visitado_no_encontrado'].append(row[0])
                    data['brecha_visitado_no_encontrado'].append(row[1])
                    data['cob_visitado_no_encontrado'].append(row[2])

            return JsonResponse(data)

        except:
            # Si ocurre alguna excepción global, la silenciamos (no mostramos nada)
            return JsonResponse({}, status=200)

    # -- Si no es AJAX, render normal de la plantilla --
    return render(request, 'pn_situacion_actual/index_pn_situacion_actual.html', {
        'actualizacion': actualizacion,
        'provincias': provincias,
    })
