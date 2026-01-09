from django.db import models
from django.conf import settings


class t_cliente(models.Model):
    nombre_cliente = models.CharField(max_length=100, verbose_name="Nombre cliente")
    estado_cliente = models.BooleanField(default=True, verbose_name="Estado cliente")
    celular = models.CharField(max_length=24, verbose_name="Celular", blank = True, null = True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.nombre_cliente:
            self.nombre_cliente = self.nombre_cliente.upper()
    def __str__(self):
        return self.nombre_cliente
    
class t_empresa(models.Model):
    codigo_cliente = models.ForeignKey(
        t_cliente,
        on_delete=models.PROTECT,
        related_name='clientes',
        verbose_name= "Cliente"
     )
    codigo_empresa = models.CharField(max_length=6,verbose_name="Codigo empresa")
    nit_empresa = models.CharField(max_length=20, verbose_name="Nit empresa")
    digito_verificacion = models.CharField(max_length=1, verbose_name="Digito Verificacion", blank = True, null = True)
    razon_social = models.CharField(max_length=200, verbose_name="Razon social")
    direccion = models.CharField(max_length=200, verbose_name="Direccion empresa")
    telefono = models.CharField(max_length=24, verbose_name="Telefono")
    
    def save(self, *args, **kwargs):
        if self.codigo_empresa:
            self.codigo_empresa = self.codigo_empresa.upper()
        if self.razon_social:
            self.razon_social = self.razon_social.upper()
        if self.direccion:
            self.direccion = self.direccion.upper()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.codigo_empresa

User = settings.AUTH_USER_MODEL

class UsuarioEmpresa(models.Model):
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='empresas'
    )
    empresa = models.ForeignKey(
        t_empresa,
        on_delete=models.CASCADE,
        related_name='usuarios'
    )
    activo = models.BooleanField(default=True)

    fecha_asignacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'empresa')

    def __str__(self):
        return f"{self.usuario} - {self.empresa.codigo_empresa}"
