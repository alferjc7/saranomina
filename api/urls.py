from django.urls import include, path
from .views import PingApiView, SaludoApiView, CargoApiView, areaApiView, AreaListCreateView, AreaDetailCreateView, listaViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'listas', listaViewSet, basename='listas')

urlpatterns = [
    path('ping/',PingApiView.as_view(),name='ping'),
    path('salu/',SaludoApiView.as_view(),name='salu'),
    #API VIEW
    path('cargos/',CargoApiView.as_view(),name='cargos'),
    path('cargos/<int:pk>/',CargoApiView.as_view(),name='cargo_detail'),
    path('areas/',areaApiView.as_view(),name='areas'),
    path('areas/<int:pk>/',areaApiView.as_view(),name='areas_detail'),
    #GENERIC VIEWS
    path('areas_list/',AreaListCreateView.as_view(),name='areas_list'),
    path('areas_list/<int:pk>/',AreaDetailCreateView.as_view(),name='areas_detail'),
     # VIEWSETS + Routers
    path('', include(router.urls))
]