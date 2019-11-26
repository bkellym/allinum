from django.conf.urls import url
from django.urls import path, include

from usuarios.views import *

urlpatterns = [
    url(r'^usuario_cadastro/$', usuario_cadastro, name='usuario_cadastro')
]