from django import forms
from django.forms import ModelForm
from gestionIdentificacion.models import t_tipo_ide, t_identificacion, t_beneficiario

class tipo_ide_form(ModelForm):
    class Meta:
        model = t_tipo_ide
        fields = ['cod_ide', 'desc_ide', 'estado_ide']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 
        self.fields['estado_ide'].initial= True

class identificacion_form(ModelForm):
    class Meta:
        model = t_identificacion
        fields = ['tipo_ide','identificacion','nombre','segundo_nombre','apellido','segundo_apellido','fecha_nacimiento',
                  'fecha_exp_doc','telefono','celular','direccion','estado_civil','genero','correo_personal','correo_coorporativo']
        widgets = {
            'fecha_nacimiento': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control'
                }
            ),
            'fecha_exp_doc': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control'
                }
            ),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['genero'].required = True  # 👈 CLAVE
        self.fields['tipo_ide'].required = True                 # 🔑 evita '--------'
        self.fields['tipo_ide'].empty_label = "Seleccione una opción"

class t_beneficiario_form(ModelForm):
    class Meta:
        model = t_beneficiario
        fields = '__all__'
        widgets = {
            'fecha_nacimiento': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control'
                }
            )
        }
        exclude = (
            'iden_titular',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tipo_ide_ben'].required = True      # 🔑 evita '--------'
        self.fields['tipo_ide_ben'].empty_label = "Seleccione una opción"

        

