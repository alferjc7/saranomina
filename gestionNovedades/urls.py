from django.urls import path
from gestionNovedades.views import (t_novedadCreateView,t_novedadDeleteView,ajax_contratos,
                                    ajax_conceptos, ajax_periodosn)

urlpatterns = [
    path("novedad_temporal/", t_novedadCreateView.as_view(), name="novedad_temporal"),
    path("novedad_temporal_eliminar/<int:pk>/", t_novedadDeleteView.as_view(), name="novedad_temporal_eliminar"),
    path("ajax/contratos/", ajax_contratos, name="ajax_contratos"),
    path("ajax/conceptos/", ajax_conceptos, name="ajax_conceptos"),
    path("ajax/periodosn/", ajax_periodosn, name="ajax_periodosn"),
   
]