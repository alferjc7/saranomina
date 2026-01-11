from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView
from gestionNomina.models import t_periodo_nomina
from gestionNomina.utils import crear_periodos
from gestionNomina.forms import GenerarPeriodoNominaForm
from gestionClientes.models import t_empresa
from django.contrib import messages
from parametros.models import t_tipo_nomina

# Create your views here.    
class periodo_nominaListView(LoginRequiredMixin,ListView):
    model = t_periodo_nomina
    template_name = 'periodo_nomina.html'
    context_object_name = 'periodo_nomina'

    def get_queryset(self):
        qs = t_periodo_nomina.objects.filter(
            empresa=self.request.session.get('empresa_id')
        )

        tipo = self.request.GET.get('tipo')
        anio = self.request.GET.get('anio')
        mes = self.request.GET.get('mes')

        if tipo:
            qs = qs.filter(tipo_nomina_id=tipo)

        if anio:
            qs = qs.filter(anio=anio)

        if mes:
            qs = qs.filter(mes=mes)

        return qs
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tipos_nomina'] = t_tipo_nomina.objects.all()
        context['tipo_seleccionado'] = self.request.GET.get('tipo')
        context['form'] = GenerarPeriodoNominaForm()
        return context

    def post(self, request, *args, **kwargs):
        form = GenerarPeriodoNominaForm(request.POST)

        if form.is_valid():
            ejecucion_automatica = form.cleaned_data['ejecucion_automatica']
            empresa = t_empresa.objects.get(id=request.session.get('empresa_id'))
            tipo_nomina = form.cleaned_data['tipo_nomina']
            anio = form.cleaned_data['anio']
            mes = form.cleaned_data['mes']
            periodo = form.cleaned_data['periodo']
            fecha_inicio = form.cleaned_data['fecha_inicio']
            fecha_fin = form.cleaned_data['fecha_fin']

            existe = False
            validar_adicionales = False
            # Evitar duplicados
            if tipo_nomina.asigna_contrato == False :
                if all([tipo_nomina, anio, mes, periodo, fecha_inicio, fecha_fin]):
                    existe = t_periodo_nomina.objects.filter(
                        empresa = empresa,
                        tipo_nomina = tipo_nomina,
                        anio = anio,
                        mes = mes,
                        periodo  = periodo,
                        fecha_inicio = fecha_inicio,
                        fecha_fin = fecha_fin
                    ).exists()
                
                else:
                    validar_adicionales = True
                    messages.error(request, "Para este tipo de Nomina se deben diligenciar todos los campos.")    
            else:
                existe = t_periodo_nomina.objects.filter(
                    empresa = empresa,
                    tipo_nomina = tipo_nomina,
                    anio = anio
                ).exists()

            if existe:
                messages.error(request, "Ya existen períodos para ese año y tipo de nómina.")
            else:
                try:
                    crear_periodos(
                        ejecucion_automatica,
                        empresa,
                        tipo_nomina,
                        anio,
                        mes,
                        periodo,
                        fecha_inicio,
                        fecha_fin
                    )
                    if validar_adicionales == False:
                        messages.success(request, "Períodos creados correctamente.")
                except ValueError as e:
                    messages.error(request, str(e))
        else:
            print(form.errors)

        return redirect('periodo_nomina')
    
class periodo_nominaDeleteView(LoginRequiredMixin,DeleteView):
    model = t_periodo_nomina
    success_url = reverse_lazy('periodo_nomina')
    login_url = 'accounts/login'

    def post(self, request, *args, **kwargs):
        messages.success(request, 'Periodo eliminado correctamente')
        return super().post(request, *args, **kwargs)
