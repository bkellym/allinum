from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from usuarios.models import *


# Create your views here.

@login_required
def usuario_cadastro(request, template_name="usuario_cadastro.html"):
    user = request.user

    if user.is_staff:
        if request.method == "POST":

            #Recebendo valores do formulário
            nome = request.POST['nome']
            sobrenome = request._post['sobrenome']
            usuario = request.POST['usuario']
            matricula = request.POST['matricula']
            senha = request.POST['senha']
            confirma_senha = request.POST['confirma_senha']
            tipo = request.POST['tipo_usuario']

            #Tratamento
            usuario = usuario.lower()

            #Validações
            if senha != confirma_senha:
                messages.error(request, "Senhas não combinam!")
                return redirect('/usuario_lista/')

            #Cadastro
            try:
                user = User.objects.create_user(first_name=nome, last_name=sobrenome, username=usuario, password=senha)
            except:
                messages.error(request, "Usuário já cadastrado!")
                return redirect('/usuario_lista/')

            user.profile.matricula = matricula
            user.profile.tema = 'C'
            user.save()

            #Determinando adminstradores
            if tipo == "administrador":
                user.is_staff = True
                user.save()

            return redirect('/usuario_lista/')

    else:
        messages.error(request, "Permissão Negada!")
        return redirect('/usuario_lista/')

    return render(request, template_name, {})


@login_required
def usuario_delete(request, pk, template_name='usuario_delete.html'):
    user = request.user
    try:
        usuario = User.objects.get(pk=pk)
    except:
        messages.error(request, "Usuário não encontrado!")
        return redirect('/usuario_lista/')

    if user.is_superuser:
        if request.method == "POST":
            usuario.delete()
            return redirect('usuario_lista')
    else:
        messages.error(request, "Permissão Negada!")
        return redirect('/usuario_lista/')

    return render(request, template_name, {'usuario':usuario})


@login_required
def usuario_lista(request, template_name="usuario_lista.html"):
    usuarios = User.objects.all()
    usuario = {'lista': usuarios}
    return render(request, template_name, usuario)


@login_required
def usuario_configuracao(request, template_name='usuario_configuracao.html'):
    if request.method == "POST":
        usuario = request.user
        tema = request.POST['tema']
        usuario.profile.tema = tema
        usuario.save()
    return render(request, template_name)


def efetuar_login(request, template_name="login.html"):
    next = request.GET.get('next', '/usuario_lista/')
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        username = username.lower()

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(next)
        else:
            messages.error(request, 'Usuário ou senha incorretos.')
            return HttpResponseRedirect(settings.LOGIN_URL)

    return render(request, template_name, {'redirect_to': next})


def efetuar_logout(request):
    logout(request)
    return HttpResponseRedirect(settings.LOGIN_URL)