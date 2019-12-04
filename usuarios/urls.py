from django.conf.urls import url
from django.urls import path, include

from usuarios.views import *

urlpatterns = [
    url(r'^login/$', efetuar_login, name='login'),
    url(r'^logout/$', efetuar_logout, name='logout'),
    url(r'^usuario_cadastro/$', usuario_cadastro, name='usuario_cadastro'),
    url(r'^usuario_delete/$', usuario_delete, name='usuario_delete'),
    url(r'^usuario_editar/(?P<pk>[0-9]+)', usuario_editar, name='usuario_editar'),
    url(r'^usuario_lista/$', usuario_lista, name='usuario_lista'),
    url(r'^usuario_configuracao/$', usuario_configuracao, name='usuario_configuracao'),
    url(r'^projeto_cadastro/$', projeto_cadastro, name='projeto_cadastro'),
    url(r'^projeto_delete/$', projeto_delete, name='projeto_delete'),
    url(r'^projeto_editar/(?P<pk>[0-9]+)', projeto_editar, name='projeto_editar'),
    url(r'^projeto_lista/$', projeto_lista, name='projeto_lista'),
    url(r'^tarefa_cadastro/(?P<pk>[0-9]+)', tarefa_cadastro, name='tarefa_cadastro'),
    url(r'^tarefa_editar/(?P<pk>[0-9]+)', tarefa_editar, name='tarefa_editar'),
    url(r'^tarefa_delete/$', tarefa_delete, name='tarefa_delete'),
    url(r'^visao_tarefa/$', tarefa_visao, name='visao_tarefa'),
    url(r'^visao_projeto/(?P<pk>[0-9]+)', projeto_visao, name='visao_projeto'),
    url(r'^visao_projeto_tarefa/(?P<pk>[0-9]+)', tarefas_do_usuario_projeto, name='visao_projeto_tarefa'),
    url(r'^visao_requisito/(?P<pk>[0-9]+)', visao_requisitos, name='visao_requisito'),
    url(r'^requisito_cadastro/$', requisito_cadastro, name='requisito_cadastro'),
    url(r'^requisito_delete/$', requisito_delete, name='requisito_delete'),
    url(r'^redefinicao_senha_admin/$', redefinicao_senha_admin, name='redefinicao_senha_admin'),
    url(r'^redefinicao_senha/$', redefinicao_senha, name='redefinicao_senha'),
    url(r'^esqueceu_senha/$', esqueceu_senha, name='esqueceu_senha'),
    url(r'^concluir_tarefa/(?P<pk>[0-9]+)', concluir_tarefa, name='concluir_tarefa')
]