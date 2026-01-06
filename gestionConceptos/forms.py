from django import forms
from django.forms import ModelForm
from gestionConceptos.models import t_conceptos, t_concepto_empresa

class t_conceptosform(ModelForm):
    class Meta:
        model = t_conceptos
        fields = '__all__'

class t_concepto_empresaform(ModelForm):
    class Meta:
        model = t_concepto_empresa
        fields = '__all__'
        exclude = (
            'empresa',
            'cod_concepto')
