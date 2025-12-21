from django.contrib.auth.models import User
from django.db import models

class UsuarioERP(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='perfil'
    )

    identificacion = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Identificación'
    )

    nombre_completo = models.CharField(
        max_length=150,
        verbose_name='Nombre completo'
    )

    cargo = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    activo = models.BooleanField(default=True)

    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre_completo