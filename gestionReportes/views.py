from django.shortcuts import render,  get_object_or_404
from django.views.generic import ListView, CreateView, DeleteView
from .models import Reporte, ParametroReporte
from .forms import parametrosreportes_form, reportes_form
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

class ReporteListView(LoginRequiredMixin,ListView):
    model = Reporte
    template_name = 'reportes.html'
    context_object_name = 'reportes'

    def get_queryset(self):
        return Reporte.objects.filter(activo=True)
    
class creareportesCreateView(LoginRequiredMixin,CreateView):
    model = Reporte
    form_class = reportes_form
    template_name = 'creareportes.html'
    context_object_name = 'crea_reportes'
    success_url = reverse_lazy('crea_reportes')
    login_url = '/accounts/login/'           # opcional
    redirect_field_name = 'next'  # opcional

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)
    
    def form_valid(self, form):
        return super().form_valid(form)
    
    def form_invalid(self, form):
        return super().form_invalid(form)

    
class parametrosreportesCreateView(LoginRequiredMixin,CreateView):
    model = ParametroReporte
    form_class = parametrosreportes_form
    template_name = 'parametrosreportes.html'
    context_object_name = 'parametros_reportes'
    success_url = reverse_lazy('parametros_reportes')
    login_url = '/accounts/login/'           # opcional
    redirect_field_name = 'next'  # opcional

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)
    def form_valid(self, form):
        return super().form_valid(form)
    def form_invalid(self, form):
        return super().form_invalid(form)
    
class parametrosreportesDeleteView(LoginRequiredMixin,DeleteView):
    model = ParametroReporte
    success_url = reverse_lazy('parametros_reportes')
    login_url = 'accounts/login'

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
 

def generar_reporte(request, reporte_id):
    reporte = get_object_or_404(Reporte, id=reporte_id)
    parametros = ParametroReporte.objects.filter(reporte=reporte)

    if request.method == 'POST':
        valores = {}
        for p in parametros:
            valores[p.nombre] = request.POST.get(p.nombre)

        formato = request.POST.get('formato')  # pdf, xls, csv, html

        # aquí luego llamaremos a Jasper
        return render(request, 'reportes/procesando.html')

    return render(request, 'generar_reporte.html', {
        'reporte': reporte,
        'parametros': parametros
    })
    
