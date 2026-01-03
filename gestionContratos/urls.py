from django.urls import path
from gestionContratos.views import (t_contratosCreateView, t_contrato_bancoCreateView)
urlpatterns = [
    path("contratos/", t_contratosCreateView.as_view(), name="contratos"),
    path('contratos/<int:contrato_id>/bancos/',t_contrato_bancoCreateView.as_view(),name='contrato_banco')
]