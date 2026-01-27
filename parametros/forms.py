from django import forms
from django.forms import ModelForm
from parametros.models import (t_tipo_contrato, t_tipo_salario, t_tipo_cotizante, 
                               t_subtipo_cotizante, t_banco, t_entidadesss,
                               t_conceptos_salario, t_tipo_nomina, ParametroGeneral,
                               ParametroDetalle)
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

class t_parametrogeneralform(ModelForm):
    class Meta:
        model = ParametroGeneral
        fields = '__all__'


    def clean_codigo(self):
        codigo = self.cleaned_data.get('codigo')
        pk = self.data.get('pk')  # 👈 viene del input hidden

        qs = ParametroGeneral.objects.filter(codigo=codigo)

        if pk:
            qs = qs.exclude(pk=pk)

        if qs.exists():
            raise forms.ValidationError(
                "Parametro general with this Codigo already exists."
            )

        return codigo


class t_parametrodetllleform(ModelForm):
    class Meta:
        model = ParametroDetalle
        fields = '__all__'
        exclude = (
            'parametro',)
        widgets = {
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
   
    def clean_codigo(self):
        codigo = self.cleaned_data.get('codigo')
        pk = self.data.get('pk')  # 👈 viene del input hidden

        qs = ParametroDetalle.objects.filter(codigo=codigo)

        if pk:
            qs = qs.exclude(pk=pk)

        if qs.exists():
            raise forms.ValidationError(
                "Parametro detalle with this Codigo already exists."
            )
        return codigo

class CargaExcelForm(forms.Form):
    archivo_excel = forms.FileField(
        required=True,
        widget=forms.ClearableFileInput(attrs={
            'accept': '.xlsx',
            'style': 'display:none;',
            'id': 'excel-input'
        })
    )



class GenerarCalendarioForm(forms.Form):
    sabado_habil = forms.BooleanField(
        label="Sabado habil",
        required=False,   
        initial=True,   
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input',
                'role': 'switch'
            }
        )
    )
    anio = forms.IntegerField(
        min_value=2000,
        max_value=2100,
        label="Año",
        required= False
    )
    mes  = forms.IntegerField(
        required = False,
        min_value=1,
        max_value=12,
        label="Mes"
    )    
    fecha = forms.DateField(
        required=False,
        label="Fecha",
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'class': 'form-control'
            }
        ))
    habil = forms.BooleanField(
        label="Habil",
        required=False,   
        initial=True,   
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input',
                'role': 'switch'
            }
        )
    )