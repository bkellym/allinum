from django.db import models
from .modelMembro import Membro
from .modelProjeto import Projeto
from .modelCategoria import Categoria


class Tarefa(models.Model):
    titulo = models.CharField(max_length=100, null=False)
    resp = models.ForeignKey(Membro, on_delete=models.CASCADE)
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE)
    prioridade = models.CharField(max_length=15, null=True)
    data_limite = models.DateField(null=True)
    concluido = models.BooleanField(default=False)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
