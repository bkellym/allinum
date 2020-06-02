from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Membro(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


# noinspection PyUnusedLocal,PyUnusedLocal
@receiver(post_save, sender=User)
def create_user_membro(sender, instance, created, **kwargs):
    if created:
        Membro.objects.create(user=instance)


# noinspection PyUnusedLocal,PyUnusedLocal
@receiver(post_save, sender=User)
def alter_user_membro(sender, instance, **kwargs):
    instance.membro.save()
