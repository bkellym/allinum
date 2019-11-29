from datetime import date

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    matricula = models.TextField(max_length=20, unique=True)
    tema = models.TextField(max_length=1)
    fontes_grandes = models.BooleanField(default=False)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def alter_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Membro(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_membro(sender, instance, created, **kwargs):
    if created:
        Membro.objects.create(user=instance)

@receiver(post_save, sender=User)
def alter_user_membro(sender, instance, **kwargs):
    instance.membro.save()

class Categoria(models.Model):
    nome = models.CharField(max_length=100, null=False)

class Projeto(models.Model):
    titulo = models.TextField(max_length=100, null=False)
    descricao = models.TextField(max_length=400, null=False)
    lider = models.ForeignKey(User, on_delete=models.CASCADE)
    membros = models.ManyToManyField(Membro)
    ult_alt = models.TextField(max_length=100, null=True)
    data_ult_alt = models.DateField(null=True)

class Tarefa(models.Model):
    titulo = models.CharField(max_length=100, null=False)
    resp = models.ForeignKey(Membro, on_delete=models.CASCADE)
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE)
    prioridade = models.CharField(max_length=15, null=True)
    data_limite = models.DateField(null=True)
    concluido = models.BooleanField(default=False)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)


class Requisito(models.Model):
    titulo = models.CharField(max_length=100, null=False)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE)