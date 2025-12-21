from django.urls import path
from parametros.views import tipos_contratosCreateView, tipo_contratosDeleteView

urlpatterns = [
    path("tipos_contratos/", tipos_contratosCreateView.as_view(), name="tipos_contratos"),
    path("tipos_contratos_eliminar/<int:pk>/", tipo_contratosDeleteView.as_view(), name="tipos_contratos_eliminar"),


]