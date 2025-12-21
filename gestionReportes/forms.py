from django.forms import ModelForm
from .models import Reporte,ParametroReporte

class reportes_form(ModelForm):
    class Meta:
        model = Reporte
        fields = '__all__'

class parametrosreportes_form(ModelForm):
    class Meta:
        model = ParametroReporte
        fields = '__all__'
