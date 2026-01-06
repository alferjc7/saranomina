from django.urls import path
from gestionConceptos.views import (t_conceptosCreateView, t_conceptosDeleteView,
                                    t_concepto_empresaCreateView, t_concepto_empresaDeleteView)

urlpatterns = [
    path("conceptos/", t_conceptosCreateView.as_view(), name="conceptos"),
    path("conceptos_eliminar/<int:pk>/", t_conceptosDeleteView.as_view(), name="conceptos_eliminar"),
    path('conceptos/<int:id>/concepto_emp/',t_concepto_empresaCreateView.as_view(),name='concepto_empresa'),
    path('conceptos/<int:id>/concepto_emp/<int:pk>',t_concepto_empresaDeleteView.as_view(),name='concepto_empresa_eliminar'),

]