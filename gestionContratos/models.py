from django.db import models
from gestionClientes.models import t_empresa
from gestionIdentificacion.models import t_identificacion
from parametros.models import (t_tipo_salario, t_tipo_contrato, 
                               t_tipo_cotizante, t_subtipo_cotizante, 
                               t_banco, t_entidadesss, t_tipo_nomina, ParametroDetalle)
from django.core.validators import MinValueValidator, MaxValueValidator

class EmpresaQuerySet(models.QuerySet):

    def por_empresa(self, empresa):
        if hasattr(self.model, 'empresa_id'):
            return self.filter(empresa=empresa)
        if hasattr(self.model, 'contrato_id'):
            return self.filter(contrato__empresa=empresa)
        raise NotImplementedError(
            f'El modelo {self.model.__name__} no soporta filtrado por empresa'
        )

class EmpresaManager(models.Manager):

    def get_queryset(self):
        return EmpresaQuerySet(self.model, using=self._db)

    def por_empresa(self, empresa):
        return self.get_queryset().por_empresa(empresa)

class t_contrato(models.Model):

    ESTADOS = (
        ('A', 'ACTIVO'),
        ('S', 'SUSPENDIDO'),
        ('T', 'TERMINADO'),
    )
    CESANTIAS = (
        ('L50', 'LEY 50'),
        ('RT', 'REGIMEN TRADICIONAL'),
        ('I', 'INTEGRAL'),
        ('A', 'APRENDICES'),
    )

    PROCEDIMIENTORET = (
        ('1', 'PROCEDIMIENTO 1'),
        ('2', 'PROCEDIMIENTO 2'),
    )

    empresa = models.ForeignKey(t_empresa, on_delete=models.CASCADE, verbose_name= "Empresa")
    identificacion = models.ForeignKey(t_identificacion, on_delete=models.PROTECT, verbose_name="Identificacion")
    cod_contrato = models.BigIntegerField(verbose_name= "Codigo contrato")
    fecha_ingreso = models.DateField(verbose_name= "Fecha ingreso")
    fecha_fin = models.DateField(verbose_name="Fecha fin" ,blank=True, null=True)
    tipo_contrato = models.ForeignKey(t_tipo_contrato, on_delete=models.CASCADE, verbose_name= "Tipo de contrato")
    periodo_vac = models.IntegerField(verbose_name="Periodo de vacaciones",
    validators=[
        MinValueValidator(0),
        MaxValueValidator(20)
        ])
    tipo_cotizante = models.ForeignKey(t_tipo_cotizante, on_delete=models.CASCADE, verbose_name= "Tipo cotizante")
    subtipo_cotizante = models.ForeignKey(t_subtipo_cotizante, on_delete=models.CASCADE, verbose_name= "Subtipo cotizante")
    codigo_interno = models.CharField(max_length=16, null = True, blank= True)
    procedimiento = models.CharField(max_length=1, choices= PROCEDIMIENTORET)
    porcentaje_retencion = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[
        MinValueValidator(0),
        MaxValueValidator(100)
        ],verbose_name= "Porcentaje retencion",
        null = True,
        blank= True
    ) 

    estado = models.CharField(max_length=1, choices=ESTADOS, default='A') 
    cesantias = models.CharField(max_length=3, choices=CESANTIAS)
    tipo_nomina = models.ForeignKey(t_tipo_nomina, on_delete=models.CASCADE, limit_choices_to={'asigna_contrato': True}, verbose_name= "Tipo de nomina") 
    motivo_retiro = models.ForeignKey(ParametroDetalle, on_delete=models.CASCADE, limit_choices_to={'parametro__codigo': 'RET'}, verbose_name= "Motivo de retito", blank = True, null = True) 
    fecha_ret = models.DateField(verbose_name="Fecha retiro" ,blank=True, null=True)
    user_creator = models.CharField(max_length=50,blank= True, null= True)
    date_created = models.DateField(blank= True, null= True)

    objects = EmpresaManager()

    class Meta:
        unique_together = ('empresa', 'cod_contrato')

    def save(self, *args, **kwargs):
        if not self.cod_contrato:
            ultimo = t_contrato.objects.filter(
                empresa=self.empresa
            ).aggregate(
                max_codigo=models.Max('cod_contrato')
            )['max_codigo']

            self.cod_contrato = (ultimo + 1) if ultimo else 1000000

        super().save(*args, **kwargs)
    
    def __str__(self):
        return str(self.cod_contrato)

class t_contrato_banco(models.Model):
    TIPO_CUENTA = (
        ('A', 'AHORRO'),
        ('C', 'CORRIENTE'),
    )
    contrato = models.ForeignKey(t_contrato, on_delete=models.CASCADE, verbose_name= "Contrato")
    banco = models.ForeignKey(t_banco, on_delete=models.CASCADE, verbose_name= "Banco")
    cuenta = models.CharField(max_length=20, choices= TIPO_CUENTA, verbose_name= "Tipo Cuenta")
    numero_cuenta = models.CharField(max_length=20, verbose_name= "Numero de cuenta", blank = True, null= True)
    fecha_inicio = models.DateField(verbose_name= "Fecha inicio")
    fecha_fin = models.DateField(verbose_name="Fecha fin" ,blank=True, null=True)
    estado = models.BooleanField(default= True, verbose_name= "Estado") 
    user_creator = models.CharField(max_length=50,blank= True, null= True)
    date_created = models.DateField(blank= True, null= True)

    objects = EmpresaManager()


class t_contrato_entidadesss(models.Model):
    TIPO_ENTIDAD = (
        ('AFP', 'AFP'),
        ('EPS', 'EPS'),
        ('CCF', 'CCF'),
        ('ARL', 'ARL'),
    )

    contrato = models.ForeignKey(t_contrato, on_delete=models.CASCADE, verbose_name= "Contrato")
    tipo_entidad = models.CharField(max_length=10, choices= TIPO_ENTIDAD, verbose_name= "Tipo entidad")
    entidad = models.ForeignKey(t_entidadesss, on_delete=models.CASCADE, verbose_name= "Entidad")
    fecha_inicio = models.DateField(verbose_name= "Fecha inicio")
    fecha_fin = models.DateField(verbose_name="Fecha fin" ,blank=True, null=True)
    user_creator = models.CharField(max_length=50,blank= True, null= True)
    date_created = models.DateField(blank= True, null= True)

    objects = EmpresaManager()

class t_contrato_salario(models.Model):
    
    contrato = models.ForeignKey(t_contrato, on_delete=models.CASCADE, verbose_name= "Contrato")
    tipo_salario = models.ForeignKey(t_tipo_salario, on_delete=models.CASCADE, verbose_name= "Tipo de salario")
    salario = models.DecimalField(max_digits=12, decimal_places=0, verbose_name= "Salario")
    fecha_inicio = models.DateField(verbose_name= "Fecha inicio")
    fecha_fin = models.DateField(verbose_name="Fecha fin" ,blank=True, null=True)
    estado = models.BooleanField(default= True, verbose_name= "Estado") 
    retroactivo = models.BooleanField(default= True, verbose_name= "Retroactivo") 
    user_creator = models.CharField(max_length=50,blank= True, null= True)
    date_created = models.DateField(blank= True, null= True)

    objects = EmpresaManager()


class t_contrato_deducibles(models.Model):
    TIPO_DEDUCIBLE = (
        ('DED', 'DEPENDIENTE'),
        ('MED', 'MEDICINA PREPAGADA'),
        ('VIV', 'VIVIENDA'),
        )
    contrato = models.ForeignKey(t_contrato, on_delete=models.CASCADE, verbose_name= "Contrato")
    tipo_deducible = models.CharField(choices= TIPO_DEDUCIBLE, verbose_name= "Tipo deducible")
    valor = models.DecimalField(max_digits=12, decimal_places=0, verbose_name= "Valor")
    fecha_inicio = models.DateField(verbose_name= "Fecha inicio")
    fecha_fin = models.DateField(verbose_name="Fecha fin")
    user_creator = models.CharField(max_length=50,blank= True, null= True)
    date_created = models.DateField(blank= True, null= True)

    objects = EmpresaManager()
