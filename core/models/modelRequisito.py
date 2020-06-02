from django.db import models
from .modelCategoria import Categoria
from .modelProjeto import Projeto


class Requisito(models.Model):
    titulo = models.CharField(max_length=100, null=False)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE)
