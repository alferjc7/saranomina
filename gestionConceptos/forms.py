from django import forms
from django.forms import ModelForm
from gestionConceptos.models import t_conceptos

class t_conceptosform(ModelForm):
    class Meta:
        model = t_conceptos
        fields = '__all__'