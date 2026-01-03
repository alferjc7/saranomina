from datetime import datetime
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DeleteView
from gestionContratos.models import t_contrato, t_contrato_banco
from gestionContratos.forms import t_contratoform, t_contrato_banco_form


# Create your views here.
class t_contratosCreateView(LoginRequiredMixin,CreateView):
    model = t_contrato
    form_class = t_contratoform
    template_name = 'contratos.html'
    context_object_name = 'contratos'
    success_url = reverse_lazy('contratos')
    login_url = '/accounts/login/'           # opcional
    redirect_field_name = 'next'  # opcional

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        registros = t_contrato.objects.filter(empresa_id = self.request.session.get('empresa_id'))
        context['registros'] = registros
        return context
    
    def form_valid(self, form):
        print("aqui" + self.request.session.get('empresa_id'))
        form.instance.empresa_id = self.request.session.get('empresa_id')
        form.instance.date_created = datetime.now()
        form.instance.user_creator = self.request.user
        messages.success(self.request, 'Registro creado correctamente')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        print(form.errors)
        messages.error(self.request, 'Validar campos del formulario')
        return super().form_invalid(form)


# Create your views here.
class t_contrato_bancoCreateView(LoginRequiredMixin,CreateView):
    model = t_contrato_banco
    form_class = t_contrato_banco_form
    template_name = 'contrato_banco.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        contrato = get_object_or_404(t_contrato,pk=self.kwargs['contrato_id'])

        context['contrato'] = contrato
        context['registros'] = t_contrato_banco.objects.filter(contrato=contrato)
        
        return context
     
    def form_valid(self, form):
        form.instance.contrato_id = self.kwargs['contrato_id']
        form.instance.date_created = datetime.now()
        form.instance.user_creator = self.request.user
        messages.success(self.request, 'Registro creado correctamente')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        print(form.errors)
        messages.error(self.request, 'Validar campos del formulario')
        return super().form_invalid(form)
    
    def get_success_url(self):
        return reverse(
            'contrato_banco',
            kwargs={'contrato_id': self.kwargs['contrato_id']}
        )
