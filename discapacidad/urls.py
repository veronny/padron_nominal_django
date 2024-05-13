from django.urls import path
from . import views 
from .views import RptOperacinalProv, RptOperacinalDist, RptOperacinalRed 

urlpatterns = [
    #discapacidad
    path('operacional/', views.operacional, name='operacional'),
    
    # provincia
    path('get_provincias/<int:provincias_id>/', views.get_provincias, name='get_provincias'),
    #-- provincia excel
    path('rpt_operacional_prov_excel/', RptOperacinalProv.as_view(), name = 'rpt_operacional_prov_xls'),
    
    # distrito
    path('get_distritos/<int:distritos_id>/', views.get_distritos, name='get_distritos'),
    path('p_distritos/', views.p_distritos, name='p_distritos'),
    #-- distrito excel
    path('rpt_operacional_distrito_excel/', RptOperacinalDist.as_view(), name = 'rpt_operacional_dist_xls'),
        
    # redes
    path('get_redes/<int:redes_id>/', views.get_redes, name='get_redes'),
    #-- redes excel
    path('rpt_operacional_red_excel/', RptOperacinalRed.as_view(), name = 'rpt_operacional_red_xls'),
    
    #microredes
    path('get_microredes/<int:microredes_id>/', views.get_microredes, name='get_microredes'),
    path('p_microredes/', views.p_microredes, name='p_microredes'),
    
    # establecimientos
    path('get_establecimientos/<int:establecimiento_id>/', views.get_establecimientos, name='get_establecimientos'),
    path('p_microredes_establec/', views.p_microredes_establec, name='p_microredes_establec'),
    path('p_establecimiento/', views.p_establecimientos, name='p_establecimientos'),    
    
   #path('establecimiento/', views.establecimiento, name='establecimiento'),
   #path('obtener_microredes/', views.obtener_microredes, name='obtener_microredes'),
   #path('obtener_establecimientos/', views.obtener_establecimientos, name='obtener_establecimientos'),
    
    
    path('matrizes/', views.crear_matriz, name='matrizes'),
]