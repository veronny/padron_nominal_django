from django.urls import path
from .padron_views import DirectorioMunicipioCreateView, DirectorioMunicipioListView

urlpatterns = [

    # -- DIRECTORIO MUNICIPIO
    path('municipio/create/', DirectorioMunicipioCreateView.as_view(), name='municipio-create'),
    
    path('municipio/list/', DirectorioMunicipioListView.as_view(), name='municipio-list'),
    
]