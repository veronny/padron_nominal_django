from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect

# DIRECTORIO MUNICIPIO 
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from .padron_models import Directorio_municipio, Directorio_salud
from .forms import Directorio_MunicipioForm , Directorio_SaludForm

# TABLERO SELLO 
from django.db import connection
from django.http import JsonResponse
from base.models import MAESTRO_HIS_ESTABLECIMIENTO, DimPeriodo
from django.db.models.functions import Substr
import logging

logger = logging.getLogger(__name__)


class DirectorioMunicipioCreateView(CreateView):
    model = Directorio_municipio
    form_class = Directorio_MunicipioForm
    template_name = 'municipio/directorio_form.html'
    success_url = reverse_lazy('municipio-list')

    def get_initial(self):
        # Inicializar datos como se hacía en la función original
        #empleados = Empleado.objects.get(user=self.request.user)

        initial_data = {
            'estado_auditoria': '0',
        }
        return initial_data


class DirectorioMunicipioListView(ListView):
    model = Directorio_municipio
    template_name = 'municipio/directorio_list.html'
    context_object_name = 'municipios'

    def get_queryset(self):
        return Directorio_municipio.objects.filter(user=self.request.user)


def directorio_municipalidad_detail(request, municipio_directorio_id):
    if request.method == 'GET':
        directorio_municipalidad = get_object_or_404(Directorio_municipio, pk=municipio_directorio_id)
        form = Directorio_MunicipioForm(instance=directorio_municipalidad)
        context = {
            'directorio_municipalidad': directorio_municipalidad,
            'form': form
        }
        return render(request, 'municipio/directorio_detail.html', context)
    else:
        try:
            directorio_municipalidad = get_object_or_404(
                Directorio_municipio, pk=municipio_directorio_id)
            form = Directorio_MunicipioForm(request.POST, request.FILES, instance=directorio_municipalidad)
            form.save()
            return redirect('municipio-list')
        except ValueError:
            return render(request, 'municipio/directorio_detail.html', {'directorio_municipalidad': directorio_municipalidad, 'form': form, 'error': 'Error actualizar'})


class DirectorioMunicipioListViewPublic(ListView):
    model = Directorio_municipio
    template_name = 'municipio/directorio_public.html'
    context_object_name = 'municipios'

    def get_queryset(self):
        return Directorio_municipio.objects.filter(estado_auditoria='1')


### SALUD 
class DirectorioSaludCreateView(CreateView):
    model = Directorio_salud
    form_class = Directorio_SaludForm
    template_name = 'salud/directorio_form.html'
    success_url = reverse_lazy('salud-list')

    def get_initial(self):
        # Inicializar datos como se hacía en la función original
        #empleados = Empleado.objects.get(user=self.request.user)

        initial_data = {
            'estado_auditoria': '0',
        }
        return initial_data


class DirectorioSaludListView(ListView):
    model = Directorio_salud
    template_name = 'salud/directorio_list.html'
    context_object_name = 'salud'

    def get_queryset(self):
        return Directorio_salud.objects.filter(user=self.request.user)


def directorio_salud_detail(request, salud_directorio_id):
    if request.method == 'GET':
        directorio_salud = get_object_or_404(Directorio_salud, pk=salud_directorio_id)
        form = Directorio_SaludForm(instance=directorio_salud)
        context = {
            'directorio_salud': directorio_salud,
            'form': form
        }
        return render(request, 'salud/directorio_detail.html', context)
    else:
        try:
            directorio_salud = get_object_or_404(
                Directorio_salud, pk=salud_directorio_id)
            form = Directorio_SaludForm(request.POST, request.FILES, instance=directorio_salud)
            form.save()
            return redirect('salud-list')
        except ValueError:
            return render(request, 'salud/directorio_detail.html', {'directorio_salud': directorio_salud, 'form': form, 'error': 'Error actualizar'})


class DirectorioSaludListViewPublic(ListView):
    model = Directorio_salud
    template_name = 'salud/directorio_public.html'
    context_object_name = 'salud'

    def get_queryset(self):
        return Directorio_salud.objects.filter(estado_auditoria='1')


#####  DE SELLO MUNICIPAL INDICADOR 1
def obtener_distritos(provincia):
    distritos = MAESTRO_HIS_ESTABLECIMIENTO.objects.filter(Provincia=provincia).values('Distrito').distinct().order_by('Distrito')
    return list(distritos)


def obtener_avance(provincia, distrito):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM public.obtener_avance(%s, %s)",
            [provincia, distrito]
        )
        return cursor.fetchall()


def obtener_ranking(mes):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM public.obtener_ranking(%s)", [mes]
        )
        return cursor.fetchall()


def index_sello(request):
    mes_seleccionado = request.GET.get('mes', 'SETIEMBRE')
    provincia_seleccionada = request.GET.get('provincia')
    distrito_seleccionado = request.GET.get('distrito')

    provincias = MAESTRO_HIS_ESTABLECIMIENTO.objects.values_list('Provincia', flat=True).distinct().order_by('Provincia')

    # Si la solicitud es AJAX
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            # Verificar si se solicitan distritos
            if 'get_distritos' in request.GET:
                distritos = obtener_distritos(provincia_seleccionada)
                return JsonResponse(distritos, safe=False)

            # Obtener datos de avance y ranking
            resultados_avance = obtener_avance(provincia_seleccionada, distrito_seleccionado)
            resultados_ranking = obtener_ranking(mes_seleccionado)

            # Procesar los resultados
            data = {
                'fechas': [row[2] for row in resultados_avance],
                'num': [float(row[3]) for row in resultados_avance],
                'den': [float(row[4]) for row in resultados_avance],
                'avance': [float(row[5]) for row in resultados_avance],
                
                'provincia': [row[0] for row in resultados_ranking],
                'distrito': [row[1] for row in resultados_ranking],
                'num_r': [float(row[2]) for row in resultados_ranking],
                'den_r': [float(row[3]) for row in resultados_ranking],
                'avance_r': [float(row[4]) for row in resultados_ranking],
            }

            return JsonResponse(data)

        except Exception as e:
            logger.error(f"Error al obtener datos: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)

    # Si no es una solicitud AJAX, renderiza la página principal
    return render(request, 'sello/index_sello.html', {
        'provincias': provincias,
        'mes_seleccionado': mes_seleccionado,
    })


#--- PROVINCIAS -------------------------------------------------------------
def sello_get_provincias(request,provincias_id):
    provincias = (
                MAESTRO_HIS_ESTABLECIMIENTO
                .objects.filter(Descripcion_Sector='GOBIERNO REGIONAL')
                .annotate(ubigueo_filtrado=Substr('Ubigueo_Establecimiento', 1, 4))
                .values('Provincia','ubigueo_filtrado')
                .distinct()
                .order_by('Provincia')
    )
    context = {
                'provincias': provincias,
            }
    
    return render(request, 'sello/provincias.html', context)

def sello_get_distritos(request, distritos_id):
    provincias = (
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
                'provincias': provincias,
                'mes_inicio':mes_inicio,
                'mes_fin':mes_fin,
    }
    return render(request, 'sello/distritos.html', context)

def sello_p_distritos(request):
    provincia_param = request.GET.get('provincia')

    # Filtra los establecimientos por sector "GOBIERNO REGIONAL"
    establecimientos = MAESTRO_HIS_ESTABLECIMIENTO.objects.filter(Descripcion_Sector='GOBIERNO REGIONAL')

    # Filtra los establecimientos por el código de la provincia
    if provincia_param:
        establecimientos = establecimientos.filter(Ubigueo_Establecimiento__startswith=provincia_param[:4])
    # Selecciona el distrito y el código Ubigueo
    distritos = establecimientos.values('Distrito', 'Ubigueo_Establecimiento').distinct().order_by('Distrito')
    
    context = {
        'provincia': provincia_param,
        'distritos': distritos
    }
    return render(request, 'sello/partials/p_distritos.html', context)
