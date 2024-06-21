from django import forms
from django.forms import modelformset_factory
from .poi_models import ActividadPOI, ProgramacionMensual, ProgramacionMensualMetaFinanciera,ProgramacionMetaFisica
    
class ActividadPOIForm(forms.ModelForm):
    class Meta:
       model =  ActividadPOI
       exclude = ['ano','tipo_presupuesto','fecha_registro','pliego','unidad_ejecutora','objetivo_sectorial','objetivo_institucional','accion_estrategica','tipo_categoria']       
       fields = [
                'categoria_presupuestal',
                'tipo_producto_proyecto',
                'producto_presupuestal',
                'tipo_actividad_obra',
                'actividad_presupuestal',
                'funcion',
                'division_funcional',
                'grupo_funcional',
                'actividad_operativa',
                'unidad_medida',
                'total_meta_fisica',
                'meta_presupuestal',
                'meta_fisica',
                'meta_programada',
                'meta_anual',
                'enero',
                'febrero',
                'marzo',
                'abril',
                'mayo',
                'junio',
                'julio',
                'agosto',
                'setiembre',
                'octubre',
                'noviembre',
                'diciembre',
                'enero_e',
                'febrero_e',
                'marzo_e',
                'abril_e',
                'mayo_e',
                'junio_e',
                'julio_e',
                'agosto_e',
                'setiembre_e',
                'octubre_e',
                'noviembre_e',
                'diciembre_e',
                'total_e',
                'primer_semestre',
                'segundo_semestre',
                'primer_semestre_e',
                'segundo_semestre_e',
                'porcentaje',
                ]     
       widgets = {
                'categoria_presupuestal': forms.TextInput(attrs={'class':'form-control','style': 'border-color: silver; color: silver;','readonly':'readonly'}),
                'tipo_producto_proyecto': forms.TextInput(attrs={'class':'form-control','style': 'border-color: silver; color: silver;','readonly':'readonly'}),
                'producto_presupuestal': forms.TextInput(attrs={'class':'form-control','style': 'border-color: silver; color: silver;','readonly':'readonly'}),
                'tipo_actividad_obra': forms.TextInput(attrs={'class':'form-control','style': 'border-color: silver; color: silver;','readonly':'readonly'}),
                'actividad_presupuestal': forms.TextInput(attrs={'class':'form-control','style': 'border-color: silver; color: silver;','readonly':'readonly'}),
                'funcion': forms.TextInput(attrs={'class':'form-control','style': 'border-color: silver; color: silver;','readonly':'readonly'}),
                'division_funcional': forms.TextInput(attrs={'class':'form-control','style': 'border-color: silver; color: silver;','readonly':'readonly'}),
                'grupo_funcional': forms.TextInput(attrs={'class':'form-control','style': 'border-color: silver; color: silver;','readonly':'readonly'}),
                'actividad_operativa': forms.TextInput(attrs={'class':'form-control','style': 'border-color: silver; color: silver;','readonly':'readonly'}),
                'unidad_medida': forms.TextInput(attrs={'class':'form-control','style': 'border-color: silver; color: silver;','readonly':'readonly'}),
                'total_meta_fisica': forms.TextInput(attrs={'class':'form-control','style': 'border-color: silver; color: silver;','readonly':'readonly'}),
                'meta_presupuestal': forms.TextInput(attrs={'class':'form-control','style': 'border-color: silver; color: silver;','readonly':'readonly'}),
                'meta_fisica': forms.TextInput(attrs={'class':'form-control','style': 'border-color: silver; color: silver;','readonly':'readonly'}),
                'meta_programada': forms.TextInput(attrs={'class':'form-control','style': 'border-color: silver; color: silver;','readonly':'readonly'}),
                'meta_anual': forms.TextInput(attrs={'class':'form-control','style': 'border-color: silver; color: silver;','readonly':'readonly'}),
                'enero': forms.TextInput(attrs={'class':'form-control','style': 'border-color: silver; color: silver;','readonly':'readonly'}),
                'febrero': forms.TextInput(attrs={'class':'form-control','style': 'border-color: silver; color: silver;','readonly':'readonly'}),
                'marzo': forms.TextInput(attrs={'class':'form-control','style': 'border-color: silver; color: silver;','readonly':'readonly'}),
                'abril': forms.TextInput(attrs={'class':'form-control','style': 'border-color: silver; color: silver;','readonly':'readonly'}),
                'mayo': forms.TextInput(attrs={'class':'form-control','style': 'border-color: silver; color: silver;','readonly':'readonly'}),
                'junio': forms.TextInput(attrs={'class':'form-control','style': 'border-color: silver; color: silver;','readonly':'readonly'}),
                'julio': forms.TextInput(attrs={'class':'form-control','style': 'border-color: silver; color: silver;','readonly':'readonly'}),
                'agosto': forms.TextInput(attrs={'class':'form-control','style': 'border-color: silver; color: silver;','readonly':'readonly'}),
                'setiembre': forms.TextInput(attrs={'class':'form-control','style': 'border-color: silver; color: silver;','readonly':'readonly'}),
                'octubre': forms.TextInput(attrs={'class':'form-control','style': 'border-color: silver; color: silver;','readonly':'readonly'}),
                'noviembre': forms.TextInput(attrs={'class':'form-control','style': 'border-color: silver; color: silver;','readonly':'readonly'}),
                'diciembre': forms.TextInput(attrs={'class':'form-control','style': 'border-color: silver; color: silver;','readonly':'readonly'}),
                'enero_e': forms.TextInput(attrs={'class':'form-control','style': 'border-color: silver; color: silver;','readonly':'readonly'}),
                'febrero_e': forms.TextInput(attrs={'class':'form-control','style': 'border-color: silver; color: silver;','readonly':'readonly'}),
                'marzo_e': forms.TextInput(attrs={'class':'form-control','style': 'border-color: silver; color: silver;','readonly':'readonly'}),
                'abril_e': forms.TextInput(attrs={'class':'form-control','style': 'border-color: silver; color: silver;','readonly':'readonly'}),
                'mayo_e': forms.TextInput(attrs={'class':'form-control','style': 'border-color: silver; color: silver;','readonly':'readonly'}),
                'junio_e': forms.TextInput(attrs={'class':'form-control','style': 'border-color: silver; color: silver;','readonly':'readonly'}),
                'julio_e': forms.TextInput(attrs={'class':'form-control','style': 'border-color: silver; color: silver;','readonly':'readonly'}),
                'agosto_e': forms.TextInput(attrs={'class':'form-control','style': 'border-color: silver; color: silver;','readonly':'readonly'}),
                'setiembre_e': forms.TextInput(attrs={'class':'form-control','style': 'border-color: silver; color: silver;','readonly':'readonly'}),
                'octubre_e': forms.TextInput(attrs={'class':'form-control','style': 'border-color: silver; color: silver;','readonly':'readonly'}),
                'noviembre_e' : forms.TextInput(attrs={'class':'form-control','style': 'border-color: silver; color: silver;','readonly':'readonly'}),
                'diciembre_e': forms.TextInput(attrs={'class':'form-control','style': 'border-color: silver; color: silver;','readonly':'readonly'}),
                'total_e' : forms.TextInput(attrs={'class':'form-control','style': 'border-color: silver; color: silver;','readonly':'readonly'}),
                'primer_semestre' : forms.TextInput(attrs={'class':'form-control','style': 'border-color: silver; color: silver;','readonly':'readonly'}),
                'segundo_semestre' : forms.TextInput(attrs={'class':'form-control','style': 'border-color: silver; color: silver;','readonly':'readonly'}),
                'primer_semestre_e' : forms.TextInput(attrs={'class':'form-control','style': 'border-color: silver; color: silver;','readonly':'readonly'}),
                'segundo_semestre_e': forms.TextInput(attrs={'class':'form-control','style': 'border-color: silver; color: silver;','readonly':'readonly'}),
                'porcentaje': forms.TextInput(attrs={'class':'form-control','style': 'border-color: silver; color: silver;','readonly':'readonly'}),          
       }
       labels = {
            'categoria_presupuestal':'Categoria Presupuestal',
            
        }


ProgramacionMensualFormSet = modelformset_factory(
    ProgramacionMensual,
    fields=['mes', 'meta_fisica', 'meta_presupuestal'],
    extra=0, max_num=12, validate_max=True,
    widgets={
        'mes': forms.Select(attrs={'class': 'form-control'}),
        'meta_fisica': forms.NumberInput(attrs={'class': 'form-control'}),
        'meta_presupuestal': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
    }
)

class RegistroTareaForm(forms.ModelForm):
    class Meta:
        model = ActividadPOI
        fields = '__all__'

class ProgramacionMensualMetaFisicaForm(forms.ModelForm):
    class Meta:
        model = ProgramacionMetaFisica
        fields = '__all__'

class ProgramacionMensualMetaFinancieraForm(forms.ModelForm):
    class Meta:
        model = ProgramacionMensualMetaFinanciera
        fields = '__all__'