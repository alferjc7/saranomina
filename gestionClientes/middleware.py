from django.shortcuts import redirect
from django.urls import reverse
from gestionClientes.models import UsuarioEmpresa, t_empresa

class EmpresaActivaMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.empresa = None

        if not request.user.is_authenticated:
            return self.get_response(request)

        # URLs que NO requieren empresa
        rutas_exentas = [
            reverse('seleccionar_empresa'),
            reverse('logout'),
        ]

        if request.path in rutas_exentas:
            return self.get_response(request)

        empresa_id = request.session.get('empresa_id')

        if not empresa_id:
            return redirect('seleccionar_empresa')

        if not UsuarioEmpresa.objects.filter(
            usuario=request.user,
            empresa_id=empresa_id,
            activo=True).exists():
            request.session.pop('empresa_id', None)
            return redirect('seleccionar_empresa')

        request.empresa = t_empresa.objects.get(id=empresa_id)
        return self.get_response(request)