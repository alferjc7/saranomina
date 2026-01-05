import os
import uuid
from django.contrib import messages
from django.conf import settings
from django.http import FileResponse, Http404, HttpResponse
from django.shortcuts import redirect, render,  get_object_or_404
from django.views.generic import ListView, CreateView, DeleteView
from .models import Reporte, ParametroReporte
from .forms import parametrosreportes_form, reportes_form
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from pyreportjasper import PyReportJasper
from datetime import datetime
import mimetypes

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
        context = super().get_context_data(**kwargs)
        registros = Reporte.objects.all().order_by('-pk')[:30]
        context['registros'] = registros
        return context
    
    def form_valid(self, form):
        pk = self.request.POST.get('pk')
        if pk:
            reportes = Reporte.objects.get(pk=pk)
            for field, value in form.cleaned_data.items():
                setattr(reportes, field, value)
            reportes.save()
            messages.success(self.request, 'Reporte actualizado correctamente')
        else:
            form.instance.date_created = datetime.now()
            form.instance.user_creator = self.request.user
            messages.success(self.request, 'Registro creado correctamente')
            return super().form_valid(form)
        return redirect(self.success_url)
    
    def form_invalid(self, form):
        return super().form_invalid(form)

class reportesDeleteView(LoginRequiredMixin,DeleteView):
    model = Reporte
    success_url = reverse_lazy('crea_reportes')
    login_url = 'accounts/login'

    def post(self, request, *args, **kwargs):
        messages.success(request, 'Reporte eliminado correctamente')
        return super().post(request, *args, **kwargs)

    
class parametrosreportesCreateView(LoginRequiredMixin,CreateView):
    model = ParametroReporte
    form_class = parametrosreportes_form
    template_name = 'parametrosreportes.html'
    context_object_name = 'parametros_reportes'
    success_url = reverse_lazy('parametros_reportes')
    login_url = '/accounts/login/'           # opcional
    redirect_field_name = 'next'  # opcional

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        registros = ParametroReporte.objects.all().order_by('-pk')[:30]
        context['registros'] = registros
        return context
    
    def form_valid(self, form):
        pk = self.request.POST.get('pk')
        if pk:
            Parametro_reportes = ParametroReporte.objects.get(pk=pk)
            for field, value in form.cleaned_data.items():
                setattr(Parametro_reportes, field, value)
            Parametro_reportes.save()
            messages.success(self.request, 'Parametro reporte actualizado correctamente')
        else:
            messages.success(self.request, 'Registro creado correctamente')
            return super().form_valid(form)
        return redirect(self.success_url)

    def form_invalid(self, form):
        return super().form_invalid(form)
    
class parametrosreportesDeleteView(LoginRequiredMixin,DeleteView):
    model = ParametroReporte
    success_url = reverse_lazy('parametros_reportes')
    login_url = 'accounts/login'

    def post(self, request, *args, **kwargs):
        messages.success(request, 'Parametro eliminado correctamente')
        return super().post(request, *args, **kwargs)
 

def generar_reporte(request, reporte_id):
    reporte = get_object_or_404(Reporte, id=reporte_id)
    parametros = ParametroReporte.objects.filter(reporte=reporte)

    if request.method == 'POST':
        valores = {}
        for p in parametros:
            valor = request.POST.get(p.nombre)
            if valor == '':
                valor = None
            valores[p.nombre] = valor
        formato = request.POST.get('formato')  # pdf, xls, csv, html
        print(valores)
        jasper_path = os.path.join(settings.BASE_DIR, reporte.ruta_jasper)
        print(jasper_path)
        if not os.path.exists(jasper_path):
            raise Http404("Archivo .jasper no encontrado")

        output_dir = os.path.join(settings.BASE_DIR, 'gestionReportes\output')
        os.makedirs(output_dir, exist_ok=True)

        output_name = f"reporte_{uuid.uuid4()}"
        output_file = os.path.join(output_dir, output_name)
        db = settings.DATABASES['default']

        db_config = {
            'driver': 'postgres',
            'username': db['USER'],
            'password': db['PASSWORD'],
            'host': db['HOST'],
            'database': db['NAME'],
            'schema' : 'public',
            'port': db['DATABASE_PORT'],
            'jdbc_driver':'org.postgresql.Driver'
        }

        jasper = PyReportJasper()
        jasper.process(
            input_file=jasper_path,
            output_file=output_file,
            format_list=[formato],
            db_connection=db_config,
            parameters = valores,
        )

        archivo_final = f"{output_file}.{formato}"
        if not os.path.exists(archivo_final):
            raise Http404("Error generando el reporte")

        mime_type, _ = mimetypes.guess_type(archivo_final)

     
        if formato == 'html':
            with open(archivo_final, 'r', encoding='utf-8', errors='ignore') as f:
                response = HttpResponse(f.read(), content_type='text/html')
                response['Content-Disposition'] = 'inline'
                return response
        elif formato == 'pdf':
            return FileResponse(
                open(archivo_final, 'rb'),
                as_attachment=False,  # clave
                content_type='application/pdf',
                filename=f"{reporte.nombre}.pdf"
                )
        else:
            return FileResponse(
                open(archivo_final, 'rb'),
                as_attachment=True,
                content_type=mime_type,
                filename=f"{reporte.nombre}.{formato}"
                )

    return render(request, 'generar_reporte.html', {
        'reporte': reporte,
        'parametros': parametros
    })
    
