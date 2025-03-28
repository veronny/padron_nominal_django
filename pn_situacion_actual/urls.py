from django.urls import path
from .views import index_situacion_padron
from .views import get_provincias_situacion, RptSituacionProvincia 
from .views import get_distritos_situacion, p_distritos_situacion, RptSituacionDistrito
from .views import get_redes_situacion, RptSituacionRed 
from .views import get_microredes_situacion, p_microredes_situacion, RptSituacionMicroRed
from .views import get_establecimientos_situacion, p_establecimientos_situacion, p_microredes_establec_situacion, RptSituacionEstablec


urlpatterns = [
    
    
    path('situacion_padron/', index_situacion_padron, name='index_situacion_padron'),
    
    ### SEGUIMIENTO
    # provincia
    path('get_provincia_situacion/<int:provincia_id>/', get_provincias_situacion, name='pn_situacion_actual_get_provincias'),
    #-- provincia excel
    path('rpt_situacion_provincia_excel/', RptSituacionProvincia.as_view(), name = 'rpt_situacion_provincia_xls'),
    
    # distrito
    path('get_distrito_situacion/<int:distrito_id>/', get_distritos_situacion, name='pn_situacion_actual_get_distritos'),
    path('p_distrito_situacion/', p_distritos_situacion, name='p_distrito_situacion'),
    #-- distrito excel
    path('rpt_situacion_distrito_excel/', RptSituacionDistrito.as_view(), name = 'rpt_situacion_distrito_xls'),
    
    # redes
    path('get_redes_situacion/<int:redes_id>/', get_redes_situacion, name='pn_situacion_actual_get_redes'),
    #-- redes excel
    path('rpt_situacion_red_excel/', RptSituacionRed.as_view(), name = 'rpt_situacion_red_xls'),
    
    # microredes
    path('get_microredes_situacion/<int:microredes_id>/', get_microredes_situacion, name='pn_situacion_actual_get_microredes'),
    path('p_microredes_situacion/', p_microredes_situacion, name='p_microredes_situacion'),
    #-- microredes excel
    path('rpt_situacion_microred_excel/', RptSituacionMicroRed.as_view(), name = 'rpt_situacion_microred_xls'),
    
    # establecimientos
    path('get_establecimientos_situacion/<int:establecimiento_id>/', get_establecimientos_situacion, name='pn_situacion_actual_get_establecimientos'),
    path('p_microredes_establec_situacion/', p_microredes_establec_situacion, name='p_microredes_establec_situacion'),
    path('p_establecimiento_situacion/', p_establecimientos_situacion, name='p_establecimientos_situacion'),       
    #-- estableccimiento excel
    path('rpt_situacion_establec_excel/', RptSituacionEstablec.as_view(), name = 'rpt_situacion_establec_xls'),
    
]