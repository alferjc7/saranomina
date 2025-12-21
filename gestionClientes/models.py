from django.db import models

class t_cliente(models.Model):
    codigo_cliente = models.CharField(max_length=6, verbose_name="Codigo cliente")
    nombre_cliente = models.CharField(max_length=100, verbose_name="Nombre cliente")
    estado_cliente = models.BooleanField(default=True, verbose_name="Estado cliente")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.codigo_cliente:
            self.codidgo_cliente = self.codigo_cliente.upper()
        if self.nombre_cliente:
            self.nombre_cliente = self.nombre_cliente.upper()
    def __str__(self):
        return self.codidgo_cliente
    
class t_empresa(models.Model):
    codigo_cliente = models.ForeignKey(
        t_cliente,
        on_delete=models.PROTECT,
        related_name='clientes',
        verbose_name= "Codigo clientes"
     )
    codigo_empresa = models.CharField(max_length=6,verbose_name="Codigo empresa")
    nit_empresa = models.CharField(max_length=20, verbose_name="Nit empresa")
    razon_social = models.CharField(max_length=200, verbose_name="Razon social")
    direccion = models.CharField(max_length=200, verbose_name="Direccion empresa")
    telefono = models.CharField(max_length=24, verbose_name="Telefono")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.codigo_empresa:
            self.codidgo_empresa = self.codigo_empresa.upper()
        if self.razon_social:
            self.razon_social = self.razon_social.upper()
        if self.direccion:
            self.direccion = self.direccion.upper()
    def __str__(self):
        return self.codigo_empresa

    




