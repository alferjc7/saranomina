from django.forms import ModelForm
from gestionClientes.models import t_cliente, t_empresa, UsuarioEmpresa

class t_cliente_form(ModelForm):
    class Meta:
        model = t_cliente
        fields = '__all__'

class t_empresa_form(ModelForm):
    class Meta: 
        model = t_empresa
        fields = '__all__'

class usuarioempresa_form(ModelForm):
    class Meta: 
        model = UsuarioEmpresa
        fields = '__all__'