from datetime import datetime
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DeleteView
from gestionContratos.models import (t_contrato, t_contrato_banco, 
                                     t_contrato_entidadesss, t_contrato_salario,
                                     t_contrato_deducibles)
from gestionContratos.forms import (t_contratoform, t_contrato_banco_form,
                                    t_contrato_entidadesss_form, t_contrato_salario_form,
                                    t_contrato_deducible_form)


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
        pk = self.request.POST.get('pk')
        if pk:
            contrato = t_contrato.objects.get(pk=pk)
            for field, value in form.cleaned_data.items():
                setattr(contrato, field, value)
            contrato.save()
            messages.success(self.request, 'Contrato actualizado correctamente')
        else:
            form.instance.empresa_id = self.request.session.get('empresa_id')
            form.instance.date_created = datetime.now()
            form.instance.user_creator = self.request.user
            messages.success(self.request, 'Registro creado correctamente')
            return super().form_valid(form)
        
        return redirect(self.success_url)

    def form_invalid(self, form):
        print(form.errors)
        messages.error(self.request, 'Validar campos del formulario')
        return super().form_invalid(form)

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
        pk = self.request.POST.get('pk')
        if pk:
            contratoban = t_contrato_banco.objects.get(pk=pk)
            for field, value in form.cleaned_data.items():
                setattr(contratoban, field, value)
            contratoban.save()
            messages.success(self.request, 'Contrato banco actualizado correctamente')
        else:
            form.instance.contrato_id = self.kwargs['contrato_id']
            form.instance.date_created = datetime.now()
            form.instance.user_creator = self.request.user
            messages.success(self.request, 'Registro creado correctamente')
            return super().form_valid(form)
        return redirect(self.get_success_url())
    
    def form_invalid(self, form):
        print(form.errors)
        messages.error(self.request, 'Validar campos del formulario')
        return super().form_invalid(form)
    
    def get_success_url(self):
        return reverse(
            'contrato_banco',
            kwargs={'contrato_id': self.kwargs['contrato_id']}
        )


class t_contrato_bancoDeleteView(LoginRequiredMixin,DeleteView):
    model = t_contrato_banco
    login_url = 'accounts/login'

    def get_success_url(self):
        return reverse_lazy(
            'contrato_banco',
            kwargs={'contrato_id': self.object.contrato_id}
        )
    def post(self, request, *args, **kwargs):
        messages.success(request, 'Registro eliminado correctamente')
        return super().post(request, *args, **kwargs)


class t_contrato_entidadCreateView(LoginRequiredMixin,CreateView):
    model = t_contrato_entidadesss
    form_class = t_contrato_entidadesss_form
    template_name = 'contrato_entidades_ss.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        contrato = get_object_or_404(t_contrato,pk=self.kwargs['contrato_id'])

        context['contrato'] = contrato
        context['registros'] = t_contrato_entidadesss.objects.filter(contrato=contrato)
        
        return context
     
    def form_valid(self, form):
        pk = self.request.POST.get('pk')
        if pk:
            contratoent = t_contrato_entidadesss.objects.get(pk=pk)
            for field, value in form.cleaned_data.items():
                setattr(contratoent, field, value)
            contratoent.save()
            messages.success(self.request, 'Contrato entidad actualizada correctamente')
        else:
            form.instance.contrato_id = self.kwargs['contrato_id']
            form.instance.date_created = datetime.now()
            form.instance.user_creator = self.request.user
            messages.success(self.request, 'Registro creado correctamente')
            return super().form_valid(form)
        return redirect(self.get_success_url())
    
    def form_invalid(self, form):
        print(form.errors)
        messages.error(self.request, 'Validar campos del formulario')
        return super().form_invalid(form)
    
    def get_success_url(self):
        return reverse(
            'contrato_entidad_ss',
            kwargs={'contrato_id': self.kwargs['contrato_id']}
        )


class t_contrato_entidadDeleteView(LoginRequiredMixin,DeleteView):
    model = t_contrato_entidadesss
    login_url = 'accounts/login'

    def get_success_url(self):
        return reverse_lazy(
            'contrato_entidad_ss',
            kwargs={'contrato_id': self.object.contrato_id}
        )
    def post(self, request, *args, **kwargs):
        messages.success(request, 'Registro eliminado correctamente')
        return super().post(request, *args, **kwargs)


class t_contrato_salarioCreateView(LoginRequiredMixin,CreateView):
    model = t_contrato_salario
    form_class = t_contrato_salario_form
    template_name = 'contrato_salario.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        contrato = get_object_or_404(t_contrato,pk=self.kwargs['contrato_id'])

        context['contrato'] = contrato
        context['registros'] = t_contrato_salario.objects.filter(contrato=contrato)
        
        return context
     
    def form_valid(self, form):
        pk = self.request.POST.get('pk')
        if pk:
            contratosal = t_contrato_salario.objects.get(pk=pk)
            for field, value in form.cleaned_data.items():
                setattr(contratosal, field, value)
            contratosal.save()
            messages.success(self.request, 'Salario contrato actualizado correctamente')
        else:
            form.instance.contrato_id = self.kwargs['contrato_id']
            form.instance.date_created = datetime.now()
            form.instance.user_creator = self.request.user
            messages.success(self.request, 'Registro creado correctamente')
            return super().form_valid(form)
        return redirect(self.get_success_url())
    
    def form_invalid(self, form):
        print(form.errors)
        messages.error(self.request, 'Validar campos del formulario')
        return super().form_invalid(form)
    
    def get_success_url(self):
        return reverse(
            'contrato_salario',
            kwargs={'contrato_id': self.kwargs['contrato_id']}
        )


class t_contrato_salarioDeleteView(LoginRequiredMixin,DeleteView):
    model = t_contrato_salario
    login_url = 'accounts/login'

    def get_success_url(self):
        return reverse_lazy(
            'contrato_salario',
            kwargs={'contrato_id': self.object.contrato_id}
        )
    def post(self, request, *args, **kwargs):
        messages.success(request, 'Registro eliminado correctamente')
        return super().post(request, *args, **kwargs)


class t_contrato_deducibleCreateView(LoginRequiredMixin,CreateView):
    model = t_contrato_deducibles
    form_class = t_contrato_deducible_form
    template_name = 'contrato_deducible.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        contrato = get_object_or_404(t_contrato,pk=self.kwargs['contrato_id'])

        context['contrato'] = contrato
        context['registros'] = t_contrato_deducibles.objects.filter(contrato=contrato)
        
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
            'contrato_deducible',
            kwargs={'contrato_id': self.kwargs['contrato_id']}
        )


class t_contrato_deducibleDeleteView(LoginRequiredMixin,DeleteView):
    model = t_contrato_deducibles
    login_url = 'accounts/login'

    def get_success_url(self):
        return reverse_lazy(
            'contrato_deducible',
            kwargs={'contrato_id': self.object.contrato_id}
        )
    def post(self, request, *args, **kwargs):
        messages.success(request, 'Registro eliminado correctamente')
        return super().post(request, *args, **kwargs)
