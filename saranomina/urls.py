from django.contrib import admin
from django.urls import path, include
from gestionIdentificacion.views import (inicio, resultado, logout_view)
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('admin/', admin.site.urls),
    path('inicio/', inicio, name='inicio'),
    path('buscar/', resultado),
    path('api/',include('api.urls')),
    path("accounts/", include("accounts.urls")),
    path("parametros/", include("parametros.urls")),
    path("gestionreportes/", include("gestionReportes.urls")),
    path("gestionclientes/", include("gestionClientes.urls")),
    path("gestioncontratos/", include("gestionContratos.urls")),
    path("gestionconceptos/", include("gestionConceptos.urls")),
    path("gestionnomina/", include("gestionNomina.urls")),
    path("gestionnovedades/", include("gestionNovedades.urls")),
    path("gestionvacaciones/", include("gestionVacaciones.urls")),
    path("gestionidentificacion/", include("gestionIdentificacion.urls")),
    path('logout/', logout_view, name='logout'),
    path('api/token/', obtain_auth_token),
]


