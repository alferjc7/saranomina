from django import forms
from django.forms import ModelForm, ValidationError
from gestionContratos.models import (t_contrato, t_contrato_banco, 
                                     t_contrato_entidadesss, t_contrato_salario,
                                     t_contrato_deducibles)
from parametros.models import (t_tipo_cotizante, t_subtipo_cotizante, t_entidadesss)

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
    def __init__(self, *args, **kwargs):
        self.contrato = kwargs.pop('contrato', None)
        super().__init__(*args, **kwargs)
    
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
        
    def clean_fecha_inicio(self):
        fecha_inicio = self.cleaned_data.get('fecha_inicio')

        if self.contrato and fecha_inicio:
            if fecha_inicio < self.contrato.fecha_ingreso:
                raise forms.ValidationError(
                    'La fecha inicio no puede ser menor a la fecha de ingreso del contrato'
                )
        return fecha_inicio
    
    
    def clean_fecha_fin(self):
        fecha_fin = self.cleaned_data.get('fecha_fin')

        if self.contrato and fecha_fin:
            if fecha_fin < self.contrato.fecha_ingreso:
                raise forms.ValidationError(
                    'La fecha fin no puede ser menor a la fecha de ingreso del contrato'
                )
        return fecha_fin

    def clean(self):
        cleaned_data = super().clean()

        fi = cleaned_data.get('fecha_inicio')
        ff = cleaned_data.get('fecha_fin')

        if fi and ff and ff < fi:
            self.add_error(
                'fecha_fin',
                'La fecha fin no puede ser menor que la fecha inicio'
            )

        return cleaned_data






class t_contrato_entidadesss_form(ModelForm):
    def __init__(self, *args, **kwargs):
        self.contrato = kwargs.pop('contrato', None)
        super().__init__(*args, **kwargs)
        self.fields['entidad'].queryset = t_entidadesss.objects.none()

        if self.instance.pk and self.instance.tipo_entidad:
            self.fields['entidad'].queryset = t_entidadesss.objects.filter(
                tipo=self.instance.tipo_entidad
            )

        if 'tipo_entidad' in self.data:
            tipo = self.data.get('tipo_entidad')
            self.fields['entidad'].queryset = t_entidadesss.objects.filter(
                tipo=tipo
            )
    
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
        
    def clean_fecha_inicio(self):
        fecha_inicio = self.cleaned_data.get('fecha_inicio')

        if self.contrato and fecha_inicio:
            if fecha_inicio < self.contrato.fecha_ingreso:
                raise forms.ValidationError(
                    'La fecha inicio no puede ser menor a la fecha de ingreso del contrato'
                )
        return fecha_inicio

    def clean_fecha_fin(self):
        fecha_fin = self.cleaned_data.get('fecha_fin')

        if self.contrato and fecha_fin:
            if fecha_fin < self.contrato.fecha_ingreso:
                raise forms.ValidationError(
                    'La fecha fin no puede ser menor a la fecha de ingreso del contrato'
                )
        return fecha_fin

    def clean(self):
        cleaned_data = super().clean()

        fi = cleaned_data.get('fecha_inicio')
        ff = cleaned_data.get('fecha_fin')

        if fi and ff and ff < fi:
            self.add_error(
                'fecha_fin',
                'La fecha fin no puede ser menor que la fecha inicio'
            )

        return cleaned_data
    






class t_contrato_salario_form(ModelForm):
    def __init__(self, *args, **kwargs):
        self.contrato = kwargs.pop('contrato', None)
        super().__init__(*args, **kwargs)
    
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
    
    def clean_fecha_inicio(self):
        fecha_inicio = self.cleaned_data.get('fecha_inicio')

        if self.contrato and fecha_inicio:
            if fecha_inicio < self.contrato.fecha_ingreso:
                raise forms.ValidationError(
                    'La fecha inicio no puede ser menor a la fecha de ingreso del contrato'
                )
        return fecha_inicio

    def clean_fecha_fin(self):
        fecha_fin = self.cleaned_data.get('fecha_fin')

        if self.contrato and fecha_fin:
            if fecha_fin < self.contrato.fecha_ingreso:
                raise forms.ValidationError(
                    'La fecha fin no puede ser menor a la fecha de ingreso del contrato'
                )
        return fecha_fin

    def clean(self):
        cleaned_data = super().clean()

        fi = cleaned_data.get('fecha_inicio')
        ff = cleaned_data.get('fecha_fin')

        if fi and ff and ff < fi:
            self.add_error(
                'fecha_fin',
                'La fecha fin no puede ser menor que la fecha inicio'
            )

        return cleaned_data

class t_contrato_deducible_form(ModelForm):
    def __init__(self, *args, **kwargs):
        self.contrato = kwargs.pop('contrato', None)
        super().__init__(*args, **kwargs)
    
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
        
    def clean_fecha_inicio(self):
        fecha_inicio = self.cleaned_data.get('fecha_inicio')
        tipo = self.cleaned_data.get('tipo_deducible')
        valor = self.cleaned_data.get('valor')

        if tipo == 'DED' and valor is not None:
            if valor != 1:
                self.add_error(
                    'valor',
                    'El valor de dependiente debe ser 1'
                )

        if self.contrato and fecha_inicio:
            if fecha_inicio < self.contrato.fecha_ingreso:
                raise forms.ValidationError(
                    'La fecha inicio no puede ser menor a la fecha de ingreso del contrato'
                )
        return fecha_inicio

    def clean_fecha_fin(self):
        fecha_fin = self.cleaned_data.get('fecha_fin')

        if self.contrato and fecha_fin:
            if fecha_fin < self.contrato.fecha_ingreso:
                raise forms.ValidationError(
                    'La fecha fin no puede ser menor a la fecha de ingreso del contrato'
                )
        return fecha_fin

    def clean(self):
        cleaned_data = super().clean()

        fi = cleaned_data.get('fecha_inicio')
        ff = cleaned_data.get('fecha_fin')

        if fi and ff and ff < fi:
            self.add_error(
                'fecha_fin',
                'La fecha fin no puede ser menor que la fecha inicio'
            )

        return cleaned_data

