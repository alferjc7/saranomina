from django.urls import path
from gestionNomina.views import (periodo_nominaListView, periodo_nominaDeleteView,
                                 logica_calculoCreateView,logica_calculoDeleteView,
                                 conceptos_por_empresa, procedimientos_por_concepto,
                                 AcumuladosListView, ProcesamientoNominaView,
                                 procesamiento_detalleListView)

urlpatterns = [
    path("periodo_nomina/", periodo_nominaListView.as_view(), name="periodo_nomina"), 
    path("periodo_nomina/<int:pk>/", periodo_nominaDeleteView.as_view(), name="periodo_nomina_eliminar"),
    path("logica_calculo/", logica_calculoCreateView.as_view(), name="logica_calculo"), 
    path("logica_calculo/<int:pk>/", logica_calculoDeleteView.as_view(), name="logica_calculo_eliminar"),
    path('ajax/conceptos-empresa/',conceptos_por_empresa,name='ajax_conceptos_empresa'), 
    path('ajax/procedimientos-concepto/',procedimientos_por_concepto,name='ajax_procedimientos_concepto'),
    path("acumulados/", AcumuladosListView.as_view(), name="acumulados"), 
    path("procesamiento/",ProcesamientoNominaView.as_view(),name="procesamiento_nomina"),
    path("procesamiento/<int:id>/detalle/",procesamiento_detalleListView.as_view(),name="procesamiento_detalle"),

]