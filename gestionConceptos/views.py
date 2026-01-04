from django.shortcuts import render
from django.contrib import messages
from gestionConceptos.models import t_conceptos
from gestionConceptos.forms import t_conceptosform
from django.views.generic import CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

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
    
    def form_valid(self, form):
        messages.success(self.request, 'Registro creado correctamente')
        return super().form_valid(form)
        
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
