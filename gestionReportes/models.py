from django.db import models

class Reporte(models.Model):
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    ruta_jasper = models.CharField(
        max_length=255,
        help_text="Ruta interna al archivo .jasper"
    )
    activo = models.BooleanField(default=True)
    user_creator = models.CharField(max_length=150, blank=True, null=True)
    date_created = models.DateTimeField(blank= True, null= True)

    def __str__(self):
        return self.nombre
    
class ParametroReporte(models.Model):
    TIPO_DATO_CHOICES = [
        ('str', 'Texto'),
        ('int', 'Entero'),
        ('date', 'Fecha'),
        ('bool', 'Booleano'),
    ]

    reporte = models.ForeignKey(
        Reporte,
        on_delete=models.CASCADE,
        related_name='parametros'
    )
    nombre = models.CharField(max_length=50)
    etiqueta = models.CharField(max_length=100)
    tipo_dato = models.CharField(max_length=10, choices=TIPO_DATO_CHOICES)
    requerido = models.BooleanField(default=True)
    orden = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.reporte.nombre} - {self.nombre}"
    

