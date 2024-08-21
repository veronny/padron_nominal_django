from django.urls import path
from .padron_views import DirectorioMunicipioCreateView, DirectorioMunicipioListView, directorio_municipalidad_detail,DirectorioMunicipioListViewPublic
from .padron_views import DirectorioSaludCreateView, DirectorioSaludListView, directorio_salud_detail,DirectorioSaludListViewPublic

urlpatterns = [

    # -- DIRECTORIO MUNICIPIO
    path('municipio/create/', DirectorioMunicipioCreateView.as_view(), name='municipio-create'),
    
    path('municipio/list/', DirectorioMunicipioListView.as_view(), name='municipio-list'),
    
    path('municipio/<int:municipio_directorio_id>/', directorio_municipalidad_detail, name='directorio_municipalidad_detail'),
    
    path('municipio/public/', DirectorioMunicipioListViewPublic.as_view(), name='municipio-public'),
    
    # -- DIRECTORIO SALUD
    path('salud/create/', DirectorioSaludCreateView.as_view(), name='salud-create'),
    
    path('salud/list/', DirectorioSaludListView.as_view(), name='salud-list'),
    
    path('salud/<int:salud_directorio_id>/', directorio_salud_detail, name='directorio_salud_detail'),
    
    path('salud/public/', DirectorioSaludListViewPublic.as_view(), name='salud-public'),
    
    
    
    
    
]
