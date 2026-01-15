from django import forms
from django.forms import ModelForm
from gestionConceptos.models import (t_conceptos, t_concepto_empresa,
                                     t_grupo_concepto, t_grupo_concepto_det)

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
        
class t_grupo_conceptoform(ModelForm):
    class Meta:
        model = t_grupo_concepto
        fields = '__all__'

class t_grupo_conceptodetform(ModelForm):
    class Meta:
        model = t_grupo_concepto_det
        fields = '__all__'
        exclude = (
            'grupo',)
    
    
    
    
