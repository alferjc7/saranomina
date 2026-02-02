from django.db import models
from gestionContratos.models import t_contrato
from gestionConceptos.models import t_concepto_empresa


class t_ciclos_vacaciones(models.Model):
    contrato = models.ForeignKey(
        t_contrato,
        on_delete=models.CASCADE,
        verbose_name="Contrato"
    )
    fecha_inicio = models.DateField(
        verbose_name="Fecha inicio del ciclo"
    )
    fecha_fin = models.DateField(
        verbose_name="Fecha fin del ciclo"
    )
    dias = models.IntegerField(
        verbose_name="Días causados",
        help_text="Días de vacaciones causados en el ciclo"
    )

    class Meta:
        verbose_name = "Ciclo de vacaciones"
        ordering = ['contrato', 'fecha_inicio']
        unique_together = ('contrato', 'fecha_inicio', 'fecha_fin')

    def __str__(self):
        return f"{self.contrato} | {self.fecha_inicio} - {self.fecha_fin} ({self.dias} días)"
    

class t_novedad_vac(models.Model):

    TIPO_VACACIONES = (
        ('D', 'DISFRUTADAS'),
        ('C', 'COMPENSADAS'),
    )
    
    tipo = models.CharField(
        max_length=1,
        choices= TIPO_VACACIONES,
        verbose_name="Tipo de vacaciones"
    )

    ciclo = models.ForeignKey(
        t_ciclos_vacaciones,
        on_delete=models.PROTECT,
        verbose_name="Ciclo de vacaciones"
    )
    contrato = models.ForeignKey(
        t_contrato,
        on_delete=models.CASCADE,
        verbose_name="Contrato"
    )
    fecha_inicio = models.DateField(
        verbose_name="Fecha inicio",
        null=True,
        blank=True
    )
    fecha_fin = models.DateField(
        verbose_name="Fecha fin",
        null=True,
        blank=True
    )

    fecha_inicio_real = models.DateField(
        verbose_name="Fecha inicio real",
        null=True,
        blank=True
    )

    fecha_fin_real = models.DateField(
        verbose_name="Fecha fin real",
        null=True,
        blank=True
    )

    dias = models.IntegerField(
        verbose_name="Días",
        help_text="Días tomados o compensados"
    )
    dias_habiles = models.IntegerField(
        verbose_name="Días hábiles",
        default=0
    )
    dias_no_habiles = models.IntegerField(
        verbose_name="Días no hábiles",
        default=0
    )
    fecha_pago = models.DateField(
        verbose_name="Fecha de pago"  
    )
    
    base = models.DecimalField(
        max_digits=15,
        decimal_places=0,
        default=0,
        verbose_name="Base",
        null = True,
        blank = True
    )
    estado = models.BooleanField(default=True, 
        verbose_name="Estado"
    )


    class Meta:
        verbose_name = "Novedad de vacaciones"
        ordering = ['fecha_inicio']

    def __str__(self):
        return f"{self.contrato} | {self.get_tipo_display()} | {self.dias} días"