from django.forms import ModelForm
from gestionClientes.models import t_cliente, t_empresa

class t_cliente_form(ModelForm):
    class Meta:
        model = t_cliente
        fields = '__all__'

class t_empresa_form(ModelForm):
    class Meta: 
        model = t_empresa
        fields = '__all__'