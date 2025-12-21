from django.urls import path
from gestionClientes.views import clienteCreateView, clienteDeleteView, empresasCreateView, empresasDeleteView

urlpatterns = [
    path("clientes/", clienteCreateView.as_view(), name="clientes"),
    path("cliente_eliminar/<int:pk>/", clienteDeleteView.as_view(), name="cliente_eliminar"),
    path("empresas/", empresasCreateView.as_view(), name="empresas"),
    path("empresa_eliminar/<int:pk>/", empresasDeleteView.as_view(), name="empresa_eliminar"),

]