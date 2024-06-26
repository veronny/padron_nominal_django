from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from django.contrib.auth.models import Permission
# Register your models here.
from django.contrib.auth.models import Permission

from .poi_models import ActividadPOI

admin.site.register(Permission)

## admin.site.register(ActividadPOI)

#------------Red---------------------------------
class POIResources(resources.ModelResource):
    class Meta:
        model = ActividadPOI

@admin.register(ActividadPOI)
class POIAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    resource_class = POIResources
    list_display = (
        'id',
        'unidad_ejecutora',
        'categoria_presupuestal',
        'producto_presupuestal',
        'tipo_actividad_obra',
        'actividad_presupuestal',
        'actividad_operativa',
        'total_meta_fisica',
    )
    search_fields = ('unidad_ejecutora','categoria_presupuestal','producto_presupuestal','tipo_actividad_obra','actividad_presupuestal','actividad_operativa','total_meta_fisica',)

