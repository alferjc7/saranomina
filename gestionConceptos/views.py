from datetime import datetime
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from gestionClientes.models import t_empresa
from gestionConceptos.models import t_conceptos, t_concepto_empresa
from gestionConceptos.forms import t_conceptosform, t_concepto_empresaform
from django.views.generic import CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.db import IntegrityError


# Create your views here.
class t_conceptosCreateView(LoginRequiredMixin, CreateView):
    model = t_conceptos
    form_class = t_conceptosform
    template_name = 'conceptos.html'
    context_object_name = 'conceptos'
    success_url = reverse_lazy('conceptos')
    login_url = '/accounts/login/'           # opcional
    redirect_field_name = 'next'  # opcional

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        registros = t_conceptos.objects.all().order_by('-pk')[:30]
        context['registros'] = registros
        return context
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        pk = self.request.POST.get('pk')
        if pk:
            kwargs['instance'] = t_conceptos.objects.get(pk=pk)
        return kwargs
    
    def form_valid(self, form):
        pk = self.request.POST.get('pk')
        if pk:
            conceptos = t_conceptos.objects.get(pk=pk)
            for field, value in form.cleaned_data.items():
                setattr(conceptos, field, value)
            conceptos.save()
            messages.success(self.request, 'Concepto actualizado correctamente')
        else:
            messages.success(self.request, 'Registro creado correctamente')
            return super().form_valid(form)
        return redirect(self.success_url)

    def form_invalid(self, form):
        messages.error(self.request, 'Validar campos del formulario')
        return super().form_invalid(form)

class t_conceptosDeleteView(LoginRequiredMixin,DeleteView):
    model = t_conceptos
    success_url = reverse_lazy('conceptos')
    login_url = 'accounts/login'

    def post(self, request, *args, **kwargs):
        messages.success(request, 'Concepto eliminado correctamente')
        return super().post(request, *args, **kwargs)
    

class t_concepto_empresaCreateView(LoginRequiredMixin,CreateView):
    model = t_concepto_empresa
    form_class = t_concepto_empresaform
    template_name = 'concepto_empresa.html'

    def get_initial(self):
        initial = super().get_initial()

        empresa_id = self.request.session.get('empresa_id')
        empresa = get_object_or_404(t_empresa, pk=empresa_id)
        concepto = get_object_or_404(t_conceptos, pk=self.kwargs['id'])

        existe = t_concepto_empresa.objects.filter(
            empresa=empresa,
            cod_concepto=concepto
        ).exists()

        if not existe:
            initial['desc_concepto_emp'] = concepto.desc_concepto

        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        empresa_id = self.request.session.get('empresa_id')
        empresa = get_object_or_404(t_empresa ,pk=empresa_id)

        concepto = get_object_or_404(t_conceptos ,pk=self.kwargs['id'])

        context['concepto'] = concepto
        context['registros'] = t_concepto_empresa.objects.filter(cod_concepto=concepto,
                                                                 empresa = empresa)        
        return context
     
    def form_valid(self, form):
        try:
            pk = self.request.POST.get('pk')
            empresa_id = self.request.session.get('empresa_id')
            empresa =  get_object_or_404(t_empresa ,pk=empresa_id)
            print(empresa)
            if pk:
                conceptoemp = t_concepto_empresa.objects.get(pk=pk)
                for field, value in form.cleaned_data.items():
                    setattr(conceptoemp, field, value)
                conceptoemp.save()
                messages.success(self.request, 'Concepto empresa actualizado correctamente')
                return redirect(self.get_success_url())
            else:
                concepto = get_object_or_404(t_conceptos ,pk=self.kwargs['id'])
                form.instance.empresa = empresa  
                form.instance.cod_concepto = concepto
                form.instance.date_created = datetime.now()
                form.instance.user_creator = self.request.user
                response = super().form_valid(form) 
                messages.success(self.request, 'Registro creado correctamente')
                return response
    
        except IntegrityError:
            form.add_error(
                None,
                'Ya existe este concepto configurado para la empresa.')   
            return self.form_invalid(form)
            
        
    def form_invalid(self, form):
        print(form.errors)
        messages.error(self.request, 'Validar campos del formulario')
        return super().form_invalid(form)
    
    def get_success_url(self):
        return reverse(
            'concepto_empresa',
            kwargs={'id': self.kwargs['id']} 
        )

class t_concepto_empresaDeleteView(LoginRequiredMixin,DeleteView):
    model = t_concepto_empresa
    login_url = 'accounts/login'

    def get_success_url(self):
        return reverse_lazy(
            'concepto_empresa',
            kwargs={'id': self.object.cod_concepto_id} 
        )
    
    def get_queryset(self):
        # 🔒 evita borrar registros de otra empresa
        empresa_id = self.request.session.get('empresa_id')
        return super().get_queryset().filter(empresa_id=empresa_id)
    
    
    def post(self, request, *args, **kwargs):
        messages.success(request, 'Registro eliminado correctamente')
        return super().post(request, *args, **kwargs)

