from django.conf.urls import url
from django.urls import path, include

from usuarios.views import *

urlpatterns = [
    url(r'^usuario_cadastro/$', usuario_cadastro, name='usuario_cadastro'),
    url(r'^usuario_lista/$', usuario_lista, name='usuario_lista'),
    url(r'^login/$', efetuar_login, name='login')
]