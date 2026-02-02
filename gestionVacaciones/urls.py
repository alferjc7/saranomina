from django.urls import path
from gestionVacaciones.views import t_ciclos_LaboralView, calcular_fecha_fin_vacaciones

urlpatterns = [
    path("vacaciones/", t_ciclos_LaboralView.as_view(), name="vacaciones"),
    path("calcular-fecha-fin/",calcular_fecha_fin_vacaciones,name='calcular_fecha_fin_vacaciones'),
]