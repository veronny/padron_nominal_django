from django.urls import path
from . import views 
from .views import RptOperacinalProv 

urlpatterns = [
    #discapacidad
    path('operacional/', views.operacional, name='operacional'),
    # provincia
    path('get_provincias/<int:provincias_id>/', views.get_provincias, name='get_provincias'),
    #-- provincia excel
    path('rpt_operacional_prov_excel/', RptOperacinalProv.as_view(), name = 'rpt_operacional_prov_xls'),
    
    path('matrizes/', views.crear_matriz, name='matrizes'),
]