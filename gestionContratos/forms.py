from django import forms
from django.forms import ModelForm, ValidationError
from gestionContratos.models import (t_contrato, t_contrato_banco, 
                                     t_contrato_entidadesss, t_contrato_salario,
                                     t_contrato_deducibles)
from parametros.models import (t_tipo_cotizante, t_subtipo_cotizante)

class t_contratoform(ModelForm):
    class Meta:
        model = t_contrato
        fields = '__all__'
        widgets = {
            'fecha_ingreso': forms.DateInput(
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
        exclude = (
            'empresa',
            'cod_contrato')
        
    def clean(self):
        cleaned_data = super().clean()

        fecha_ingreso = cleaned_data.get('fecha_ingreso')
        fecha_fin = cleaned_data.get('fecha_fin')

        # Validar solo si fecha_fin está diligenciada
        if fecha_ingreso and fecha_fin:
            if fecha_ingreso > fecha_fin:
                        self.add_error('fecha_fin','La fecha de ingreso no puede ser mayor a la fecha de fin')
                        self.add_error('fecha_ingreso','La fecha de ingreso no puede ser mayor a la fecha de fin')

        return cleaned_data
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Deshabilitar campo estado
        self.fields['estado'].disabled = True

         # Inicialmente vacío
        self.fields['subtipo_cotizante'].queryset = t_subtipo_cotizante.objects.none()

        # Caso edición
        if self.instance.pk and self.instance.tipo_cotizante:
            self.fields['subtipo_cotizante'].queryset = (
                t_subtipo_cotizante.objects.filter(
                    codigo_cotizante=self.instance.tipo_cotizante
                )
            )

        # Caso POST
        if 'tipo_cotizante' in self.data:
            try:
                tipo_id = int(self.data.get('tipo_cotizante'))
                self.fields['subtipo_cotizante'].queryset = (
                    t_subtipo_cotizante.objects.filter(
                        codigo_cotizante=tipo_id
                    )
                )
            except (ValueError, TypeError):
                pass


class t_contrato_banco_form(ModelForm):
    class Meta:
        model = t_contrato_banco
        fields = '__all__'
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
        exclude = (
            'contrato',)



class t_contrato_entidadesss_form(ModelForm):
    class Meta:
        model = t_contrato_entidadesss
        fields = '__all__'
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
        exclude = (
            'contrato',)



class t_contrato_salario_form(ModelForm):
    class Meta:
        model = t_contrato_salario        
        fields = '__all__'
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
        exclude = (
            'contrato',)
        


class t_contrato_deducible_form(ModelForm):
    class Meta:
        model = t_contrato_deducibles        
        fields = '__all__'
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
        exclude = (
            'contrato',)
