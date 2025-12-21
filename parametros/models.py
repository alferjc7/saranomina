from django.db import models

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
