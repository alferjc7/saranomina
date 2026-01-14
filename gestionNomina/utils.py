import calendar
from datetime import date
from gestionNomina.models import t_periodo_nomina

def crear_periodos(ejecucion_automatica ,empresa, tipo_nomina, anio, mes, periodo, fecha_inicio, fecha_fin):
    if ejecucion_automatica:
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
                    estado = True )
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
                    fecha_fin=date(anio, mes, 15),
                    estado = True)
                p1.save()

                p2 = t_periodo_nomina(
                    empresa=empresa,
                    tipo_nomina=tipo_nomina,
                    anio=anio,
                    mes=mes,
                    periodo=2,
                    fecha_inicio=date(anio, mes, 16),
                    fecha_fin=date(anio, mes, ultimo_dia),
                    estado = True)
                p2.save()
        elif tipo_nomina.codigo == 'LI' or tipo_nomina.codigo == 'RL' or tipo_nomina.codigo == 'AD' or tipo_nomina.codigo == 'PR':       
            raise ValueError("Este tipo no esta parametrizado para generacion automatica.")    
    elif ejecucion_automatica != True :
        print("AUTO:", ejecucion_automatica)
        periodo = t_periodo_nomina(
                empresa=empresa,
                tipo_nomina=tipo_nomina,
                anio=anio,
                mes=mes,
                periodo=periodo,
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin,
                estado = True
                )
        periodo.save()



