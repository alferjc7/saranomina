from django.urls import path
from gestionNomina.views import periodo_nominaListView, periodo_nominaDeleteView

urlpatterns = [
    path("periodo_nomina/", periodo_nominaListView.as_view(), name="periodo_nomina"), 
    path("periodo_nomina/<int:pk>/", periodo_nominaDeleteView.as_view(), name="periodo_nomina_eliminar"), 
]