from datetime import datetime
from django import forms
from django.shortcuts import redirect, render
from django.http import HttpResponse
from gestionIdentificacion.models import t_tipo_ide, t_identificacion, t_beneficiario
from gestionIdentificacion.forms import tipo_ide_form, identificacion_form, t_beneficiario_form
from django.views.generic import CreateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.messages import get_messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout


# Create your views here.
@login_required
def tipos_ide(request):
    registros = t_tipo_ide.objects.all().order_by('-id')[:10]
    form = tipo_ide_form()
    if request.method == 'POST':
        accion = request.POST.get('accion')
        pk_edit = request.POST.get('edit_id')
        pk_elim = request.POST.get('elim_id')

        if accion == "guardar":
            if pk_edit:
                obj = t_tipo_ide.objects.get(pk=pk_edit)
                form = tipo_ide_form(request.POST, instance=obj)
            else:
                form = tipo_ide_form(request.POST)

            if form.is_valid():
                obj = form.save(commit=False)
                nombre_usuario = request.user.username
                obj.user_creator = nombre_usuario
                obj.date_created = datetime.now()
                obj.save()
                messages.success(request, 'Registro guardado correctamente')
                return redirect('tipos_ide')

        elif accion == 'editar':
            obj = t_tipo_ide.objects.get(pk=pk_edit)
            form = tipo_ide_form(instance=obj)
        elif accion == 'eliminar' and pk_elim:
            obj = t_tipo_ide.objects.get(pk=pk_elim)
            obj.delete()
            messages.success(request, 'Registro eliminado correctamente')
            return redirect('tipos_ide')


    return render(request, "tipos_ide.html", {"form": form, "registros": registros})

@login_required
def identificaciones(request):
    form = identificacion_form()
    registros = t_identificacion.objects.all().order_by('-id')[:10]
    
    if request.method == 'POST' :
        pk_edit = request.POST.get('edit_id')
        pk_elim = request.POST.get('elim_id')
        accion = request.POST.get('accion')

        if accion == "guardar":             
            print("aqui 2",pk_edit)
            form = identificacion_form(request.POST)
            #print("tipo ide ",form.data)
            if pk_edit:
                obj = t_identificacion.objects.get(pk=pk_edit)
                form = identificacion_form(request.POST, instance=obj)
            else:
                obj = form.save(commit=False)
            if form.is_valid():
                obj.save()
                messages.success(request, 'Registro guardado correctamente')
                return redirect('identificaciones')
            else: 
                print("Error en el formulario",form.errors)
        elif accion == "editar":
            print("aqui")
            obj = t_identificacion.objects.get(pk=pk_edit)
            form = identificacion_form(instance=obj)
        elif accion =='eliminar':
            obj = t_identificacion.objects.get(pk=pk_elim)
            obj.delete()
            messages.success(request, 'Registro eliminado correctamente')
            return redirect('identificaciones')
        


    return render(request, "identificaciones.html", {"form": form,"registros":registros})

class BeneficiarioCreateView(LoginRequiredMixin, CreateView):
    model = t_beneficiario
    form_class = t_beneficiario_form
    template_name = 'beneficiarios.html'
    context_object_name = 'beneficiarios'
    success_url = reverse_lazy('beneficiarios')
    login_url = '/accounts/login/'           # opcional
    redirect_field_name = 'next'  # opcional
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Hacer que el campo iden_titular no se muestre en el formulario
        form.fields['iden_titular'].widget = forms.HiddenInput()
        return form
    
    def get_initial(self):
        initial = super().get_initial()
        identificacion = self.request.GET.get('identificacion')

        if identificacion:
            try:
                # Buscar el objeto de t_identificacion que coincida
                titular = t_identificacion.objects.get(identificacion=identificacion)
                initial['iden_titular'] = titular
            except t_identificacion.DoesNotExist:
                pass  # si no existe, no prellenar nada
        return initial
  
    def form_valid(self, form):
        pk = self.request.POST.get('pk')
        if pk:
            beneficiario = t_beneficiario.objects.get(pk=pk)
            for field, value in form.cleaned_data.items():
                setattr(beneficiario, field, value)
            beneficiario.save()
            messages.success(self.request, 'Beneficiario actualizado correctamente')
        else:
            response = super().form_valid(form)
            messages.success(self.request, 'Registro creado correctamente')
        
        return redirect(self.success_url)
            
    def form_invalid(self, form):
        identificacion = self.request.GET.get('identificacion')
        storage = get_messages(self.request)
        for _ in storage:
            pass  # limpi
        if identificacion is None:
            messages.error(self.request, 'Campo identificacion no se encuentra filtrado')
        
        return super().form_invalid(form)

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        identificacion = self.request.GET.get('identificacion')
        print('Aqui')
        if identificacion:
            print('Aqui2')
            try:
                titular = t_identificacion.objects.get(identificacion=identificacion)
                beneficiarios = t_beneficiario.objects.filter(iden_titular__identificacion = identificacion)
                context['beneficiarios'] = beneficiarios
                context['nombre'] = "%s %s %s %s"%(titular.nombre,titular.segundo_nombre,titular.apellido,titular.segundo_apellido)  # OJO: atributo, no el objeto
            except t_identificacion.DoesNotExist:
                context['nombre'] = ''
        return context
    
class BeneficiarioDeleteView(LoginRequiredMixin,DeleteView):
    model = t_beneficiario
    success_url = reverse_lazy('beneficiarios')
    login_url = 'accounts/login'

    def post(self, request, *args, **kwargs):
        messages.success(request, 'Beneficiario eliminado correctamente')
        return super().post(request, *args, **kwargs)

@login_required
def inicio(request):
    return render(request,"base.html",)

def logout_view(request):
    logout(request)
    return redirect('login')

def resultado(request):
    if request.GET['prd']:
        #mensaje = "El valor buscado es %r"%request.GET['prd']
        busqueda = request.GET['prd']
        tipo_ide = t_tipo_ide.objects.filter(desc_ide__icontains = busqueda)

        return render(request,"resultado_buscar.html",{"tipo":tipo_ide, "query":busqueda})
    else:
        mensaje = "No ingreso ningun valor"
        return HttpResponse(mensaje)
