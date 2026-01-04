from django import forms
from django.forms import ModelForm
from gestionContratos.models import (t_contrato, t_contrato_banco, 
                                     t_contrato_entidadesss, t_contrato_salario,
                                     t_contrato_deducibles)

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
