from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect

# DIRECTORIO MUNICIPIO 
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from .padron_models import Directorio_municipio
from .forms import Directorio_MunicipioForm 

class DirectorioMunicipioCreateView(CreateView):
    model = Directorio_municipio
    form_class = Directorio_MunicipioForm
    template_name = 'municipio/directorio_form.html'
    success_url = reverse_lazy('municipio-list')

    def get_initial(self):
        # Inicializar datos como se hacía en la función original
        #empleados = Empleado.objects.get(user=self.request.user)

        initial_data = {
            '': '',
            '': '',
        }
        return initial_data


class DirectorioMunicipioListView(ListView):
    model = Directorio_municipio
    template_name = 'municipio/directorio_list.html'
    context_object_name = 'municipios'



