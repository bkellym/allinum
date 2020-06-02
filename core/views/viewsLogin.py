from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from core.models import *


# Create your views here.
def efetuar_login(request, template_name="login.html"):
    next = request.GET.get('next', '/projeto_lista/')
    if request.method == "POST":
        # Recebendo valores do formulário
        username = request.POST['username']
        password = request.POST['password']
        username = username.lower()

        # Autenticação do usuário
        user = authenticate(username=username, password=password)

        # Se usuário foi retornado realiza o Login
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(next)

        # Se usuário não for encontrado, retorna erro
        else:
            messages.error(request, 'Usuário ou senha incorretos.')
            return HttpResponseRedirect(settings.LOGIN_URL)

    return render(request, template_name, {'redirect_to': next})


def efetuar_logout(request):
    logout(request)
    return HttpResponseRedirect(settings.LOGIN_URL)


def esqueceu_senha(request, template_name="esqueceu_senha.html"):
    return render(request, template_name)


@login_required
def redefinicao_senha_admin(request):
    admin = request.user
    if admin.is_staff:
        senha = request.POST['senha']
        confirma_senha = request.POST['confirma_senha']

        if senha == confirma_senha:
            pk = request.POST['pk']

            try:
                usuario = User.objects.get(pk=pk)
            except:
                messages.error(request, "Usuário não encontrado!")
                return redirect('/usuario_lista/')

            usuario.set_password(senha)
            usuario.save()
            return redirect('/usuario_lista/')
        else:
            messages.error(request, "Senhas não combinam!")
            return redirect('/usuario_lista/')


@login_required
def redefinicao_senha(request):
    user = request.user
    senha_antiga = request.POST['senha_antiga']
    if user.check_password(senha_antiga):
        senha = request.POST['senha']
        confirma_senha = request.POST['confirma_senha']

        if senha == confirma_senha:
            user.set_password(senha)
            user.save()
            return redirect('/usuario_configuracao/')
        else:
            messages.error(request, "Senhas não combinam!")
            return redirect('/usuario_configuracao/')
    else:
        messages.error(request, "Senha atual está incorreta!")
        return redirect('/usuario_configuracao/')
