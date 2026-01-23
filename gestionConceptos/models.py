from django.db import models
from gestionClientes.models import t_empresa

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
    
class t_conceptos(models.Model):
    TIPO_CONCEPTO = (
        ('DEV', 'DEVENGO'),
        ('DED', 'DEDUCCION'),
        ('PRO', 'PROVISION'),
    )
    cod_concepto = models.CharField(max_length=5, verbose_name= "Codigo concepto", unique= True)
    desc_concepto = models.CharField(max_length=100, verbose_name= "Descripcion concepto")
    desc_concepto_eng = models.CharField(max_length=100, verbose_name= "Descripcion en ingles")
    tipo_concepto = models.CharField(max_length=3, choices= TIPO_CONCEPTO ,verbose_name= "Tipo de concepto")
    user_creator = models.CharField(max_length=50,blank= True, null= True)
    date_created = models.DateField(blank= True, null= True)
    
    def save(self, *args, **kwargs):
        if self.desc_concepto:
            self.desc_concepto = self.desc_concepto.upper()
        if self.desc_concepto_eng:
            self.desc_concepto_eng = self.desc_concepto_eng.upper()
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.cod_concepto+" "+self.desc_concepto


class t_concepto_empresa(models.Model):
    TIPO_REDONDEO = (
        ('SR', 'Sin redondeo'),
        ('T', 'Truncar'),
        ('RA', 'Redondeo arriba'),
        ('RB', 'Redondeo abajo'),
        ('C', 'Centenar cercano'),
    )

    SIN_VALOR = (
        ('BO', 'BORRAR LINEA'),
        ('NB', 'NO BORRAR LINEA'),
        )

    empresa = models.ForeignKey(t_empresa, on_delete=models.CASCADE, verbose_name= "Empresa")
    cod_concepto = models.ForeignKey(t_conceptos, on_delete=models.CASCADE, verbose_name= "Concepto")
    desc_concepto_emp = models.CharField(max_length=100, verbose_name= "Descripcion concepto")
    tipo_redondeo = models.CharField(max_length=2, choices= TIPO_REDONDEO ,verbose_name= "Tipo de redondeo")
    sin_valor = models.CharField(max_length=2, choices= SIN_VALOR ,verbose_name= "Sin valor")
    concepto_espejo = models.ForeignKey(
        t_conceptos,
        on_delete=models.SET_NULL,   
        blank=True,                  
        null=True,                  
        related_name='concepto_espejo',
        verbose_name="Concepto espejo"
    )
    concepto_cliente = models.CharField(max_length=10, verbose_name= "Concepto cliente", blank = True, null = True)
    user_creator = models.CharField(max_length=50,blank= True, null= True)
    date_created = models.DateField(blank= True, null= True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['empresa', 'cod_concepto'],
                name='unique_concepto_por_empresa'
            )
        ]
        verbose_name = "Concepto por empresa"
        verbose_name_plural = "Conceptos por empresa"

    def save(self, *args, **kwargs):
        if self.desc_concepto_emp:
            self.desc_concepto_emp = self.desc_concepto_emp.upper()
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.desc_concepto_emp


class t_grupo_concepto(models.Model):
    codigo = models.CharField(
        max_length=6,
        unique=True)
    titulo = models.CharField(
        max_length=100)
    descripcion = models.TextField(
        blank=True)
    user_creator = models.CharField(max_length=50,blank= True, null= True)
    date_created = models.DateField(blank= True, null= True)

    def save(self, *args, **kwargs):
        if self.codigo:
            self.codigo = self.codigo.upper()
        if self.titulo:
            self.titulo = self.titulo.upper()
        if self.descripcion:
            self.descripcion = self.descripcion.upper()
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.codigo} - {self.titulo}"
    
class t_grupo_concepto_det(models.Model):
    
    OPERACION = (
        ('+', 'SUMAR'),
        ('-', 'RESTAR'),)

    grupo = models.ForeignKey(t_grupo_concepto,  on_delete=models.CASCADE, verbose_name= "Grupo")
    concepto = models.ForeignKey(t_concepto_empresa, on_delete=models.CASCADE, verbose_name="Concepto") 
    operacion = models.CharField(max_length=1, choices= OPERACION ,verbose_name= "Operacion")    
    user_creator = models.CharField(max_length=50,blank= True, null= True)
    date_created = models.DateField(blank= True, null= True)

    class Meta:
        unique_together = ('grupo', 'concepto')   
        
