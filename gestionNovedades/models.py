from django.db import models
from gestionContratos.models import t_contrato
from gestionConceptos.models import t_concepto_empresa
from gestionNomina.models import t_periodo_nomina, t_acumulado_empleado_def
from parametros.models import t_tipo_nomina

# Create your models here.
class t_novedad_temporal(models.Model):
    contrato = models.ForeignKey(
        t_contrato,
        on_delete=models.CASCADE,
        verbose_name="Contrato"
    )
    concepto = models.ForeignKey(
        t_concepto_empresa,
        on_delete=models.CASCADE,
        verbose_name="Concepto"
    )
    anio = models.IntegerField(verbose_name="Año")
    mes = models.IntegerField(verbose_name="Mes")
    periodo = models.IntegerField(verbose_name="Periodo")
    tipo_nomina = models.ForeignKey(
        t_tipo_nomina,
        on_delete=models.CASCADE,
        verbose_name="Tipo de nómina"
    )
    unidad = models.DecimalField(
        max_digits=10,
        decimal_places=0,
        default=0,
        verbose_name="Unidad"
    )

    base = models.DecimalField(
        max_digits=15,
        decimal_places=0,
        default=0,
        verbose_name="Base",
        blank = True
    )

    valor = models.DecimalField(
        max_digits=15,
        decimal_places=0,
        default=0,
        verbose_name="Valor",
        blank = True
    )

    periodo_nomina = models.ForeignKey(
        t_periodo_nomina,
        on_delete=models.CASCADE,
        verbose_name="Periodo Nomina"
    )
    
    fecha_novedad = models.DateField(
        verbose_name="Fecha novedad",
        blank=True,
        null=True
    )
    estado = models.BooleanField(default=True, verbose_name="Estado")
    user_creator = models.CharField(max_length=50,blank= True, null= True)
    date_created = models.DateField(blank= True, null= True)


class t_novedad_fija(models.Model):
    contrato = models.ForeignKey(
        t_contrato,
        on_delete=models.CASCADE,
        verbose_name="Contrato"
    )
    concepto = models.ForeignKey(
        t_concepto_empresa,
        on_delete=models.CASCADE,
        verbose_name="Concepto"
    )
    tipo_nomina = models.ForeignKey(
        t_tipo_nomina,
        on_delete=models.CASCADE,
        verbose_name="Tipo de nómina"
    )
    unidad = models.DecimalField(
        max_digits=10,
        decimal_places=0,
        default=0,
        verbose_name="Unidad"
    )
    base = models.DecimalField(
        max_digits=15,
        decimal_places=0,
        default=0,
        verbose_name="Base",
        blank = True
    )
    valor = models.DecimalField(
        max_digits=15,
        decimal_places=0,
        default=0,
        verbose_name="Valor"
    )
    fecha_inicio = models.DateField(
        verbose_name="Fecha inicio"
    )
    fecha_fin = models.DateField(
        verbose_name="Fecha fin"
    )
    estado = models.BooleanField(default=True, verbose_name="Estado")
    user_creator = models.CharField(max_length=50,blank= True, null= True)
    date_created = models.DateField(blank= True, null= True)

class t_novedad_fija_det(models.Model):
    
    novedad = models.ForeignKey(
        t_novedad_fija,
        on_delete=models.CASCADE,
        verbose_name="Novedad"
    )

    acumulado = models.ForeignKey(
        t_acumulado_empleado_def,
        on_delete=models.CASCADE,
        verbose_name="Acumulado"
    )

    contrato = models.ForeignKey(
        t_contrato,
        on_delete=models.CASCADE,
        verbose_name="Contrato"
    )
    concepto = models.ForeignKey(
        t_concepto_empresa,
        on_delete=models.CASCADE,
        verbose_name="Concepto"
    )
    anio = models.IntegerField(verbose_name="Año")
    mes = models.IntegerField(verbose_name="Mes")
    periodo = models.IntegerField(verbose_name="Periodo")
    tipo_nomina = models.ForeignKey(
        t_tipo_nomina,
        on_delete=models.CASCADE,
        verbose_name="Tipo de nómina"
    )
    unidad = models.DecimalField(
        max_digits=10,
        decimal_places=0,
        default=0,
        verbose_name="Unidad"
    )

    base = models.DecimalField(
        max_digits=15,
        decimal_places=0,
        default=0,
        verbose_name="Base",
        blank = True
    )

    valor = models.DecimalField(
        max_digits=15,
        decimal_places=0,
        default=0,
        verbose_name="Valor",
        blank = True
    )

    periodo_nomina = models.ForeignKey(
        t_periodo_nomina,
        on_delete=models.CASCADE,
        verbose_name="Periodo Nomina"
    )
    
    user_creator = models.CharField(max_length=50,blank= True, null= True)
    date_created = models.DateField(blank= True, null= True)
