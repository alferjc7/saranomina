from django.urls import path
from gestionReportes.views import ReporteListView, parametrosreportesCreateView, parametrosreportesDeleteView, creareportesCreateView, generar_reporte


urlpatterns = [
    path("reportes/", ReporteListView.as_view(), name="reportes"),
    path("creareportes/", creareportesCreateView.as_view(), name="crea_reportes"),
    path('generar/<int:reporte_id>/', generar_reporte, name='generar_reporte'),
    path("parametros_reportes/", parametrosreportesCreateView.as_view(), name="parametros_reportes"),
    path("eliminar_parametros/<int:pk>/", parametrosreportesDeleteView.as_view(), name="eliminar_parametros"),

    
]