from django.db import models

# Create your models here.
class t_cargo(models.Model):
    codigo = models.CharField(max_length=5)
    nombre = models.CharField(max_length=50)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre
    
class t_area(models.Model):
    codigo = models.CharField(max_length=10)
    nombre = models.CharField(max_length=100)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre
    
class t_lista(models.Model):
    codigo = models.CharField(max_length=6)
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=100)

    def __str__(self):
        return "%s %s"%(self.codigo,self.nombre)
    