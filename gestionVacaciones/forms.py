from django import forms
from django.forms import ModelForm

TIPO_VACACIONES = (
        ('D', 'DISFRUTADAS'),
        ('C', 'COMPENSADAS'),
)
   
class GenerarVacacionesForm(forms.Form):
    tipo_vac = forms.ChoiceField(
        choices=TIPO_VACACIONES,
        required=True,
        label="Tipo de vacaciones",
        widget=forms.Select(
        attrs={
          'class': 'form-control'
          }
        )
    )
   
    dias  = forms.IntegerField(
        required = False,
        min_value=1,
        max_value=25,
        label="Dias"
    )

    fecha_inicio = forms.DateField(
        required=False,
        label="Fecha inicio",
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'class': 'form-control'
            }
        )
    )
    
    fecha_fin = forms.DateField(
        required=False,
        label="Fecha fin",
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'readonly': 'readonly',   # 👈 CLAVE
            }
        )
    )
    
    fecha_pago = forms.DateField(
        required=False,
        label="Fecha pago",
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'class': 'form-control'
            }
        )
    )