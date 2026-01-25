from django.db import models
from gestionClientes.models import t_empresa
from parametros.models import t_tipo_nomina, ParametroDetalle
from gestionConceptos.models import t_concepto_empresa
from gestionContratos.models import t_contrato

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
    estado = models.BooleanField(default=True, verbose_name= "Estado")
    user_creator = models.CharField(max_length=50,blank= True, null= True)
    date_created = models.DateField(blank= True, null= True)

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
        return f"{self.codigo}-{self.anio}-{self.mes} P{self.periodo}"
    

class t_logica_calculo(models.Model):

    empresa = models.ForeignKey(
        t_empresa,
        on_delete=models.CASCADE,
        verbose_name="Empresa"
    )

    tipo_nomina = models.ForeignKey(
        t_tipo_nomina,
        on_delete=models.CASCADE,
        verbose_name="Tipo de Nomina"
    )
    
    modulo = models.ForeignKey(
        ParametroDetalle, 
        on_delete=models.CASCADE, 
        limit_choices_to={'parametro__codigo': 'MOD'}, 
        verbose_name= "Modulo", blank = True, null = True) 
    
    periodo = models.IntegerField(verbose_name="Periodo")    
    concepto = models.ForeignKey(
        t_concepto_empresa, 
        on_delete=models.CASCADE, 
        verbose_name= "Concepto"
        ) 

    logica = models.CharField(max_length=200,blank= True, null= True)
    orden = models.IntegerField(verbose_name="Orden")
    user_creator = models.CharField(max_length=50,blank= True, null= True)
    date_created = models.DateField(blank= True, null= True)
    
    class Meta:
        verbose_name = "Lógica de cálculo"
        verbose_name_plural = "Lógicas de cálculo"
        constraints = [
            models.UniqueConstraint(
                fields=['empresa', 'tipo_nomina', 'periodo', 'concepto'],
                name='uq_logica_empresa_nomina_periodo_concepto'
            )
        ]

    def __str__(self):
        return f"{self.empresa} - {self.concepto} - {self.logica}"

class t_acumulado_empleado(models.Model):

    contrato = models.ForeignKey(
        t_contrato,
        on_delete=models.CASCADE,
        verbose_name="Contrato"
    )

    tipo_nomina = models.ForeignKey(
        t_tipo_nomina,
        on_delete=models.CASCADE,
        verbose_name="Tipo de nómina"
    )

    anio = models.IntegerField(verbose_name="Año")
    mes = models.IntegerField(verbose_name="Mes")
    periodo = models.IntegerField(verbose_name="Periodo")

    fecha_novedad = models.DateField(
        verbose_name="Fecha novedad",
        blank=True,
        null=True
    )

    fecha_inicio = models.DateField(
        verbose_name="Fecha inicio",
        blank=True,
        null=True
    )

    fecha_fin = models.DateField(
        verbose_name="Fecha fin",
        blank=True,
        null=True
    )

    concepto = models.ForeignKey(
        t_concepto_empresa,
        on_delete=models.CASCADE,
        verbose_name="Concepto"
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
        verbose_name="Base"
    )

    valor = models.DecimalField(
        max_digits=15,
        decimal_places=0,
        default=0,
        verbose_name="Valor"
    )

    modulo = models.ForeignKey(
        ParametroDetalle,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        limit_choices_to={'parametro__codigo': 'MOD'},
        verbose_name="Módulo"
    )

    periodo_nomina = models.ForeignKey(
        t_periodo_nomina,
        on_delete=models.CASCADE,
        verbose_name="Periodo Nomina"
    )

    t01 = models.CharField(max_length=100, blank=True, null=True)
    v01 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    t02 = models.CharField(max_length=100, blank=True, null=True)
    v02 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    t03 = models.CharField(max_length=100, blank=True, null=True) 
    v03 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    t04 = models.CharField(max_length=100, blank=True, null=True)
    v04 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    t05 = models.CharField(max_length=100, blank=True, null=True)
    v05 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    t06 = models.CharField(max_length=100, blank=True, null=True) 
    v06 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    t07 = models.CharField(max_length=100, blank=True, null=True)
    v07 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    t08 = models.CharField(max_length=100, blank=True, null=True)
    v08 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    t09 = models.CharField(max_length=100, blank=True, null=True) 
    v09 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    t10 = models.CharField(max_length=100, blank=True, null=True)
    v10 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    t11 = models.CharField(max_length=100, blank=True, null=True)
    v11 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    t12 = models.CharField(max_length=100, blank=True, null=True) 
    v12 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    t13 = models.CharField(max_length=100, blank=True, null=True) 
    v13 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    t14 = models.CharField(max_length=100, blank=True, null=True)
    v14 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    t15 = models.CharField(max_length=100, blank=True, null=True)
    v15 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    t16 = models.CharField(max_length=100, blank=True, null=True) 
    v16 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    t17 = models.CharField(max_length=100, blank=True, null=True)
    v17 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    t18 = models.CharField(max_length=100, blank=True, null=True)
    v18 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    t19 = models.CharField(max_length=100, blank=True, null=True) 
    v19 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    t20 = models.CharField(max_length=100, blank=True, null=True)
    v20 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    ft01 = models.CharField(max_length=100, blank=True, null=True)
    f01 = models.DateField(blank=True, null=True)
    ft02 = models.CharField(max_length=100, blank=True, null=True)
    f02 = models.DateField(blank=True, null=True)
    ft03 = models.CharField(max_length=100, blank=True, null=True)
    f03 = models.DateField(blank=True, null=True)
    ft04 = models.CharField(max_length=100, blank=True, null=True)
    f04 = models.DateField(blank=True, null=True)


class t_acumulado_empleado_def(models.Model):

    contrato = models.ForeignKey(
        t_contrato,
        on_delete=models.CASCADE,
        verbose_name="Contrato"
    )

    tipo_nomina = models.ForeignKey(
        t_tipo_nomina,
        on_delete=models.CASCADE,
        verbose_name="Tipo de nómina"
    )

    anio = models.IntegerField(verbose_name="Año")
    mes = models.IntegerField(verbose_name="Mes")
    periodo = models.IntegerField(verbose_name="Periodo")

    fecha_novedad = models.DateField(
        verbose_name="Fecha novedad",
        blank=True,
        null=True
    )

    fecha_inicio = models.DateField(
        verbose_name="Fecha inicio",
        blank=True,
        null=True
    )

    fecha_fin = models.DateField(
        verbose_name="Fecha fin",
        blank=True,
        null=True
    )

    concepto = models.ForeignKey(
        t_concepto_empresa,
        on_delete=models.CASCADE,
        verbose_name="Concepto"
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
        verbose_name="Base"
    )

    valor = models.DecimalField(
        max_digits=15,
        decimal_places=0,
        default=0,
        verbose_name="Valor"
    )

    modulo = models.ForeignKey(
        ParametroDetalle,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        limit_choices_to={'parametro__codigo': 'MOD'},
        verbose_name="Módulo"
    )

    periodo_nomina = models.ForeignKey(
        t_periodo_nomina,
        on_delete=models.CASCADE,
        verbose_name="Periodo Nomina"
    )

    t01 = models.CharField(max_length=100, blank=True, null=True)
    v01 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    t02 = models.CharField(max_length=100, blank=True, null=True)
    v02 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    t03 = models.CharField(max_length=100, blank=True, null=True) 
    v03 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    t04 = models.CharField(max_length=100, blank=True, null=True)
    v04 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    t05 = models.CharField(max_length=100, blank=True, null=True)
    v05 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    t06 = models.CharField(max_length=100, blank=True, null=True) 
    v06 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    t07 = models.CharField(max_length=100, blank=True, null=True)
    v07 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    t08 = models.CharField(max_length=100, blank=True, null=True)
    v08 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    t09 = models.CharField(max_length=100, blank=True, null=True) 
    v09 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    t10 = models.CharField(max_length=100, blank=True, null=True)
    v10 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    t11 = models.CharField(max_length=100, blank=True, null=True)
    v11 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    t12 = models.CharField(max_length=100, blank=True, null=True) 
    v12 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    t13 = models.CharField(max_length=100, blank=True, null=True) 
    v13 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    t14 = models.CharField(max_length=100, blank=True, null=True)
    v14 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    t15 = models.CharField(max_length=100, blank=True, null=True)
    v15 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    t16 = models.CharField(max_length=100, blank=True, null=True) 
    v16 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    t17 = models.CharField(max_length=100, blank=True, null=True)
    v17 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    t18 = models.CharField(max_length=100, blank=True, null=True)
    v18 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    t19 = models.CharField(max_length=100, blank=True, null=True) 
    v19 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    t20 = models.CharField(max_length=100, blank=True, null=True)
    v20 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    ft01 = models.CharField(max_length=100, blank=True, null=True)
    f01 = models.DateField(blank=True, null=True)
    ft02 = models.CharField(max_length=100, blank=True, null=True)
    f02 = models.DateField(blank=True, null=True)
    ft03 = models.CharField(max_length=100, blank=True, null=True)
    f03 = models.DateField(blank=True, null=True)
    ft04 = models.CharField(max_length=100, blank=True, null=True)
    f04 = models.DateField(blank=True, null=True)



class t_proceso_nomina(models.Model):

    ESTADOS = (
        ("P", "PROCESANDO"),
        ("F", "FINALIZADO"),
        ("X", "ERROR"),
        ("C","CERRADO")
    )

    periodo_nomina = models.ForeignKey(
        t_periodo_nomina,
        on_delete=models.CASCADE,
        verbose_name="Periodo nómina"
    )

    estado = models.CharField(
        max_length=1,
        choices=ESTADOS,
        default="P",
        verbose_name= "Estado"
    )
    progreso = models.PositiveSmallIntegerField(
        default=0,
        verbose_name="Progreso (%)"
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_finished = models.DateTimeField(blank=True, null=True)
    mensaje_error = models.TextField(blank=True, null=True)
    user_creator = models.CharField(max_length=50, blank=True, null=True)


class t_logica_calculo_filtro(models.Model):
    OPERADOR_CHOICES = [
    ('IN', 'EN LISTA'),
    ('NOT_IN', 'NO EN LA LISTA'),
    ]
    
    logica_calculo = models.ForeignKey(
        t_logica_calculo,
        on_delete=models.CASCADE,
        related_name='filtros',
        verbose_name="Lógica de cálculo"
    )
    campo = models.CharField(
        max_length=50,
        verbose_name="Campo a evaluar"
    )
    operador = models.CharField(
        max_length=20,
        choices=OPERADOR_CHOICES,
        verbose_name="Operador"
    )
    valor = models.IntegerField(verbose_name= 'Valor')
    
    user_creator = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )
    date_created = models.DateField(
        blank=True,
        null=True
    )

