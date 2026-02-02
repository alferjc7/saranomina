from urllib.parse import urlencode
from django.db import connection, transaction
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from gestionVacaciones.models import t_ciclos_vacaciones, t_novedad_vac
from gestionContratos.models import t_contrato
from gestionVacaciones.forms import GenerarVacacionesForm
from django.contrib import messages

# Create your views here.

def procesar_vacaciones_db(
    contrato_id,
    tipo,
    fecha_inicio,
    fecha_fin,
    dias,
    fecha_pago
):
    with transaction.atomic():
        with connection.cursor() as cursor:

            # 1️⃣ Inicializamos variables de salida
            cursor.execute("""
                DO $$
                DECLARE
                    v_ok BOOLEAN;
                    v_sin_ciclos BOOLEAN;
                    v_dias_insuf BOOLEAN;
                BEGIN
                    CALL prc_procesar_vacaciones(
                        %s, %s, %s, %s, %s, %s,
                        v_ok,
                        v_sin_ciclos,
                        v_dias_insuf
                    );

                    CREATE TEMP TABLE tmp_resultado_vacaciones (
                        ok BOOLEAN,
                        sin_ciclos BOOLEAN,
                        dias_insuficientes BOOLEAN
                    ) ON COMMIT DROP;

                    INSERT INTO tmp_resultado_vacaciones
                    VALUES (v_ok, v_sin_ciclos, v_dias_insuf);
                END $$;
            """, [
                contrato_id,
                tipo,
                fecha_inicio,
                fecha_fin,
                dias,
                fecha_pago
            ])

            # 2️⃣ Leemos el resultado
            cursor.execute("""
                SELECT ok, sin_ciclos, dias_insuficientes
                FROM tmp_resultado_vacaciones
            """)

            row = cursor.fetchone()

    return {
        "ok": row[0],
        "sin_ciclos": row[1],
        "dias_insuficientes": row[2],
    }

def calcular_fecha_fin_vacaciones(request):
    contrato_id = request.GET.get('contrato')
    fecha_inicio = request.GET.get('fecha_inicio')
    dias = request.GET.get('dias')

    if not contrato_id or not fecha_inicio or not dias:
        return JsonResponse({'fecha_fin': None})

    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT fn_calcular_fecha_fin_habil(%s, %s, %s)
            """,
            [contrato_id, fecha_inicio, dias]
        )
        fecha_fin = cursor.fetchone()[0]
    print("aqui")
    print(fecha_fin)
    print(contrato_id)
    return JsonResponse({
        'fecha_fin': fecha_fin.strftime('%Y-%m-%d') if fecha_fin else None
    })

class t_ciclos_LaboralView(View):
    template_name = "vacaciones.html"

    def get(self, request):
        contrato = request.GET.get("contrato")
        registros = []
        novedades = []

        if contrato:
            registros = t_ciclos_vacaciones.objects.filter(
                contrato__id=contrato).order_by("fecha_inicio")
            novedades = t_novedad_vac.objects.filter(contrato__id = contrato)

        contratos = t_contrato.objects.filter(empresa_id = self.request.session.get('empresa_id') ,
                                              estado='A')
        
        form = GenerarVacacionesForm()

        context = {
            "ciclos": registros,
            "contratos": contratos,
            "contrato_seleccionado": contrato,
            "form": form,
            "novedades": novedades
        }

        return render(request, self.template_name, context)
    
    def post(self, request):
        accion = request.POST.get("accion")
        contrato = request.POST.get("contrato")
        print(accion) 
        form = GenerarVacacionesForm(request.POST)
        
        if accion == "validar" and form.is_valid():
             
            data = procesar_vacaciones_db(
                contrato_id = contrato,
                tipo = form.cleaned_data['tipo_vac'],
                fecha_inicio = form.cleaned_data.get('fecha_inicio'),
                fecha_fin = form.cleaned_data.get('fecha_fin'),
                dias = form.cleaned_data['dias'],
                fecha_pago = form.cleaned_data['fecha_pago']
            )

            print(form.cleaned_data.get('fecha_fin'))
            
            if data["sin_ciclos"]:
                messages.error(request, "El contrato no tiene ciclos de vacaciones disponibles.")
            elif data["dias_insuficientes"]:
                messages.error(request, "No hay días suficientes en los periodos disponibles.")
            elif data["ok"]:
                messages.success(request, "Vacaciones procesadas correctamente.")
            else:
                messages.error(request, "Ocurrió un error inesperado.")
        else:
            messages.error(request, "Formulario inválido.")
        
        base_url = reverse('vacaciones')

        if contrato:
            query_string = urlencode({'contrato': contrato})
            return redirect(f"{base_url}?{query_string}")

        return redirect(base_url)
