from datetime import datetime
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from parametros.models import (t_tipo_contrato, t_tipo_salario, 
                               t_tipo_cotizante, t_subtipo_cotizante,
                               t_banco, t_entidadesss)
from parametros.forms import (tipo_contratoform, tipo_salarioform, 
                              tipo_cotizanteform, subtipo_cotizanteform,
                              bancoform, t_entidadesssform, CargaExcelForm)
from django.views.generic import CreateView, DeleteView
from openpyxl import load_workbook
from django.http import HttpResponse
from openpyxl import Workbook


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

    
    def post(self, request, *args, **kwargs):
        # 👉 EXPORTAR EXCEL
        if 'exportar_excel' in request.POST:
            return self.exportar_excel()

        # 👉 SI VIENE EXCEL
        if 'archivo_excel' in request.FILES:
            form_excel = CargaExcelForm(request.POST, request.FILES)

            if form_excel.is_valid():
                archivo = request.FILES['archivo_excel']
                wb = load_workbook(archivo)
                ws = wb.active

                creados = 0
                omitidos = 0

                for row in ws.iter_rows(min_row=2, values_only=True):
                    banco, codigo_ach, codigo_pse, codigo_br, codigo_fintech, estado = row

                    if not codigo_ach or not codigo_br or not codigo_pse or not codigo_fintech:
                        continue

                    _, created = t_banco.objects.get_or_create(
                        codigo_ach=codigo_ach,
                        codigo_pse=codigo_pse,
                        codigo_br=codigo_br,
                        codigo_fintech=codigo_fintech,
                        defaults={
                            'banco': banco,
                            'estado': True,
                            'user_creator': request.user,
                            'date_created': datetime.now()
                        }
                    )

                    if created:
                        creados += 1
                    else:
                        omitidos += 1

                messages.success(
                    request,
                    f'Carga masiva exitosa. Nuevos: {creados}, Omitidos: {omitidos}'
                )

            return redirect(self.success_url)

        # 👉 SI NO, ES CREATE NORMAL
        return super().post(request, *args, **kwargs)

    def exportar_excel(self):
        wb = Workbook()
        ws = wb.active
        ws.title = 'Bancos'

        ws.append(['banco', 'codigo_ach', 'codigo_pse', 'codigo_br', 'codigo_fintech'])

        registros = t_banco.objects.all().order_by('-pk')

        for r in registros:
            ws.append([r.banco, r.codigo_ach, r.codigo_pse, r.codigo_br, r.codigo_fintech])

        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=bancos_ss.xlsx'

        wb.save(response)
        return response

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


class entidadesssCreateView(LoginRequiredMixin,CreateView):
    model = t_entidadesss
    form_class = t_entidadesssform
    template_name = 'entidades_ss.html'
    context_object_name = 'entidades_ss'
    success_url = reverse_lazy('entidades_ss')
    login_url = '/accounts/login/'           # opcional
    redirect_field_name = 'next'  # opcional

    def post(self, request, *args, **kwargs):
        # 👉 EXPORTAR EXCEL
        if 'exportar_excel' in request.POST:
            return self.exportar_excel()

        # 👉 SI VIENE EXCEL
        if 'archivo_excel' in request.FILES:
            form_excel = CargaExcelForm(request.POST, request.FILES)

            if form_excel.is_valid():
                archivo = request.FILES['archivo_excel']
                wb = load_workbook(archivo)
                ws = wb.active

                creados = 0
                omitidos = 0

                for row in ws.iter_rows(min_row=2, values_only=True):
                    tipo, codigo, nit, nombre = row

                    if not codigo:
                        continue

                    _, created = t_entidadesss.objects.get_or_create(
                        codigo=codigo,
                        defaults={
                            'tipo': tipo,
                            'nit': nit,
                            'nombre': nombre,
                            'user_creator': request.user,
                            'date_created': datetime.now()
                        }
                    )

                    if created:
                        creados += 1
                    else:
                        omitidos += 1

                messages.success(
                    request,
                    f'Carga masiva exitosa. Nuevos: {creados}, Omitidos: {omitidos}'
                )

            return redirect(self.success_url)

        # 👉 SI NO, ES CREATE NORMAL
        return super().post(request, *args, **kwargs)

    def exportar_excel(self):
        wb = Workbook()
        ws = wb.active
        ws.title = 'Entidades SS'

        ws.append(['Tipo', 'Código', 'NIT', 'Nombre'])

        registros = t_entidadesss.objects.all().order_by('-pk')

        for r in registros:
            ws.append([r.tipo, r.codigo, r.nit, r.nombre])

        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=entidades_ss.xlsx'

        wb.save(response)
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        registros = t_entidadesss.objects.all().order_by('-pk')[:30]
        context['registros'] = registros
        context['form_excel'] = CargaExcelForm()
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
    
class entidadesssDeleteView(LoginRequiredMixin,DeleteView):
    model = t_entidadesss
    success_url = reverse_lazy('entidades_ss')
    login_url = 'accounts/login'

    def post(self, request, *args, **kwargs):
        messages.success(request, 'Banco eliminado correctamente')
        return super().post(request, *args, **kwargs)

