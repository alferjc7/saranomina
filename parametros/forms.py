from django import forms
from django.forms import ModelForm
from parametros.models import (t_tipo_contrato, t_tipo_salario, t_tipo_cotizante, 
                               t_subtipo_cotizante, t_banco, t_entidadesss,
                               t_conceptos_salario, t_tipo_nomina)
from gestionConceptos.models import t_conceptos

class tipo_contratoform(ModelForm):
    class Meta:
        model = t_tipo_contrato
        fields = '__all__'

class tipo_salarioform(ModelForm):
    class Meta:
        model = t_tipo_salario
        fields = '__all__'

class tipo_cotizanteform(ModelForm):
    class Meta:
        model = t_tipo_cotizante
        fields = '__all__'

class subtipo_cotizanteform(ModelForm):
    class Meta:
        model = t_subtipo_cotizante
        fields = '__all__'

class bancoform(ModelForm):
    class Meta:
        model = t_banco
        fields = '__all__'

class t_entidadesssform(ModelForm):
    class Meta:
        model = t_entidadesss
        fields = '__all__'

class t_conceptos_salarioform(ModelForm):
    class Meta:
        model = t_conceptos_salario
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['concepto'].queryset = t_conceptos.objects.filter(
            tipo_concepto='DEV')
        
class t_tipo_nominaform(ModelForm):
    class Meta:
        model = t_tipo_nomina
        fields = '__all__'

class CargaExcelForm(forms.Form):
    archivo_excel = forms.FileField(
        required=True,
        widget=forms.ClearableFileInput(attrs={
            'accept': '.xlsx',
            'style': 'display:none;',
            'id': 'excel-input'
        })
    )
