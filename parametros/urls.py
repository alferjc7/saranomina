from django.urls import path
from parametros.views import (tipos_contratosCreateView, tipo_contratosDeleteView, 
                              tipos_salariosCreateView, tipo_salariosDeleteView, 
                              tipos_cotizantesCreateView, tipo_cotizantesDeleteView,
                              subtipos_cotizantesCreateView, subtipo_cotizantesDeleteView,
                              bancosCreateView,bancosDeleteView)
urlpatterns = [
    path("tipos_contratos/", tipos_contratosCreateView.as_view(), name="tipos_contratos"),
    path("tipos_contratos_eliminar/<int:pk>/", tipo_contratosDeleteView.as_view(), name="tipos_contratos_eliminar"),
    path("tipos_salarios/", tipos_salariosCreateView.as_view(), name="tipos_salarios"),
    path("tipos_salarios_eliminar/<int:pk>/", tipo_salariosDeleteView.as_view(), name="tipos_salarios_eliminar"),
    path("tipos_cotizantes/", tipos_cotizantesCreateView.as_view(), name="tipos_cotizantes"),
    path("tipos_cotizantes_eliminar/<int:pk>/", tipo_cotizantesDeleteView.as_view(), name="tipos_cotizantes_eliminar"),
    path("subtipos_cotizantes/", subtipos_cotizantesCreateView.as_view(), name="subtipos_cotizantes"),
    path("subtipos_cotizantes_eliminar/<int:pk>/", subtipo_cotizantesDeleteView.as_view(), name="subtipos_cotizantes_eliminar"),
    path("bancos/", bancosCreateView.as_view(), name="bancos"),
    path("bancos_eliminar/<int:pk>/", bancosDeleteView.as_view(), name="bancos_eliminar"),
    
]