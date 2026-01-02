from django.urls import path
from gestionClientes.views import (clienteCreateView, clienteDeleteView, 
                                   empresasCreateView, empresasDeleteView,
                                   userempresaCreateView, userempresasDeleteView,
                                   seleccionar_empresa)

urlpatterns = [
    path("clientes/", clienteCreateView.as_view(), name="clientes"),
    path("cliente_eliminar/<int:pk>/", clienteDeleteView.as_view(), name="cliente_eliminar"),
    path("empresas/", empresasCreateView.as_view(), name="empresas"),
    path("empresa_eliminar/<int:pk>/", empresasDeleteView.as_view(), name="empresa_eliminar"),
    path("user_empresa/", userempresaCreateView.as_view(), name="user_empresa"),
    path("user_empresa_eliminar/<int:pk>/", userempresasDeleteView.as_view(), name="user_empresa_eliminar"),
    path("seleccionar_empresa/", seleccionar_empresa, name="seleccionar_empresa"),

]