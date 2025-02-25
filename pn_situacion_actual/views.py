import logging
from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import render
from .queries import obtener_distritos, obtener_avance_situacion_padron, obtener_cumple_situacion_cnv, obtener_cumple_situacion_dni
from .queries import obtener_cumple_situacion_eje_vial, obtener_cumple_situacion_direccion, obtener_cumple_situacion_referencia, obtener_cumple_situacion_visitado
from .queries import obtener_cumple_situacion_encontrado, obtener_cumple_situacion_celular, obtener_cumple_situacion_sexo, obtener_cumple_situacion_seguro
from .queries import obtener_cumple_situacion_eess, obtener_cumple_situacion_frecuencia, obtener_cumple_situacion_direccion_completa, obtener_cumple_situacion_visitado_no_encontrado

from base.models import MAESTRO_HIS_ESTABLECIMIENTO, DimPeriodo, Actualizacion

logger = logging.getLogger(__name__)

from django.db.models.functions import Substr

def get_distritos(request, distrito):
    provincia = (
                MAESTRO_HIS_ESTABLECIMIENTO
                .objects.filter(Descripcion_Sector='GOBIERNO REGIONAL')
                .annotate(ubigueo_filtrado=Substr('Ubigueo_Establecimiento', 1, 4))
                .values('Provincia','ubigueo_filtrado')
                .distinct()
                .order_by('Provincia')
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
                'provincia': provincia,
                'mes_inicio':mes_inicio,
                'mes_fin':mes_fin,
    }
    return render(request, 'discapacidad/distritos.html', context)

## PANTALLA PRINCIPAL
def index_situacion_padron(request):
    actualizacion = Actualizacion.objects.all()

    ## muestra las provincias
    provincias = MAESTRO_HIS_ESTABLECIMIENTO.objects.values_list('Provincia', flat=True).distinct().order_by('Provincia')
    
    ## obtiene la provincia seleccionada
    provincia_seleccionada = request.GET.get('provincia','JUNIN')
    
    distrito_seleccionado = request.GET.get('distrito')

    print(provincia_seleccionada)
    print(distrito_seleccionado)
    
    # Si la solicitud es AJAX/Validamos si es AJAX
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            # Verificar si se solicitan distritos
            if 'get_distritos' in request.GET:
                distritos = obtener_distritos(provincia_seleccionada)
                return JsonResponse(distritos, safe=False)
            
            print(distritos)
            # AVANCE GRAFICO POR EDAD 
            resultados_avance_situacion_padron = obtener_avance_situacion_padron(provincia_seleccionada, distrito_seleccionado)
            # AVANCE POR CNV 
            resultados_cumple_situacion_cnv = obtener_cumple_situacion_cnv(provincia_seleccionada, distrito_seleccionado)
            # AVANCE POR DNI 
            resultados_cumple_situacion_dni = obtener_cumple_situacion_dni(provincia_seleccionada, distrito_seleccionado)
            # AVANCE POR DNI 
            resultados_cumple_situacion_eje_vial = obtener_cumple_situacion_eje_vial(provincia_seleccionada, distrito_seleccionado)
            # AVANCE POR DNI 
            resultados_cumple_situacion_direccion = obtener_cumple_situacion_direccion(provincia_seleccionada, distrito_seleccionado)
            # AVANCE POR DNI 
            resultados_cumple_situacion_referencia = obtener_cumple_situacion_referencia(provincia_seleccionada, distrito_seleccionado)
            # AVANCE POR DNI 
            resultados_cumple_situacion_visitado = obtener_cumple_situacion_visitado(provincia_seleccionada, distrito_seleccionado)
            # AVANCE POR DNI 
            resultados_cumple_situacion_encontrado = obtener_cumple_situacion_encontrado(provincia_seleccionada, distrito_seleccionado)
            # AVANCE POR DNI 
            resultados_cumple_situacion_celular = obtener_cumple_situacion_celular(provincia_seleccionada, distrito_seleccionado)
            # AVANCE POR DNI 
            resultados_cumple_situacion_sexo = obtener_cumple_situacion_sexo(provincia_seleccionada, distrito_seleccionado)
            # AVANCE POR DNI 
            resultados_cumple_situacion_seguro = obtener_cumple_situacion_seguro(provincia_seleccionada, distrito_seleccionado)
            # AVANCE POR DNI 
            resultados_cumple_situacion_eess = obtener_cumple_situacion_eess(provincia_seleccionada, distrito_seleccionado)
            # AVANCE POR DNI 
            resultados_cumple_situacion_frecuencia = obtener_cumple_situacion_frecuencia(provincia_seleccionada, distrito_seleccionado)
            # AVANCE POR DNI 
            resultados_cumple_situacion_direccion_completa = obtener_cumple_situacion_direccion_completa(provincia_seleccionada, distrito_seleccionado)
            # AVANCE POR DNI 
            resultados_cumple_situacion_visitado_no_encontrado = obtener_cumple_situacion_visitado_no_encontrado(provincia_seleccionada, distrito_seleccionado)

            data = {    
                
                # AVANCE GRAFICO POR EDAD           
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
                
                # CUMPLE CNV
                'total_cumple_cnv': [],
                'brecha_cumple_cnv': [],
                'cob_cnv': [],
                
                # CUMPLE DNI
                'total_cumple_dni': [],
                'brecha_cumple_dni': [],
                'cob_dni': [],
                
                # CUMPLE EJE VIAL                
                'total_cumple_eje_vial': [],
                'brecha_eje_vial': [],
                'cob_eje_vial': [],
                
                # CUMPLE DIRECCION
                'total_cumple_direccion': [],
                'brecha_direccion': [],
                'cob_direccion': [],
                
                
                'total_cumple_referencia': [],
                'brecha_referencia': [],
                'cob_referencia': [],
                
                'total_cumple_visitado': [],
                'brecha_visitado': [],
                'cob_visitado': [],
                
                'total_cumple_encontrado': [],
                'brecha_encontrado': [],
                'cob_encontrado': [],
                
                'total_cumple_celular': [],
                'brecha_celular': [],
                'cob_celular': [],
                
                'total_cumple_sexo_masculino': [],
                'total_cumple_sexo_femenino': [],
                'cob_sexo': [],
                
                'total_cumple_seguro': [],
                'brecha_seguro': [],
                'cob_seguro': [],
                
                'total_eess': [],
                'brecha_eess': [],
                'cob_eess': [],
                
                'total_frecuencia': [],
                'brecha_frecuencia': [],
                'cob_frecuencia': [],
                
                'total_direccion_completa': [],
                'brecha_direccion_completa': [],
                'cob_direccion_completa': [],
                
                'total_visitado_no_encontrado': [],
                'brecha_visitado_no_encontrado': [],
                'cob_visitado_no_encontrado': [],
                
            }
            
            #AVANCE GRAFICO MESES
            for index, row in enumerate(resultados_avance_situacion_padron):
                try:
                    # Verifica que la tupla tenga exactamente 4 elementos
                    if len(row) != 10:
                        raise ValueError(f"La fila {index} no tiene 14 elementos: {row}")

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

                except Exception as e:
                    logger.error(f"Error procesando la fila {index}: {str(e)}")
            
            #CUMPLE CNV
            for index, row in enumerate(resultados_cumple_situacion_cnv):
                try:
                    # Verifica que la tupla tenga exactamente 4 elementos
                    if len(row) != 3:
                        raise ValueError(f"La fila {index} no tiene 14 elementos: {row}")

                    data['total_cumple_cnv'].append(row[0])
                    data['brecha_cumple_cnv'].append(row[1])
                    data['cob_cnv'].append(row[2])

                except Exception as e:
                    logger.error(f"Error procesando la fila {index}: {str(e)}")
            
            #CUMPLE DNI
            for index, row in enumerate(resultados_cumple_situacion_dni):
                try:
                    # Verifica que la tupla tenga exactamente 4 elementos
                    if len(row) != 3:
                        raise ValueError(f"La fila {index} no tiene 14 elementos: {row}")

                    data['total_cumple_dni'].append(row[0])
                    data['brecha_cumple_dni'].append(row[1])
                    data['cob_dni'].append(row[2])

                except Exception as e:
                    logger.error(f"Error procesando la fila {index}: {str(e)}")
            
            #CUMPLE EJE VIAL
            for index, row in enumerate(resultados_cumple_situacion_eje_vial):
                try:
                    # Verifica que la tupla tenga exactamente 4 elementos
                    if len(row) != 3:
                        raise ValueError(f"La fila {index} no tiene 14 elementos: {row}")

                    data['total_cumple_eje_vial'].append(row[0])
                    data['brecha_eje_vial'].append(row[1])
                    data['cob_eje_vial'].append(row[2])

                except Exception as e:
                    logger.error(f"Error procesando la fila {index}: {str(e)}")
            
            #CUMPLE DIRECCION
            for index, row in enumerate(resultados_cumple_situacion_direccion):
                try:
                    # Verifica que la tupla tenga exactamente 4 elementos
                    if len(row) != 3:
                        raise ValueError(f"La fila {index} no tiene 14 elementos: {row}")

                    data['total_cumple_direccion'].append(row[0])
                    data['brecha_direccion'].append(row[1])
                    data['cob_direccion'].append(row[2])

                except Exception as e:
                    logger.error(f"Error procesando la fila {index}: {str(e)}")
                    
            #CUMPLE REFERENCIA
            for index, row in enumerate(resultados_cumple_situacion_referencia):
                try:
                    # Verifica que la tupla tenga exactamente 4 elementos
                    if len(row) != 3:
                        raise ValueError(f"La fila {index} no tiene 14 elementos: {row}")

                    data['total_cumple_referencia'].append(row[0])
                    data['brecha_referencia'].append(row[1])
                    data['cob_referencia'].append(row[2])

                except Exception as e:
                    logger.error(f"Error procesando la fila {index}: {str(e)}")
                    
            #CUMPLE VISITADO
            for index, row in enumerate(resultados_cumple_situacion_visitado):
                try:
                    # Verifica que la tupla tenga exactamente 4 elementos
                    if len(row) != 3:
                        raise ValueError(f"La fila {index} no tiene 14 elementos: {row}")

                    data['total_cumple_visitado'].append(row[0])
                    data['brecha_visitado'].append(row[1])
                    data['cob_visitado'].append(row[2])

                except Exception as e:
                    logger.error(f"Error procesando la fila {index}: {str(e)}")
                    
            
            #CUMPLE ENCONTRADO
            for index, row in enumerate(resultados_cumple_situacion_encontrado):
                try:
                    # Verifica que la tupla tenga exactamente 4 elementos
                    if len(row) != 3:
                        raise ValueError(f"La fila {index} no tiene 14 elementos: {row}")

                    data['total_cumple_encontrado'].append(row[0])
                    data['brecha_encontrado'].append(row[1])
                    data['cob_encontrado'].append(row[2])

                except Exception as e:
                    logger.error(f"Error procesando la fila {index}: {str(e)}")
                    
                    
            #CUMPLE CELULAR
            for index, row in enumerate(resultados_cumple_situacion_celular):
                try:
                    # Verifica que la tupla tenga exactamente 4 elementos
                    if len(row) != 3:
                        raise ValueError(f"La fila {index} no tiene 14 elementos: {row}")

                    data['total_cumple_celular'].append(row[0])
                    data['brecha_celular'].append(row[1])
                    data['cob_celular'].append(row[2])

                except Exception as e:
                    logger.error(f"Error procesando la fila {index}: {str(e)}")
                    
                    
            #CUMPLE SEXO
            for index, row in enumerate(resultados_cumple_situacion_sexo):
                try:
                    # Verifica que la tupla tenga exactamente 4 elementos
                    if len(row) != 3:
                        raise ValueError(f"La fila {index} no tiene 14 elementos: {row}")

                    data['total_cumple_sexo_masculino'].append(row[0])
                    data['total_cumple_sexo_femenino'].append(row[1])
                    data['cob_sexo'].append(row[2])

                except Exception as e:
                    logger.error(f"Error procesando la fila {index}: {str(e)}")
                    
                    
            #CUMPLE SEGURO
            for index, row in enumerate(resultados_cumple_situacion_seguro):
                try:
                    # Verifica que la tupla tenga exactamente 4 elementos
                    if len(row) != 3:
                        raise ValueError(f"La fila {index} no tiene 14 elementos: {row}")

                    data['total_cumple_seguro'].append(row[0])
                    data['brecha_seguro'].append(row[1])
                    data['cob_seguro'].append(row[2])

                except Exception as e:
                    logger.error(f"Error procesando la fila {index}: {str(e)}")
                    
                    
            #CUMPLE EESS
            for index, row in enumerate(resultados_cumple_situacion_eess):
                try:
                    # Verifica que la tupla tenga exactamente 4 elementos
                    if len(row) != 3:
                        raise ValueError(f"La fila {index} no tiene 14 elementos: {row}")

                    data['total_eess'].append(row[0])
                    data['brecha_eess'].append(row[1])
                    data['cob_eess'].append(row[2])

                except Exception as e:
                    logger.error(f"Error procesando la fila {index}: {str(e)}")
                    
                    
            #CUMPLE FRECUENCIA
            for index, row in enumerate(resultados_cumple_situacion_frecuencia):
                try:
                    # Verifica que la tupla tenga exactamente 4 elementos
                    if len(row) != 3:
                        raise ValueError(f"La fila {index} no tiene 14 elementos: {row}")

                    data['total_frecuencia'].append(row[0])
                    data['brecha_frecuencia'].append(row[1])
                    data['cob_frecuencia'].append(row[2])

                except Exception as e:
                    logger.error(f"Error procesando la fila {index}: {str(e)}")
                    
                    
                    
            #CUMPLE DIRECCION COMPLETA
            for index, row in enumerate(resultados_cumple_situacion_direccion_completa):
                try:
                    # Verifica que la tupla tenga exactamente 4 elementos
                    if len(row) != 3:
                        raise ValueError(f"La fila {index} no tiene 14 elementos: {row}")

                    data['total_direccion_completa'].append(row[0])
                    data['brecha_direccion_completa'].append(row[1])
                    data['cob_direccion_completa'].append(row[2])

                except Exception as e:
                    logger.error(f"Error procesando la fila {index}: {str(e)}")
                    
                    
            #CUMPLE VISITADO NO ENCONTRADO
            for index, row in enumerate(resultados_cumple_situacion_visitado_no_encontrado):
                try:
                    # Verifica que la tupla tenga exactamente 4 elementos
                    if len(row) != 3:
                        raise ValueError(f"La fila {index} no tiene 14 elementos: {row}")

                    data['total_visitado_no_encontrado'].append(row[0])
                    data['brecha_visitado_no_encontrado'].append(row[1])
                    data['cob_visitado_no_encontrado'].append(row[2])

                except Exception as e:
                    logger.error(f"Error procesando la fila {index}: {str(e)}")
            
            return JsonResponse(data)

        except Exception as e:
            logger.error(f"Error al obtener datos: {str(e)}")

    # Si no es una solicitud AJAX, renderiza la página principal
    return render(request, 'pn_situacion_actual/index_pn_situacion_actual.html', {
        'actualizacion': actualizacion,
        'provincias': provincias,
    })

