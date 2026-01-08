from django.urls import path
from gestionIdentificacion.views import (inicio, resultado, tipos_ide, identificaciones, 
                                         logout_view, t_beneficiarioCreateView, t_beneficiarioDeleteView)

urlpatterns = [
    path('identificaciones/', identificaciones, name= 'identificaciones'),
    path('tipos_ide/', tipos_ide, name= 'tipos_ide'),
    path('identificaciones/<int:id>/beneficiarios/',t_beneficiarioCreateView.as_view(),name='tbeneficiario'),
    path('identificaciones/<int:id>/beneficiarios/<int:pk>',t_beneficiarioDeleteView.as_view(),name='beneficiario_eliminar'),

]