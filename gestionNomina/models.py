from django.db import models
from gestionClientes.models import t_empresa
from parametros.models import t_tipo_nomina


class t_periodo_nomina(models.Model):

    empresa = models.ForeignKey(
        t_empresa,
        on_delete=models.CASCADE,
        verbose_name="Empresa"
    )

    codigo = models.IntegerField(
        verbose_name="Código período",  
        blank=True,
        null=True)

    tipo_nomina = models.ForeignKey(
        t_tipo_nomina,
        on_delete=models.CASCADE,
        verbose_name="Tipo de nómina"
    )

    anio = models.IntegerField(verbose_name="Año")
    mes = models.IntegerField(verbose_name="Mes")

    periodo = models.IntegerField(verbose_name="Periodo")

    fecha_inicio = models.DateField(verbose_name="Fecha inicio")
    fecha_fin = models.DateField(verbose_name="Fecha fin")

    class Meta:
        unique_together = (
            'empresa',
            'tipo_nomina',
            'anio',
            'mes',
            'periodo'
        )
        ordering = ['anio', 'mes', 'periodo']

    def save(self, *args, **kwargs):
        if not self.codigo:
            ultimo = t_periodo_nomina.objects.filter(
                empresa=self.empresa
            ).aggregate(
                max_codigo=models.Max('codigo')
            )['max_codigo']

            self.codigo = (ultimo + 1) if ultimo else 1000

        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.empresa} - {self.anio}-{self.mes} P{self.periodo}"
    
