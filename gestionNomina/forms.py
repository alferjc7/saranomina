from django import forms
from django.forms import ModelForm, ValidationError
from gestionNomina.models import t_periodo_nomina
from parametros.models import t_tipo_nomina

class t_periodo_nominaform(ModelForm):
    class Meta:
        model = t_periodo_nomina
        fields = '__all__'
        exclude = ('codigo',)
        
class GenerarPeriodoNominaForm(forms.Form):
    tipo_nomina = forms.ModelChoiceField(
        queryset=t_tipo_nomina.objects.all(),
        label="Tipo de nómina"
    )
    anio = forms.IntegerField(
        min_value=2000,
        max_value=2100,
        label="Año"
    )
    mes  = forms.IntegerField(
        required = False,
        min_value=1,
        max_value=12,
        label="Mes"
    )    
    periodo  = forms.IntegerField(
        required=False,
        min_value=1,
        max_value=4,
        label="Periodo"
    )
    fecha_inicio = forms.DateField(
        required=False,
        label="Fecha inicio",
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'class': 'form-control'
            }
        ))
    fecha_fin = forms.DateField(
        required=False,
        label="Fecha fin",
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'class': 'form-control'
            }
        ))
