from django.urls import path
from gestionNovedades.views import (t_novedadCreateView,t_novedadDeleteView,ajax_contratos,
                                    ajax_conceptos, ajax_periodosn, t_novedad_fijaCreateView,
                                    t_novedad_fijaDeleteView, t_novedadFijaDetListView)

urlpatterns = [
    path("novedad_temporal/", t_novedadCreateView.as_view(), name="novedad_temporal"),
    path("novedad_temporal_eliminar/<int:pk>/", t_novedadDeleteView.as_view(), name="novedad_temporal_eliminar"),
    path("novedad_fija/", t_novedad_fijaCreateView.as_view(), name="novedad_fija"),
    path("novedad_fija_eliminar/<int:pk>/", t_novedad_fijaDeleteView.as_view(), name="novedad_fija_eliminar"),
    path('novedad_fija/<int:novedad_id>/detalle/',t_novedadFijaDetListView.as_view(),name='novedad_fijadet'),
    path("ajax/contratos/", ajax_contratos, name="ajax_contratos"),
    path("ajax/conceptos/", ajax_conceptos, name="ajax_conceptos"),
    path("ajax/periodosn/", ajax_periodosn, name="ajax_periodosn"),
   
]