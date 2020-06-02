from django.contrib.auth.models import User
from django.db import models
from .modelMembro import Membro


class Projeto(models.Model):
    titulo = models.TextField(max_length=100, null=False)
    descricao = models.TextField(max_length=400, null=False)
    lider = models.ForeignKey(User, on_delete=models.CASCADE)
    membros = models.ManyToManyField(Membro)
    ult_alt = models.TextField(max_length=100, null=True)
    data_ult_alt = models.DateField(null=True)
