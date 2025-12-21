from django import forms
from django.forms import ModelForm
from parametros.models import t_tipo_contrato

class tipo_contratoform(ModelForm):
    class Meta:
        model = t_tipo_contrato
        fields = '__all__'
