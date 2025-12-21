from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from .models import UsuarioERP

@receiver(post_save, sender=User)
def crear_usuario_erp(sender, instance, created, **kwargs):
      if created:
        UsuarioERP.objects.create(
            user=instance,
            nombre_completo=instance.get_full_name() or instance.username,
            identificacion=f"PEND-{instance.id}"
        )