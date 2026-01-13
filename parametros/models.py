from django.db import models
from gestionConceptos.models import t_conceptos

# Create your models here.
class t_tipo_contrato(models.Model):
    contrato = models.CharField(max_length=50, verbose_name="Tipo de contrato")
    estado = models.BooleanField(default=True, verbose_name="Estado")
    user_creator = models.CharField(max_length=50,blank= True, null= True)
    date_created = models.DateField(blank= True, null= True)
    def save(self, *args, **kwargs):
        if self.contrato:
            self.contrato = self.contrato.upper()
        return super().save(*args, **kwargs)
    def __str__(self):
        return self.contrato

class t_tipo_salario(models.Model):
    salario = models.CharField(max_length=50, verbose_name="Tipo de salario")
    estado = models.BooleanField(default=True, verbose_name="Estado")
    user_creator = models.CharField(max_length=50,blank= True, null= True)
    date_created = models.DateField(blank= True, null= True)
    def save(self, *args, **kwargs):
        if self.salario:
            self.salario = self.salario.upper()
        return super().save(*args, **kwargs)
    def __str__(self):
        return self.salario
    
class t_tipo_cotizante(models.Model):
    codigo = models.CharField(max_length=2, verbose_name="Codigo")
    descripcion = models.CharField(max_length=100, verbose_name="Descripcion")
    estado = models.BooleanField(default=True, verbose_name="Estado")
    user_creator = models.CharField(max_length=50,blank= True, null= True)
    date_created = models.DateField(blank= True, null= True)
    def __str__(self):
        return self.descripcion
    def save(self, *args, **kwargs):
        if self.descripcion:
            self.descripcion = self.descripcion.upper()
        return super().save(*args, **kwargs)
    
class t_subtipo_cotizante(models.Model):
    codigo_cotizante = models.ForeignKey(
        t_tipo_cotizante,
        on_delete=models.PROTECT,
        related_name='subtipos',
        verbose_name= "Cotizante"
     )
    codigo = models.CharField(max_length=2, verbose_name="Codigo")
    descripcion = models.CharField(max_length=100, verbose_name="Descripcion")
    estado = models.BooleanField(default=True, verbose_name="Estado")
    user_creator = models.CharField(max_length=50,blank= True, null= True)
    date_created = models.DateField(blank= True, null= True)
    def save(self, *args, **kwargs):
        if self.descripcion:
            self.descripcion = self.descripcion.upper()
        return super().save(*args, **kwargs)
    def __str__(self):
        return self.descripcion
    
   
class t_banco(models.Model):
    banco = models.CharField(max_length=200, verbose_name="Banco")
    codigo_ach = models.CharField(max_length=3, verbose_name="Codigo ACH", blank=True, null= True)
    codigo_pse = models.CharField(max_length=4, verbose_name="Codigo PSE", blank=True, null= True)
    codigo_br = models.CharField(max_length=2, verbose_name="Codigo BR", blank=True, null= True)
    codigo_fintech = models.CharField(max_length=4, verbose_name="Codigo FINTECH", blank=True, null= True)
    estado = models.BooleanField(default=True, verbose_name="Estado")
    user_creator = models.CharField(max_length=50,blank= True, null= True)
    date_created = models.DateField(blank= True, null= True)
    def __str__(self):
        return self.banco
    def save(self, *args, **kwargs):
        if self.banco:
            self.banco = self.banco.upper()
        return super().save(*args, **kwargs)
 

class t_entidadesss(models.Model):
    TIPOS= (
        ('EPS', 'EPS'),
        ('AFP', 'AFP'),
        ('CCF', 'Caja compensacion'),
        ('ARL', 'ARL'),
    )
    tipo = models.CharField(max_length=3, choices=TIPOS)
    codigo = models.CharField(max_length=10, verbose_name="Codigo")
    nit = models.CharField(max_length=16, verbose_name="Nit Entidad")
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    user_creator = models.CharField(max_length=50,blank= True, null= True)
    date_created = models.DateField(blank= True, null= True)
    def save(self, *args, **kwargs):
        if self.nombre:
            self.nombre = self.nombre.upper()
        if self.codigo:
            self.codigo = self.codigo.upper()
        return super().save(*args, **kwargs)
    def __str__(self):
        return self.nombre
    
class t_conceptos_salario(models.Model):
    tipo_salario = models.ForeignKey(t_tipo_salario, on_delete=models.CASCADE, verbose_name= "Tipo salario", unique= True)
    concepto = models.ForeignKey(t_conceptos, on_delete=models.CASCADE, verbose_name= "Concepto")
    user_creator = models.CharField(max_length=50,blank= True, null= True)
    date_created = models.DateField(blank= True, null= True)

class t_tipo_nomina(models.Model):
    codigo = models.CharField(max_length=2, verbose_name="Codigo")
    descripcion = models.CharField(max_length=100, verbose_name="Descripcion")
    estado = models.BooleanField(default=True, verbose_name="Estado")
    asigna_contrato = models.BooleanField(default=True, verbose_name="Se asigna a contrato")
    user_creator = models.CharField(max_length=50,blank= True, null= True)
    date_created = models.DateField(blank= True, null= True)
    def save(self, *args, **kwargs):
        if self.codigo:
            self.codigo = self.codigo.upper()
        if self.descripcion:
            self.descripcion = self.descripcion.upper()
        return super().save(*args, **kwargs)
    def __str__(self):
        return self.descripcion

class ParametroGeneral(models.Model):
    codigo = models.CharField(
        max_length=6,
        unique=True)
    titulo = models.CharField(
        max_length=100)
    descripcion = models.TextField(
        blank=True)
    activo = models.BooleanField(
        default=True)
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
    
class ParametroDetalle(models.Model):
    parametro = models.ForeignKey(
        ParametroGeneral,
        on_delete=models.CASCADE,
        related_name="detalles")

    codigo = models.CharField(
        max_length=6)
    valor_texto = models.CharField(
        max_length=255,
        blank=True,
        null=True)
    valor_numerico = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        blank=True,
        null=True)
    fecha_inicio = models.DateField(
        blank=True,
        null=True)
    fecha_fin = models.DateField(
        blank=True,
        null=True)
    valor_booleano = models.BooleanField(
        default=False)
    activo = models.BooleanField(
        default=True)
    user_creator = models.CharField(max_length=50,blank= True, null= True)
    date_created = models.DateField(blank= True, null= True)
    

    class Meta:
        unique_together = ('parametro', 'codigo')
        
    def save(self, *args, **kwargs):
        if self.codigo:
            self.codigo = self.codigo.upper()
        if self.valor_texto:
            self.valor_texto = self.valor_texto.upper()
        return super().save(*args, **kwargs)
    def __str__(self):
        codigo = self.codigo or ''
        valor_texto = self.valor_texto or ''
        valor_numerico = self.valor_numerico or ''
        return f"{valor_texto}"
        