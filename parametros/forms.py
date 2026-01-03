from django import forms
from django.forms import ModelForm
from parametros.models import (t_tipo_contrato, t_tipo_salario, t_tipo_cotizante, 
                               t_subtipo_cotizante, t_banco, t_entidadesss)

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


class CargaExcelForm(forms.Form):
    archivo_excel = forms.FileField(
        required=True,
        widget=forms.ClearableFileInput(attrs={
            'accept': '.xlsx',
            'style': 'display:none;',
            'id': 'excel-input'
        })
    )
