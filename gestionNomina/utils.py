import calendar
from datetime import date
from gestionNomina.models import t_periodo_nomina

def crear_periodos(empresa, tipo_nomina, anio, mes, periodo):
    if tipo_nomina.codigo == 'ME': 
        for mes in range(1, 13):
            ultimo_dia = calendar.monthrange(anio, mes)[1]

            periodo = t_periodo_nomina(
                empresa=empresa,
                tipo_nomina=tipo_nomina,
                anio=anio,
                mes=mes,
                periodo=1,
                fecha_inicio=date(anio, mes, 1),
                fecha_fin=date(anio, mes, ultimo_dia),
            )
            periodo.save()
        
    elif tipo_nomina.codigo == 'QI':  # QUINCENAL
        for mes in range(1, 13):
            ultimo_dia = calendar.monthrange(anio, mes)[1]

            p1 = t_periodo_nomina(
                empresa=empresa,
                tipo_nomina=tipo_nomina,
                anio=anio,
                mes=mes,
                periodo=1,
                fecha_inicio=date(anio, mes, 1),
                fecha_fin=date(anio, mes, 15)
            )
            p1.save()

            p2 = t_periodo_nomina(
                empresa=empresa,
                tipo_nomina=tipo_nomina,
                anio=anio,
                mes=mes,
                periodo=2,
                fecha_inicio=date(anio, mes, 16),
                fecha_fin=date(anio, mes, ultimo_dia)
            )
            p2.save()
        
