from django.urls import path
from .views import index_situacion_padron, get_distritos

urlpatterns = [

    ##path('', dashboard, name='dashboard'),
    path('situacion_padron/', index_situacion_padron, name='index_situacion_padron'),
    
    path('get_distritos/<int:distritos_id>/', get_distritos, name='get_distritos'),
]