from django import forms
from django.forms import ModelForm
from gestionNovedades.models import t_novedad_temporal, t_novedad_fija, t_novedad_fija_det
from gestionContratos.models import t_contrato

class t_novedad_temporalform(ModelForm):
    class Meta:
        model = t_novedad_temporal
        fields = '__all__'
        widgets = {
            'contrato': forms.Select(
                attrs={'class': 'select-contrato'
                       }
            ),
            'concepto': forms.Select(
                attrs={'class': 'select-concepto'
                       }
            ),
            'periodo_nomina': forms.Select(
                attrs={'class': 'select-periodo_nomina'
                       }
            ),
            'fecha_novedad': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control'
                }
            ),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Deshabilitar campo estado
        self.fields['estado'].disabled = True


class t_novedad_fijaform(ModelForm):
    class Meta:
        model = t_novedad_fija
        fields = '__all__'
        widgets = {
            'contrato': forms.Select(
                attrs={'class': 'select-contrato'
                       }
            ),
            'concepto': forms.Select(
                attrs={'class': 'select-concepto'
                       }
            ),
            'fecha_inicio': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control'
                }
            ),
            'fecha_fin': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control'
                }
            ),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Deshabilitar campo estado
        self.fields['estado'].disabled = True


class t_novedad_fija_detform(ModelForm):
    class Meta:
        model = t_novedad_fija_det
        fields = '__all__'