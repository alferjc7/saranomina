from datetime import datetime
from django import forms
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from gestionIdentificacion.models import t_tipo_ide, t_identificacion, t_beneficiario
from gestionIdentificacion.forms import tipo_ide_form, identificacion_form, t_beneficiario_form
from django.views.generic import CreateView, DeleteView
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.messages import get_messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from django.db.models.deletion import ProtectedError



# Create your views here.
@login_required
def tipos_ide(request):
    registros = t_tipo_ide.objects.all().order_by('-id')[:10]
    
    codigo = request.GET.get('codigo')

    if codigo:
        registros = t_tipo_ide.objects.filter(cod_ide = codigo.upper())

    
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
    
    identificacion = request.GET.get('identificacion')
    
    if identificacion:
        registros = t_identificacion.objects.filter(identificacion = identificacion)


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
            try:
                obj.delete()
                messages.success(request, 'Registro eliminado correctamente')
            except ProtectedError:
                messages.error(request,'Esta identificacion ya esta asignada a un contrato!')           
            return redirect('identificaciones')
        


    return render(request, "identificaciones.html", {"form": form,"registros":registros})

class t_beneficiarioCreateView(LoginRequiredMixin,CreateView):
    model = t_beneficiario
    form_class = t_beneficiario_form
    template_name = 'beneficiarios.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        identificacion = get_object_or_404(t_identificacion,pk=self.kwargs['id'])

        context['identificacion'] = identificacion
        context['beneficiarios'] = t_beneficiario.objects.filter(iden_titular=identificacion)
        
        identificacion = self.request.GET.get('identificacion')

        if identificacion:
            context['beneficiarios']  = t_beneficiario.objects.filter(iden_titular=identificacion ,iden_beneficiario = identificacion)

        return context
     
    def form_valid(self, form):
        pk = self.request.POST.get('pk')
        print(pk)
        if pk:
            beneficiarios= t_beneficiario.objects.get(pk=pk)
            for field, value in form.cleaned_data.items():
                setattr(beneficiarios, field, value)
            beneficiarios.save()
            messages.success(self.request, 'Beneficiario actualizado correctamente')
        else:
            identificacion = get_object_or_404(t_identificacion,pk=self.kwargs['id'])    
            form.instance.iden_titular = identificacion
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
            'tbeneficiario',
            kwargs={'id': self.kwargs['id']}
        )
    
class t_beneficiarioDeleteView(LoginRequiredMixin,DeleteView):
    model = t_beneficiario
    login_url = 'accounts/login'

    def get_success_url(self):
        return reverse_lazy(
            'tbeneficiario',
            kwargs={'id': self.object.iden_titular.id}
        )
    def post(self, request, *args, **kwargs):
        messages.success(request, 'Registro eliminado correctamente')
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
