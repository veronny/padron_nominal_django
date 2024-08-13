from django import forms
from django.forms import modelformset_factory
from .poi_models import ActividadPOI, ProgramacionMensual, ProgramacionMensualMetaFinanciera,ProgramacionMetaFisica
from .padron_models import Directorio_municipio 
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
        
class Directorio_MunicipioForm(forms.ModelForm):
    class Meta:
        model =  Directorio_municipio
        exclude = ['nombre_completo','situacion_usuario','dateTimeOfUpload_req_oficio','dateTimeOfUpload_req_resolucion','dateTimeOfUpload_req_formato_alta','dateTimeOfUpload_req_formato_excel']       
        fields = [
                'tipo_documento',
                'documento_identidad',
                'apellido_paterno',
                'apellido_materno',
                'nombres',
                'telefono',                
                'correo_electronico',
                'provincia',
                'distrito',
                'ubigueo',
                'nombre_municipio',
                'cargo',
                'perfil',
                'condicion',
                'cuenta_usuario',
                'estado_usuario',
                'condicion_laboral',
                'user',
                'req_oficio',
                'req_resolucion',
                'req_formato_alta',
                'req_formato_excel',
        ]     
        widgets = {
                'tipo_documento' : forms.Select(attrs={'class':'form-control','required': True}),
                'documento_identidad' : forms.TextInput(attrs={'class':'form-control'}),
                'apellido_paterno' : forms.TextInput(attrs={'class':'form-control'}),
                'apellido_materno' : forms.TextInput(attrs={'class':'form-control'}),
                'nombres' : forms.TextInput(attrs={'class':'form-control'}),
                'telefono' : forms.TextInput(attrs={'class':'form-control'}),
                'correo_electronico' : forms.TextInput(attrs={'class':'form-control'}),
                'provincia' : forms.TextInput(attrs={'class':'form-control'}),
                'distrito' : forms.TextInput(attrs={'class':'form-control'}),
                'ubigueo' : forms.TextInput(attrs={'class':'form-control'}),
                'nombre_municipio' : forms.TextInput(attrs={'class':'form-control'}),
                'condicion_laboral' : forms.Select(attrs={'class':'form-control','required': True}),
                'cargo' : forms.Select(attrs={'class':'form-control','required': True}),
                'perfil' : forms.Select(attrs={'class':'form-control','required': True}),
                'condicion' : forms.Select(attrs={'class':'form-control','required': True}),
                'user' : forms.TextInput(attrs={'class':'form-control','style': 'display: none'}),
                'cuenta_usuario' : forms.TextInput(attrs={'class':'form-control','style': 'display: none'}),
                'estado_usuario' : forms.TextInput(attrs={'class':'form-control','style': 'display: none'}),
                'nombre_completo' : forms.TextInput(attrs={'class':'form-control','style': 'display: none'}),
                'estado_auditoria' : forms.TextInput(attrs={'class':'form-control','style': 'display: none'}),
                #####################
                'situacion_usuario': forms.TextInput(attrs={'class':'form-control','style': 'display: none'}),
                'dateTimeOfUpload_req_oficio': forms.TextInput(attrs={'class':'form-control','style': 'display: none'}),
                'dateTimeOfUpload_req_resolucion': forms.TextInput(attrs={'class':'form-control','style': 'display: none'}), 
                'dateTimeOfUpload_req_formato_alta':forms.TextInput(attrs={'class':'form-control','style': 'display: none'}), 
                'dateTimeOfUpload_req_formato_excel': forms.TextInput(attrs={'class':'form-control','style': 'display: none'}),
        }
        labels = {
            'tipo_documento':'Tipo Documento',
            'documento_identidad':'Numero de Documento',
            'correo_electronico':'Correo electronico',
            'nombre_municipio':'Nombre de Municipio',
            'req_oficio': 'Oficio',
            'req_resolucion':'Resolucion',
            'req_formato_alta':'Formato Alta/Baja',
            'req_formato_excel':'Formato Excel',            
            'ubigueo': '',
            'estado_usuario': '',
            'nombre_completo': '',
            'situacion_usuario': '',
        }