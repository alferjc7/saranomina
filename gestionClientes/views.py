from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.generic import CreateView, DeleteView
from gestionClientes.models import t_cliente, t_empresa
from gestionClientes.forms import t_cliente_form, t_empresa_form
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


class clienteCreateView(LoginRequiredMixin,CreateView):
    model = t_cliente
    form_class = t_cliente_form
    template_name = 'clientes.html'
    context_object_name = 'clientes'
    success_url = reverse_lazy('clientes')
    login_url = '/accounts/login/'           # opcional
    redirect_field_name = 'next'  # opcional

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        registros = t_cliente.objects.all().order_by('-pk')[:30]
        context['registros'] = registros
        return context
    
    def form_valid(self, form):
        pk = self.request.POST.get('pk')
        if pk:
            cliente = t_cliente.objects.get(pk=pk)
            for field, value in form.cleaned_data.items():
                setattr(cliente, field, value)
            cliente.save()
            messages.success(self.request, 'Registro actualizado correctamente')
        else:
            response = super().form_valid(form)
            messages.success(self.request, 'Registro creado correctamente')
        return redirect(self.success_url)

    def form_invalid(self, form):
        messages.error(self.request, 'Validar campos del formulario')
        return super().form_invalid(form)

class clienteDeleteView(LoginRequiredMixin,DeleteView):
    model = t_cliente
    success_url = reverse_lazy('clientes')
    login_url = 'accounts/login'

    def post(self, request, *args, **kwargs):
        messages.success(request, 'Cliente eliminado correctamente')
        return super().post(request, *args, **kwargs)

    
class empresasCreateView(LoginRequiredMixin, CreateView):
    model = t_empresa
    form_class = t_empresa_form
    template_name = 'empresas.html'
    context_object_name = 'empresas'
    success_url = reverse_lazy('empresas')
    login_url = '/accounts/login/'           # opcional
    redirect_field_name = 'next'  # opcional

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        registros = t_empresa.objects.all().order_by('-pk')[:30]
        context['registros'] = registros
        return context
    
    def form_valid(self, form):
        pk = self.request.POST.get('pk')
        print(pk)
        if pk:
            empresa = t_empresa.objects.get(pk=pk)
            for field, value in form.cleaned_data.items():
                setattr(empresa, field, value)
            empresa.save()
            messages.success(self.request, 'Registro actualizado correctamente')
        else:
            response = super().form_valid(form)
            messages.success(self.request, 'Registro creado correctamente')
        return redirect(self.success_url)
        
    def form_invalid(self, form):
        pk = self.request.POST.get('pk')
        print(pk)
        messages.error(self.request, 'Validar campos del formulario')
        return super().form_invalid(form)

class empresasDeleteView(LoginRequiredMixin,DeleteView):
    model = t_empresa
    success_url = reverse_lazy('empresas')
    login_url = 'accounts/login'

    def post(self, request, *args, **kwargs):
        messages.success(request, 'Empresa eliminado correctamente')
        return super().post(request, *args, **kwargs)