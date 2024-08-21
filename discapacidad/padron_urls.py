from django.urls import path
from .padron_views import DirectorioMunicipioCreateView, DirectorioMunicipioListView, directorio_municipalidad_detail,DirectorioMunicipioListViewPublic

urlpatterns = [

    # -- DIRECTORIO MUNICIPIO
    path('municipio/create/', DirectorioMunicipioCreateView.as_view(), name='municipio-create'),
    
    path('municipio/list/', DirectorioMunicipioListView.as_view(), name='municipio-list'),
    
    path('municipio/<int:municipio_directorio_id>/', directorio_municipalidad_detail, name='directorio_municipalidad_detail'),
    
    path('municipio/public/', DirectorioMunicipioListViewPublic.as_view(), name='municipio-public'),
]
