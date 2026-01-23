from django import forms
from django.db import connection
from django.forms import ModelForm, ValidationError
from gestionNomina.models import t_periodo_nomina, t_logica_calculo, t_acumulado_empleado, t_logica_calculo_filtro
from gestionConceptos.models import t_concepto_empresa
from parametros.models import t_tipo_nomina, t_tipo_contrato, t_tipo_cotizante

class t_periodo_nominaform(ModelForm):
    class Meta:
        model = t_periodo_nomina
        fields = '__all__'
        exclude = ('codigo',)

class t_acumulaldo_empleadoform(ModelForm):
    class Meta:
        model = t_acumulado_empleado
        fields = '__all__'

class t_logica_calculoform(ModelForm):
    logica = forms.ChoiceField(
        choices=[],
        required=False,
        label="Lógica de cálculo"
    )

    class Meta:
        model = t_logica_calculo
        fields = '__all__'
        exclude = ('empresa',)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['logica'].choices = [('', 'Seleccione un concepto')]

        concepto_id = None

        self.fields['logica'].choices += self._obtener_prc(concepto_id)

    def _obtener_prc(self, concepto_id):
        cursor = connection.cursor()
        print('aca')
        sql = """
         SELECT upper(routine_name)
            FROM information_schema.routines
            WHERE routine_type = 'PROCEDURE'
              AND routine_name LIKE 'prc_%'
            ORDER BY routine_name
        """
        cursor.execute(sql)
        resultados = cursor.fetchall()

        return [(r[0], r[0]) for r in resultados]


class GenerarPeriodoNominaForm(forms.Form):
    ejecucion_automatica = forms.BooleanField(
        label="Ejecución automática",
        required=False,   
        initial=True,   
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input',
                'role': 'switch'
            }
        )
    )
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
    estado = forms.BooleanField(
        required= False,
        label = "Estado",
        initial= True,
        disabled= True
        )

class FiltroTipoContratoForm(forms.ModelForm):
    valor = forms.ModelChoiceField(
        queryset=t_tipo_contrato.objects.filter(estado=True),
        label="Tipo de contrato"
    )

    class Meta:
        model = t_logica_calculo_filtro
        fields = ['operador']


class FiltroTipoCotizanteForm(forms.ModelForm):
    valor = forms.ModelChoiceField(
        queryset=t_tipo_cotizante.objects.filter(estado=True),
        label="Tipo de cotizante"
    )

    class Meta:
        model = t_logica_calculo_filtro
        fields = ['operador']