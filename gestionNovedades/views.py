from django.shortcuts import render,redirect
from django.views.generic import CreateView, DeleteView, ListView
from gestionNovedades.models import t_novedad_temporal, t_novedad_fija, t_novedad_fija_det
from gestionNovedades.forms import t_novedad_temporalform, t_novedad_fijaform
from gestionContratos.models import t_contrato
from gestionConceptos.models import t_concepto_empresa
from gestionNomina.models import t_periodo_nomina
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse

# Create your views here.
def ajax_contratos(request):
    q = request.GET.get('q', '').strip()
    page = int(request.GET.get('page', 1))

    queryset = t_contrato.objects.filter(empresa_id = request.session.get('empresa_id'))

    if q:
        terms = q.split()  
        q_filter = Q()

        for term in terms:
            q_filter &= (
                Q(cod_contrato__icontains=term) |
                Q(identificacion__nombre__icontains=term) |
                Q(identificacion__segundo_nombre__icontains=term) |
                Q(identificacion__apellido__icontains=term) |
                Q(identificacion__segundo_apellido__icontains=term)
            )

        queryset = queryset.filter(q_filter)

    queryset = queryset.order_by('-id')

    paginator = Paginator(queryset, 30)
    page_obj = paginator.get_page(page)

    results = []
    for item in page_obj:
        results.append({
            "id": item.id,
            "text": f"{item.cod_contrato} - {nombre_completo(item)}"
        })

    return JsonResponse({
        "results": results,
        "pagination": {
            "more": page_obj.has_next()
        }
    })

def ajax_conceptos(request):
    q = request.GET.get('q', '').strip()
    page = int(request.GET.get('page', 1))

    queryset = t_concepto_empresa.objects.filter(empresa_id = request.session.get('empresa_id'))

    if q:
        terms = q.split()  
        q_filter = Q()

        for term in terms:
            q_filter &= (
                Q(cod_concepto__cod_concepto__icontains=term) |
                Q(desc_concepto_emp__icontains=term)
            )

        queryset = queryset.filter(q_filter)

    queryset = queryset.order_by('-id')

    paginator = Paginator(queryset, 30)
    page_obj = paginator.get_page(page)

    results = []
    for item in page_obj:
        results.append({
            "id": item.id,
            "text": f"{item.cod_concepto.cod_concepto} - {item.desc_concepto_emp}"
        })

    return JsonResponse({
        "results": results,
        "pagination": {
            "more": page_obj.has_next()
        }
    })

def ajax_periodosn(request):
    q = request.GET.get('q', '').strip()
    page = int(request.GET.get('page', 1))

    queryset = t_periodo_nomina.objects.filter(empresa_id = request.session.get('empresa_id'),
                                               estado = True)

    if q:
        terms = q.split()  
        q_filter = Q()

        for term in terms:
            q_filter &= (
                Q(codigo__icontains=term) |
                Q(anio__icontains=term) |
                Q(mes__icontains=term) |
                Q(periodo__icontains=term) 
            )

        queryset = queryset.filter(q_filter)

    queryset = queryset.order_by('-id')

    paginator = Paginator(queryset, 30)
    page_obj = paginator.get_page(page)

    results = []
    for item in page_obj:
        results.append({
            "id": item.id,
            "text": f"{item.codigo} - {item.anio} - {item.mes}- {item.periodo}"
        })

    return JsonResponse({
        "results": results,
        "pagination": {
            "more": page_obj.has_next()
        }
    })


def nombre_completo(item):
    return " ".join(filter(None, [
        item.identificacion.nombre,
        item.identificacion.segundo_nombre,
        item.identificacion.apellido,
        item.identificacion.segundo_apellido
    ]))


class t_novedadCreateView(LoginRequiredMixin, CreateView):
    model = t_novedad_temporal
    form_class = t_novedad_temporalform
    template_name = 'novedad_temporal.html'
    context_object_name = 'novedad_temporal'
    success_url = reverse_lazy('novedad_temporal')
    login_url = '/accounts/login/'         
    redirect_field_name = 'next'  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        empresa_id = self.request.session.get('empresa_id')
        registros = t_novedad_temporal.objects.filter(contrato__empresa_id=empresa_id, estado = True)
        context['registros'] = registros

        return context
        
    def form_valid(self, form):
        pk = self.request.POST.get('pk')
        if pk:
            novedad = t_novedad_temporal.objects.get(pk=pk)
            for field, value in form.cleaned_data.items():
                setattr(novedad, field, value)
            novedad.save()
            messages.success(self.request, 'Registro actualizado correctamente')
        else:
            messages.success(self.request, 'Registro creado correctamente')
            return super().form_valid(form)
        return redirect(self.success_url)

    def form_invalid(self, form):
        messages.error(self.request, 'Validar campos del formulario')
        return super().form_invalid(form)

class t_novedadDeleteView(LoginRequiredMixin,DeleteView):
    model = t_novedad_temporal
    success_url = reverse_lazy('novedad_temporal')
    login_url = 'accounts/login'

    def post(self, request, *args, **kwargs):
        messages.success(request, 'Novedad eliminada correctamente')
        return super().post(request, *args, **kwargs)
    


class t_novedad_fijaCreateView(LoginRequiredMixin, CreateView):
    model = t_novedad_fija
    form_class = t_novedad_fijaform
    template_name = 'novedad_fija.html'
    context_object_name = 'novedad_fija'
    success_url = reverse_lazy('novedad_fija')
    login_url = '/accounts/login/'         
    redirect_field_name = 'next'  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        empresa_id = self.request.session.get('empresa_id')
        registros = t_novedad_fija.objects.filter(contrato__empresa_id=empresa_id, estado = True)
        context['registros'] = registros

        return context
        
    def form_valid(self, form):
        pk = self.request.POST.get('pk')
        if pk:
            novedad = t_novedad_fija.objects.get(pk=pk)
            for field, value in form.cleaned_data.items():
                setattr(novedad, field, value)
            novedad.save()
            messages.success(self.request, 'Registro actualizado correctamente')
        else:
            messages.success(self.request, 'Registro creado correctamente')
            return super().form_valid(form)
        return redirect(self.success_url)

    def form_invalid(self, form):
        messages.error(self.request, 'Validar campos del formulario')
        return super().form_invalid(form)

class t_novedad_fijaDeleteView(LoginRequiredMixin,DeleteView):
    model = t_novedad_fija
    success_url = reverse_lazy('novedad_fija')
    login_url = 'accounts/login'

    def post(self, request, *args, **kwargs):
        messages.success(request, 'Novedad eliminada correctamente')
        return super().post(request, *args, **kwargs)

class t_novedadFijaDetListView(ListView):
    model = t_novedad_fija_det
    template_name = 'novedad_fijadet.html'
    context_object_name = 'novedad_fijadet'

    def get_queryset(self):
        novedad_id = self.kwargs['novedad_id']
        return (
            t_novedad_fija_det.objects.filter(novedad_id=novedad_id).order_by('anio', 'mes', 'periodo')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['novedad'] = t_novedad_fija.objects.get(
            id=self.kwargs['novedad_id']
        )
        return context

