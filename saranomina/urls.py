"""
URL configuration for saranomina project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from gestionIdentificacion.views import inicio, resultado, tipos_ide, identificaciones, BeneficiarioCreateView, BeneficiarioDeleteView, logout_view
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('admin/', admin.site.urls),
    path('inicio/', inicio, name='inicio'),
    path('buscar/', resultado),
    path('tipos_ide/', tipos_ide, name= 'tipos_ide'),
    path('identificaciones/', identificaciones, name= 'identificaciones'),
    path('api/',include('api.urls')),
    path("accounts/", include("accounts.urls")),
    path("parametros/", include("parametros.urls")),
    path("gestionreportes/", include("gestionReportes.urls")),
    path("gestionclientes/", include("gestionClientes.urls")),
    path("gestioncontratos/", include("gestionContratos.urls")),
    path('beneficiarios/',BeneficiarioCreateView.as_view(),name='beneficiarios'),
    path('beneficiarios/eliminar/<int:pk>/',BeneficiarioDeleteView.as_view(),name='beneficiario_eliminar'),
    path('logout/', logout_view, name='logout'),
    path('api/token/', obtain_auth_token),
]


