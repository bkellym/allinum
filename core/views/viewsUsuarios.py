from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from core.models import *


@login_required
def usuario_cadastro(request, template_name="usuario_cadastro.html"):
    user = request.user

    if user.is_staff:
        if request.method == "POST":

            # Recebendo valores do formulário
            nome = request.POST['nome']
            sobrenome = request.POST['sobrenome']
            usuario = request.POST['usuario']
            matricula = request.POST['matricula']
            senha = request.POST['senha']
            confirma_senha = request.POST['confirma_senha']
            tipo = request.POST['tipo_usuario']

            # Tratamento
            usuario = usuario.lower()

            # Validações
            if senha != confirma_senha:
                messages.error(request, "Senhas não combinam!")
                return redirect('/usuario_lista/')

            user = User.objects.create_user(username=usuario, password=senha, first_name=nome, last_name=sobrenome)

            user.profile.matricula = matricula
            user.profile.tema = 'C'
            user.save()

            # Determinando adminstradores
            if tipo == "administrador":
                user.is_staff = True
                user.save()

            return redirect('/usuario_lista/')

    else:
        messages.error(request, "Permissão Negada!")
        return redirect('/projeto_lista/')

    return render(request, template_name, {"menu": "configuracoes"})


@login_required
def usuario_editar(request, pk, template_name='usuario_editar.html'):
    user = request.user
    try:
        usuario = User.objects.get(pk=pk)
    except:
        messages.error(request, "Usuário não encontrado!")
        return redirect('/projeto_lista/')

    if user.is_staff:
        if request.method == "POST":
            # Recebendo valores do formulário
            nome = request.POST['nome']
            sobrenome = request.POST['sobrenome']
            matricula = request.POST['matricula']
            tipo = request.POST['tipo_usuario']

            usuario.first_name = nome
            usuario.last_name = sobrenome
            usuario.profile.matricula = matricula

            if tipo == "administrador":
                usuario.is_staff = True
                usuario.save()
            else:
                usuario.is_staff = False
                usuario.save()

            return redirect('/usuario_lista/')
    else:
        messages.error(request, "Permissão Negada!")
        return redirect('/projeto_lista/')

    return render(request, template_name, {'usuario': usuario, "menu": "configuracoes"})


@login_required
def usuario_delete(request):
    user = request.user
    if request.method == "POST":
        pk = request.POST['pk']
        try:
            usuario = User.objects.get(pk=pk)
        except:
            messages.error(request, "Usuário não encontrado!")
            return redirect('/usuario_lista/')

        if user.is_superuser:
            usuario.delete()
            return redirect('usuario_lista')
        else:
            messages.error(request, "Permissão Negada!")
            return redirect('/projeto_lista/')


@login_required
def usuario_configuracao(request, template_name='usuario_configuracao.html'):
    if request.method == "POST":
        usuario = request.user
        tema = request.POST['tema']
        usuario.profile.tema = tema
        usuario.save()
    return render(request, template_name, {"menu": "configuracoes"})


@login_required
def usuario_lista(request, template_name="usuario_lista.html"):
    if request.user.is_staff:
        usuarios = User.objects.all()
        usuario = {'lista': usuarios, "menu": "configuracoes"}
        return render(request, template_name, usuario)
    else:
        messages.error(request, "Permissão Negada!")
        return redirect('/projeto_lista/')
