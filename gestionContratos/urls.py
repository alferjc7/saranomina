from django.urls import path
from gestionContratos.views import (t_contratosCreateView, 
                                    t_contrato_bancoCreateView, t_contrato_bancoDeleteView,
                                    t_contrato_entidadCreateView, t_contrato_entidadDeleteView,
                                    t_contrato_salarioCreateView, t_contrato_salarioDeleteView,
                                    t_contrato_deducibleCreateView, t_contrato_deducibleDeleteView, cargar_subtipos)
urlpatterns = [
    path("contratos/", t_contratosCreateView.as_view(), name="contratos"),
    path('contratos/<int:contrato_id>/bancos/',t_contrato_bancoCreateView.as_view(),name='contrato_banco'),
    path('contratos/<int:contrato_id>/bancos/<int:pk>',t_contrato_bancoDeleteView.as_view(),name='contrato_banco_eliminar'),
    path('contratos/<int:contrato_id>/entidades_ss/',t_contrato_entidadCreateView.as_view(),name='contrato_entidad_ss'),
    path('contratos/<int:contrato_id>/entidades_ss/<int:pk>',t_contrato_entidadDeleteView.as_view(),name='contrato_entidad_eliminar'),
    path('contratos/<int:contrato_id>/salario/',t_contrato_salarioCreateView.as_view(),name='contrato_salario'),
    path('contratos/<int:contrato_id>/salario/<int:pk>',t_contrato_salarioDeleteView.as_view(),name='contrato_salario_eliminar'),
    path('contratos/<int:contrato_id>/deducible/',t_contrato_deducibleCreateView.as_view(),name='contrato_deducible'),
    path('contratos/<int:contrato_id>/deducible/<int:pk>',t_contrato_deducibleDeleteView.as_view(),name='contrato_deducible_eliminar'),
    path('ajax/subtipos/', cargar_subtipos, name='ajax_subtipos'),


]