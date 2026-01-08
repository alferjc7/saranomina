from django import forms
from django.db import models

# Create your models here.
class t_tipo_ide(models.Model):
    cod_ide = models.CharField(max_length=8, verbose_name= 'Codigo')
    desc_ide = models.CharField(max_length=32, verbose_name= 'Descripcion',)
    estado_ide = models.BooleanField(verbose_name= 'Estado')
    user_creator = models.CharField(max_length=50,blank= True, null= True)
    date_created = models.DateField()
    def save(self, *args, **kwargs):
        if self.cod_ide:
            self.cod_ide = self.cod_ide.upper()
        if self.desc_ide:
            self.desc_ide = self.desc_ide.upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return "%s"%(self.desc_ide)
    
class t_identificacion(models.Model):
    TIPO_ESTADO = [
        ('','Seleccion una opcion '),
        (1, 'SOLTERO(A)'),
        (2, 'CASADO(A)'),
        (3, 'DIVORCIADO(A)'),
        (4, 'UNION LIBRE'),
        (5, 'VIUDO(A)')
    ]
    TIPO_SEXO = [
        ('','Seleccione una opcion '),
        (1, 'FEMENINO'),
        (2, 'MASCULINO'),
        (3, 'NO DEFINIDO')
    ]

    tipo_ide = models.ForeignKey(
        t_tipo_ide,
        on_delete=models.PROTECT,
        related_name='personas',
        verbose_name= "Tipo identificación"
    )
    identificacion = models.CharField(max_length=24, verbose_name= "Numero documento")
    nombre = models.CharField(max_length=100, verbose_name= "Primer nombre")
    segundo_nombre =  models.CharField(max_length=100, blank= True, null= True, verbose_name= "Segundo nombre")
    apellido = models.CharField(max_length=100, verbose_name= "Primer apellido")
    segundo_apellido =  models.CharField(max_length=100, blank= True, null= True, verbose_name= "Segundo apellido")
    fecha_nacimiento = models.DateField(verbose_name= "Fecha nacimiento")
    fecha_exp_doc = models.DateField(verbose_name="Fecha expedicion documento")
    telefono = models.CharField(max_length=30, verbose_name= "Telefono", blank = True, null = True)
    celular = models.CharField(max_length=30, verbose_name= "Celular")
    direccion = models.CharField(max_length=100, verbose_name= "Direccion")
    estado_civil = models.IntegerField(
        choices=TIPO_ESTADO,
        verbose_name="Estado civil",
        blank=True,
        null=True
    )
    genero = models.IntegerField(
        choices=TIPO_SEXO,
        verbose_name="Genero",
        blank=True,
        null=True
    )    
    correo_personal = models.EmailField(verbose_name="Correo personal")
    correo_coorporativo = models.EmailField(verbose_name="Correo coorporativo", blank= True, null= True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['tipo_ide', 'identificacion'],
                name='unique_tipo_numero'
                
            )
        ]

    def __str__(self):
        return "%s"%(self.identificacion)
    
    def save(self, *args, **kwargs):
        if self.nombre:
            self.nombre = self.nombre.upper()
        if self.segundo_nombre:
            self.segundo_nombre = self.segundo_nombre.upper()
        if self.apellido:
            self.apellido = self.apellido.upper()
        if self.segundo_apellido:
            self.segundo_apellido = self.segundo_apellido.upper()
        if self.correo_coorporativo:
            self.correo_coorporativo = self.correo_coorporativo.upper()
        if self.correo_personal:
            self.correo_personal = self.correo_personal.upper()
        super().save(*args, **kwargs)

 
class t_beneficiario(models.Model):
    
    TIPO_PARENTESCO = [
        ('','Seleccione una opcion '),
        (1, 'MADRE'),
        (2, 'PADRE'),
        (3, 'HIJO'),
        (4, 'CONYUGUE')
    ]

    tipo_ide_ben = models.ForeignKey(
        t_tipo_ide,
        on_delete= models.CASCADE,
        verbose_name= "Tipo identificación"
    )

    iden_beneficiario = models.CharField(
        max_length=24,
        verbose_name="Identificacion beneficiario"
    )

    iden_titular = models.ForeignKey(
        t_identificacion,
        on_delete= models.CASCADE,
        related_name='beneficiarios',
        verbose_name= "Identificacion titular"
    )
    nombre_completo = models.CharField(max_length=200, verbose_name= "Nombre completo")
    fecha_nacimiento = models.DateField(verbose_name= "Fecha nacimiento")
    parentesco = models.IntegerField(
        choices= TIPO_PARENTESCO,
        verbose_name="Parentesco",
        blank=True,
        null=True
    )
    exogena = models.BooleanField(verbose_name= 'Exogena', default=True)
        
    def save(self, *args, **kwargs):
        if self.nombre_completo:
            self.nombre_completo = self.nombre_completo.upper()
        return super().save(*args, **kwargs)

    





