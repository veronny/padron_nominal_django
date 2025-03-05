from django.urls import path
from .views import index_situacion_padron

urlpatterns = [
    
    ##path('', dashboard, name='dashboard'),
    path('situacion_padron/', index_situacion_padron, name='index_situacion_padron'),
    
]