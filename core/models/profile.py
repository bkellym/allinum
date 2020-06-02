from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    matricula = models.TextField(max_length=20, unique=True)
    tema = models.TextField(max_length=1)
    fontes_grandes = models.BooleanField(default=False)


# noinspection PyUnusedLocal
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


# noinspection PyUnusedLocal
@receiver(post_save, sender=User)
def alter_user_profile(sender, instance, **kwargs):
    instance.profile.save()
