from datetime import datetime
from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, DeleteView
from gestionNomina.models import (t_periodo_nomina, t_logica_calculo, 
                                  t_acumulado_empleado, t_proceso_nomina, 
                                  t_logica_calculo_filtro, t_acumulado_empleado_def)
from gestionConceptos.models import t_concepto_empresa
from gestionNomina.utils import crear_periodos
from gestionNomina.forms import (GenerarPeriodoNominaForm, t_logica_calculoform, t_acumulaldo_empleadoform, 
                                 FiltroTipoContratoForm, FiltroTipoCotizanteForm)
from gestionClientes.models import t_empresa
from django.contrib import messages
from parametros.models import t_tipo_nomina, t_tipo_contrato, t_tipo_cotizante,ParametroDetalle
from django.http import JsonResponse
from django.db import connection, transaction
from django.utils import timezone
from django.db.models import OuterRef, Subquery, IntegerField
from django.db.models.functions import Coalesce
from threading import Thread


def ejecutar_nomina_background(proceso_id, periodo):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SET client_min_messages TO NOTICE;")
            cursor.execute(
                """
                CALL prc_procesar_nomina(
                    %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
                """,
                [
                    periodo.empresa_id,
                    periodo.tipo_nomina_id,
                    periodo.anio,
                    periodo.mes,
                    periodo.periodo,
                    periodo.fecha_inicio,
                    periodo.fecha_fin,
                    proceso_id,
                    periodo.id
                ]
            )

        t_proceso_nomina.objects.filter(id=proceso_id).update(
            estado="F",
            progreso=100,
            mensaje_error="SIN ERRORES",
            date_finished=timezone.now()
        )

    except Exception as e:
        t_proceso_nomina.objects.filter(id=proceso_id).update(
            estado="X",
            mensaje_error=str(e),
            date_finished=timezone.now()
        )


def ejecutar_nomina_cierre(proceso_id, periodo):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SET client_min_messages TO NOTICE;")
            cursor.execute(
                """
                CALL prc_cierre_nomina(
                    %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
                """,
                [
                    periodo.empresa_id,
                    periodo.tipo_nomina_id,
                    periodo.anio,
                    periodo.mes,
                    periodo.periodo,
                    periodo.fecha_inicio,
                    periodo.fecha_fin,
                    proceso_id,
                    periodo.id
                ]
            )

        t_proceso_nomina.objects.filter(id=proceso_id).update(
            estado="C",
            progreso=100,
            mensaje_error="CIERRE FINALIZADO",
            date_finished=timezone.now()
        )

    except Exception as e:
        t_proceso_nomina.objects.filter(id=proceso_id).update(
            estado="X",
            mensaje_error=str(e),
            date_finished=timezone.now()
        )

def procedimientos_por_concepto(request):
    concepto_id = request.GET.get('concepto_id')
    modulo_id = request.GET.get('modulo')
    modulo = ParametroDetalle.objects.get(id = modulo_id).codigo 
    print(modulo)

    if not concepto_id:
        return JsonResponse([], safe=False)

    concepto = t_concepto_empresa.objects.get(id=concepto_id)
    codigo = concepto.cod_concepto.cod_concepto  # ej: 1000
    print(codigo)

    like_pattern = f'prc_{codigo}_%'

    if modulo == 'NOV':
        like_pattern = 'prc_nov_%'


    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT upper(routine_name)
            FROM information_schema.routines
            WHERE routine_type = 'PROCEDURE'
              AND routine_name LIKE %s
            ORDER BY routine_name
        """, [like_pattern])

        procedimientos = [row[0] for row in cursor.fetchall()]

    return JsonResponse(procedimientos, safe=False)

def progreso_nomina_ajax(request, periodo_id):
    proceso = (
        t_proceso_nomina.objects
        .filter(periodo_nomina_id=periodo_id)
        .order_by("-id")
        .first()
    )

    if not proceso:
        return JsonResponse({
            "progreso": 0,
            "estado": None
        })

    return JsonResponse({
        "progreso": proceso.progreso,
        "estado": proceso.estado
    })

def conceptos_por_empresa(request):
    empresa_id = request.session.get('empresa_id')

    conceptos = t_concepto_empresa.objects.filter(
        empresa_id=empresa_id
    ).values('id', 'cod_concepto__cod_concepto','desc_concepto_emp')

    return JsonResponse(list(conceptos), safe=False)

class periodo_nominaListView(LoginRequiredMixin,ListView):
    model = t_periodo_nomina
    template_name = 'periodo_nomina.html'
    context_object_name = 'periodo_nomina'

    def get_queryset(self):
        qs = t_periodo_nomina.objects.filter(
            empresa=self.request.session.get('empresa_id')
        )

        tipo = self.request.GET.get('tipo')
        anio = self.request.GET.get('anio')
        mes = self.request.GET.get('mes')

        if tipo:
            qs = qs.filter(tipo_nomina_id=tipo)

        if anio:
            qs = qs.filter(anio=anio)

        if mes:
            qs = qs.filter(mes=mes)

        return qs
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tipos_nomina'] = t_tipo_nomina.objects.all()
        context['tipo_seleccionado'] = self.request.GET.get('tipo')
        context['form'] = GenerarPeriodoNominaForm()
        return context

    def post(self, request, *args, **kwargs):
        form = GenerarPeriodoNominaForm(request.POST)

        if form.is_valid():
            ejecucion_automatica = form.cleaned_data['ejecucion_automatica']
            empresa = t_empresa.objects.get(id=request.session.get('empresa_id'))
            tipo_nomina = form.cleaned_data['tipo_nomina']
            anio = form.cleaned_data['anio']
            mes = form.cleaned_data['mes']
            periodo = form.cleaned_data['periodo']
            fecha_inicio = form.cleaned_data['fecha_inicio']
            fecha_fin = form.cleaned_data['fecha_fin']

            existe = False
            validar_adicionales = False
            # Evitar duplicados
            if tipo_nomina.asigna_contrato == False :
                if all([tipo_nomina, anio, mes, periodo, fecha_inicio, fecha_fin]):
                    existe = t_periodo_nomina.objects.filter(
                        empresa = empresa,
                        tipo_nomina = tipo_nomina,
                        anio = anio,
                        mes = mes,
                        periodo  = periodo,
                        fecha_inicio = fecha_inicio,
                        fecha_fin = fecha_fin
                    ).exists()
                
                else:
                    validar_adicionales = True
                    messages.error(request, "Para este tipo de Nomina se deben diligenciar todos los campos.")    
            else:
                existe = t_periodo_nomina.objects.filter(
                    empresa = empresa,
                    tipo_nomina = tipo_nomina,
                    anio = anio
                ).exists()

            if existe:
                messages.error(request, "Ya existen períodos para ese año y tipo de nómina.")
            else:
                try:
                    crear_periodos(
                        ejecucion_automatica,
                        empresa,
                        tipo_nomina,
                        anio,
                        mes,
                        periodo,
                        fecha_inicio,
                        fecha_fin
                    )
                    if validar_adicionales == False:
                        messages.success(request, "Períodos creados correctamente.")
                except ValueError as e:
                    messages.error(request, str(e))
        else:
            print(form.errors)

        return redirect('periodo_nomina')
    
class periodo_nominaDeleteView(LoginRequiredMixin,DeleteView):
    model = t_periodo_nomina
    success_url = reverse_lazy('periodo_nomina')
    login_url = 'accounts/login'

    def post(self, request, *args, **kwargs):
        messages.success(request, 'Periodo eliminado correctamente')
        return super().post(request, *args, **kwargs)

class logica_calculoCreateView(LoginRequiredMixin,CreateView):
    model = t_logica_calculo
    form_class = t_logica_calculoform
    template_name = 'logica_calculo.html'
    context_object_name = 'logica_calculo'
    success_url = reverse_lazy('logica_calculo')
    login_url = '/accounts/login/'           # opcional
    redirect_field_name = 'next'  # opcional

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        registros = t_logica_calculo.objects.filter(empresa_id = self.request.session.get('empresa_id')).order_by('orden','concepto__cod_concepto__cod_concepto')
        context['registros'] = registros
        return context
    
    def form_valid(self, form):
        pk = self.request.POST.get('pk')
        if pk:
            logica = t_logica_calculo.objects.get(pk=pk)
            for field, value in form.cleaned_data.items():
                setattr(logica, field, value)
            logica.save()
            messages.success(self.request, 'Logica de calculo actualizada correctamente')
        else:
            form.instance.empresa_id = self.request.session.get('empresa_id')
            form.instance.date_created = datetime.now()
            form.instance.user_creator = self.request.user
            response = super().form_valid(form)
            messages.success(self.request, 'Registro creado correctamente')
        return redirect(self.success_url)

    def form_invalid(self, form):
        messages.error(self.request, 'Validar campos del formulario')
        return super().form_invalid(form)

class logica_calculoDeleteView(LoginRequiredMixin,DeleteView):
    model = t_logica_calculo
    success_url = reverse_lazy('logica_calculo')
    login_url = 'accounts/login'

    def post(self, request, *args, **kwargs):
        messages.success(request, 'Logica eliminada correctamente')
        return super().post(request, *args, **kwargs)

class AcumuladosListView(LoginRequiredMixin,ListView):
    model = t_acumulado_empleado
    template_name = 'acumulados.html'
    context_object_name = 'acumulados'

    def get_queryset(self):
        empresa_id = self.request.session.get('empresa_id')

        contrato = self.request.GET.get('contrato')
        anio = self.request.GET.get('anio')
        mes = self.request.GET.get('mes')
        periodo = self.request.GET.get('periodo')
        concepto = self.request.GET.get('concepto')

        # 👉 Si no hay ningún filtro, NO mostrar nada
        if not any([contrato, anio, mes, periodo, concepto]):
            return t_acumulado_empleado.objects.none()

        qs = t_acumulado_empleado.objects.filter(
            contrato__empresa_id=empresa_id
        )

        if contrato:
            qs = qs.filter(contrato__cod_contrato__icontains=contrato)

        if anio:
            qs = qs.filter(anio=anio)

        if mes:
            qs = qs.filter(mes=mes)

        if periodo:
            qs = qs.filter(periodo_nomina__codigo=periodo)

        if concepto:
            qs = qs.filter(concepto__cod_concepto=concepto)

        return qs


class AcumuladosDefListView(LoginRequiredMixin,ListView):
    model = t_acumulado_empleado_def
    template_name = 'acumulados_hist.html'
    context_object_name = 'acumulados_hist'

    def get_queryset(self):
        empresa_id = self.request.session.get('empresa_id')

        contrato = self.request.GET.get('contrato')
        anio = self.request.GET.get('anio')
        mes = self.request.GET.get('mes')
        periodo = self.request.GET.get('periodo')
        concepto = self.request.GET.get('concepto')

        if not any([contrato, anio, mes, periodo, concepto]):
            return t_acumulado_empleado_def.objects.none()

        qs = t_acumulado_empleado_def.objects.filter(
            contrato__empresa_id=empresa_id
        )

        if contrato:
            qs = qs.filter(contrato__cod_contrato__icontains=contrato)

        if anio:
            qs = qs.filter(anio=anio)

        if mes:
            qs = qs.filter(mes=mes)

        if periodo:
            qs = qs.filter(periodo_nomina__codigo=periodo)

        if concepto:
            qs = qs.filter(concepto__cod_concepto=concepto)

        return qs
    
class ProcesamientoNominaView(View):

    template_name = "procesamiento_nomina.html"

    def get(self, request):
        empresa_id = self.request.session.get('empresa_id')
        
        anio = request.GET.get('anio')
        mes = request.GET.get('mes')
        periodo = request.GET.get('periodo')
        codigo = request.GET.get('codigo')

        if not any([anio, mes, periodo, codigo]):
            periodos = t_periodo_nomina.objects.none()
        else:
            ultimo_proceso = (
                t_proceso_nomina.objects
                .filter(periodo_nomina=OuterRef('pk'))
                .order_by('-id')
            )

            periodos = (
                t_periodo_nomina.objects
                .filter(empresa_id=empresa_id)
                .annotate(
                    progreso=Coalesce(
                        Subquery(
                            ultimo_proceso.values('progreso')[:1],
                            output_field=IntegerField()
                        ),
                        0
                    ),
                    estado_proceso=Subquery(
                        ultimo_proceso.values('estado')[:1]
                    )
                )
                .order_by("anio", "mes", "periodo")
            )

            if anio:
                periodos = periodos.filter(anio=anio)

            if mes:
                periodos = periodos.filter(mes=mes)

            if periodo:
                periodos = periodos.filter(periodo=periodo)

            if codigo:
                periodos = periodos.filter(codigo__icontains=codigo)
     
        return render(request, self.template_name, {
        "periodos": periodos,
        })

    @transaction.non_atomic_requests
    def post(self, request):

        periodos_ids = request.POST.getlist("periodos")
        accion = request.POST.get("accion")
        print(accion)

        if not periodos_ids:
            return JsonResponse({"error": "No periodos"}, status=400)

        procesos = []

        for periodo_id in periodos_ids:
            periodo = t_periodo_nomina.objects.select_related(
                "empresa", "tipo_nomina"
            ).get(id=periodo_id)

            if accion == 'procesar':
                if periodo.estado:
                    proceso = t_proceso_nomina.objects.create(
                        periodo_nomina=periodo,
                        estado="P",
                        progreso=0,
                        user_creator=request.user.username
                    )

                    procesos.append(proceso.id)

                    Thread(
                        target=ejecutar_nomina_background,
                        args=(proceso.id, periodo),
                        daemon=True
                    ).start()
                else:
                    return JsonResponse({"error": "No se puede procesar un periodo cerrado"}, status=400)

            elif accion == 'cerrar':
                if periodo.estado:
                    proceso = t_proceso_nomina.objects.create(
                        periodo_nomina=periodo,
                        estado="P",
                        progreso=0,
                        user_creator=request.user.username
                    )

                    procesos.append(proceso.id)

                    Thread(
                        target=ejecutar_nomina_cierre,
                        args=(proceso.id, periodo),
                        daemon=True
                    ).start()
                else:
                    return JsonResponse({"error": "No se puede procesar un periodo cerrado"}, status=400)

            
        return JsonResponse({
            "ok": True,
            "procesos": procesos
        })
                            
class procesamiento_detalleListView(LoginRequiredMixin,ListView):
    model = t_proceso_nomina
    template_name = 'procesamiento_detalle.html'
    context_object_name = 'procesos'

    def get_queryset(self):
        id = self.kwargs['id']
        
        qs = t_proceso_nomina.objects.filter(periodo_nomina_id = id).order_by('date_created')

        return qs


class LogicaFiltrosView(View):

    template_name = "filtros.html"

    def get(self, request, id):
        
        tipo_contratos =   t_logica_calculo_filtro.objects.filter(logica_calculo_id = id, campo = 'tipo_contrato_id')
        tipos  = t_tipo_contrato.objects.all()
        tipos_map = {c.id: c.contrato for c in tipos}
        tipo_cotizantes =   t_logica_calculo_filtro.objects.filter(logica_calculo_id = id, campo = 'tipo_cotizante_id')
        tipos_c =  t_tipo_cotizante.objects.all()
        tipos_c_map = {c.id: c.descripcion for c in tipos_c}
        
        context = {
            "form_tipo_contrato": FiltroTipoContratoForm(prefix="contrato"),
            "tipo_contrato": tipo_contratos,
            "tipos_map": tipos_map,
            "form_tipo_cotizante": FiltroTipoCotizanteForm(prefix="cotizante"),
            "tipo_cotizante": tipo_cotizantes,
            "tipos_c_map": tipos_c_map,


        }
        return render(request, self.template_name, context)

    def post(self, request, id):

        if 'contrato-submit' in request.POST:
            form = FiltroTipoContratoForm(
                request.POST,
                prefix="contrato"
            )
            campo = "tipo_contrato_id"
        elif 'cotizante-submit' in request.POST:
            form = FiltroTipoCotizanteForm(
                request.POST,
                prefix="cotizante"
            )
            campo = "tipo_cotizante_id"
        else:
            return redirect(request.path)

        if form.is_valid():
            filtro = form.save(commit=False)
            filtro.campo = campo
            filtro.logica_calculo_id = id
            contrato = form.cleaned_data['valor']
            filtro.valor = str(contrato.id)
            filtro.user_creator = request.user.username
            filtro.save()
        
        print(form.errors)


        return redirect(request.path)
    

class LogicaFiltrosDeleteView(LoginRequiredMixin,DeleteView):
    model = t_logica_calculo_filtro
    login_url = 'accounts/login'

    def get_success_url(self):
        return reverse_lazy(
            'logica_filtros',
            kwargs={'id': self.object.logica_calculo_id}
        )
    def post(self, request, *args, **kwargs):
        messages.success(request, 'Registro eliminado correctamente')
        return super().post(request, *args, **kwargs)
