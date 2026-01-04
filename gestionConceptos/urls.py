from django.urls import path
from gestionConceptos.views import t_conceptosCreateView, t_conceptosDeleteView

urlpatterns = [
    path("conceptos/", t_conceptosCreateView.as_view(), name="conceptos"),
    path("conceptos_eliminar/<int:pk>/", t_conceptosDeleteView.as_view(), name="conceptos_eliminar"),
]