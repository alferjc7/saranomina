from datetime import datetime
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from parametros.models import (t_tipo_contrato, t_tipo_salario, 
                               t_tipo_cotizante, t_subtipo_cotizante,
                               t_banco)
from parametros.forms import (tipo_contratoform, tipo_salarioform, 
                              tipo_cotizanteform, subtipo_cotizanteform,
                              bancoform)
from django.views.generic import CreateView, DeleteView


# Create your views here.
class tipos_contratosCreateView(LoginRequiredMixin,CreateView):
    model = t_tipo_contrato
    form_class = tipo_contratoform
    template_name = 'tipos_contratos.html'
    context_object_name = 'tipos_contratos'
    success_url = reverse_lazy('tipos_contratos')
    login_url = '/accounts/login/'           # opcional
    redirect_field_name = 'next'  # opcional

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        registros = t_tipo_contrato.objects.all().order_by('-pk')[:30]
        context['registros'] = registros
        return context
    
    def form_valid(self, form):
        form.instance.date_created = datetime.now()
        form.instance.user_creator = self.request.user
        messages.success(self.request, 'Registro creado correctamente')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        print(form.errors)
        messages.error(self.request, 'Validar campos del formulario')
        return super().form_invalid(form)

class tipo_contratosDeleteView(LoginRequiredMixin,DeleteView):
    model = t_tipo_contrato
    success_url = reverse_lazy('tipos_contratos')
    login_url = 'accounts/login'

    def post(self, request, *args, **kwargs):
        messages.success(request, 'Tipo de contraro eliminado correctamente')
        return super().post(request, *args, **kwargs)

class tipos_salariosCreateView(LoginRequiredMixin,CreateView):
    model = t_tipo_salario
    form_class = tipo_salarioform
    template_name = 'tipos_salarios.html'
    context_object_name = 'tipos_salarios'
    success_url = reverse_lazy('tipos_salarios')
    login_url = '/accounts/login/'           # opcional
    redirect_field_name = 'next'  # opcional

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        registros = t_tipo_salario.objects.all().order_by('-pk')[:30]
        context['registros'] = registros
        return context
    
    def form_valid(self, form):
        form.instance.date_created = datetime.now()
        form.instance.user_creator = self.request.user
        messages.success(self.request, 'Registro creado correctamente')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        print(form.errors)
        messages.error(self.request, 'Validar campos del formulario')
        return super().form_invalid(form)
    
class tipo_salariosDeleteView(LoginRequiredMixin,DeleteView):
    model = t_tipo_salario
    success_url = reverse_lazy('tipos_salarios')
    login_url = 'accounts/login'

    def post(self, request, *args, **kwargs):
        messages.success(request, 'Tipo de contraro eliminado correctamente')
        return super().post(request, *args, **kwargs)
    

class tipos_cotizantesCreateView(LoginRequiredMixin,CreateView):
    model = t_tipo_cotizante
    form_class = tipo_cotizanteform
    template_name = 'tipos_cotizantes.html'
    context_object_name = 'tipos_cotizantes'
    success_url = reverse_lazy('tipos_cotizantes')
    login_url = '/accounts/login/'           # opcional
    redirect_field_name = 'next'  # opcional

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        registros = t_tipo_cotizante.objects.all().order_by('-pk')[:30]
        context['registros'] = registros
        return context
    
    def form_valid(self, form):
        form.instance.date_created = datetime.now()
        form.instance.user_creator = self.request.user
        messages.success(self.request, 'Registro creado correctamente')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        print(form.errors)
        messages.error(self.request, 'Validar campos del formulario')
        return super().form_invalid(form)
    
class tipo_cotizantesDeleteView(LoginRequiredMixin,DeleteView):
    model = t_tipo_cotizante
    success_url = reverse_lazy('tipos_cotizantes')
    login_url = 'accounts/login'

    def post(self, request, *args, **kwargs):
        messages.success(request, 'Tipo de cotizante eliminado correctamente')
        return super().post(request, *args, **kwargs)


class subtipos_cotizantesCreateView(LoginRequiredMixin,CreateView):
    model = t_tipo_cotizante
    form_class = subtipo_cotizanteform
    template_name = 'subtipos_cotizantes.html'
    context_object_name = 'subtipos_cotizantes'
    success_url = reverse_lazy('subtipos_cotizantes')
    login_url = '/accounts/login/'           # opcional
    redirect_field_name = 'next'  # opcional

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        registros = t_subtipo_cotizante.objects.all().order_by('-pk')[:30]
        context['registros'] = registros
        return context
    
    def form_valid(self, form):
        form.instance.date_created = datetime.now()
        form.instance.user_creator = self.request.user
        messages.success(self.request, 'Registro creado correctamente')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        print(form.errors)
        messages.error(self.request, 'Validar campos del formulario')
        return super().form_invalid(form)
    
class subtipo_cotizantesDeleteView(LoginRequiredMixin,DeleteView):
    model = t_subtipo_cotizante
    success_url = reverse_lazy('subtipos_cotizantes')
    login_url = 'accounts/login'

    def post(self, request, *args, **kwargs):
        messages.success(request, 'Subtipo de cotizante eliminado correctamente')
        return super().post(request, *args, **kwargs)

class bancosCreateView(LoginRequiredMixin,CreateView):
    model = t_banco
    form_class = bancoform
    template_name = 'bancos.html'
    context_object_name = 'bancos'
    success_url = reverse_lazy('bancos')
    login_url = '/accounts/login/'           # opcional
    redirect_field_name = 'next'  # opcional

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        registros = t_banco.objects.all().order_by('-pk')[:30]
        context['registros'] = registros
        return context
    
    def form_valid(self, form):
        form.instance.date_created = datetime.now()
        form.instance.user_creator = self.request.user
        messages.success(self.request, 'Registro creado correctamente')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        print(form.errors)
        messages.error(self.request, 'Validar campos del formulario')
        return super().form_invalid(form)
    
class bancosDeleteView(LoginRequiredMixin,DeleteView):
    model = t_banco
    success_url = reverse_lazy('bancos')
    login_url = 'accounts/login'

    def post(self, request, *args, **kwargs):
        messages.success(request, 'Banco eliminado correctamente')
        return super().post(request, *args, **kwargs)

