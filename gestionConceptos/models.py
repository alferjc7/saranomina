from django.db import models

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
        ('DEV', 'Devengo'),
        ('DED', 'Deduccion'),
        ('PRO', 'Porvision'),
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



