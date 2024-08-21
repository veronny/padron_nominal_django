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
            form = Directorio_MunicipioForm(request.POST, instance=directorio_municipalidad)
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
            form = Directorio_SaludForm(request.POST, instance=directorio_salud)
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