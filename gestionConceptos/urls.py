from django.urls import path
from gestionConceptos.views import (t_conceptosCreateView, t_conceptosDeleteView,
                                    t_concepto_empresaCreateView, t_concepto_empresaDeleteView,
                                    grupo_conceptoCreateView, grupo_conceptoDeleteView,
                                    grupo_conceptodetDeleteView, grupo_conceptodetCreateView)

urlpatterns = [
    path("conceptos/", t_conceptosCreateView.as_view(), name="conceptos"),
    path("conceptos_eliminar/<int:pk>/", t_conceptosDeleteView.as_view(), name="conceptos_eliminar"),
    path('conceptos/<int:id>/concepto_emp/',t_concepto_empresaCreateView.as_view(),name='concepto_empresa'),
    path('conceptos/<int:id>/concepto_emp/<int:pk>',t_concepto_empresaDeleteView.as_view(),name='concepto_empresa_eliminar'),
    path("grupo_concepto/", grupo_conceptoCreateView.as_view(), name="grupo_concepto"),
    path("grupo_concepto/<int:pk>/", grupo_conceptoDeleteView.as_view(), name="grupo_concepto_eliminar"),
    path("grupo_concepto/<int:id>/detalle/", grupo_conceptodetCreateView.as_view(), name="grupo_concepto_det"),
    path("grupo_concepto/<int:id>/detalle/<int:pk>", grupo_conceptodetDeleteView.as_view(), name="grupo_concepto_det_eliminar"),
    
]