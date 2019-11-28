import datetime

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from usuarios.models import *


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


@login_required
def usuario_cadastro(request, template_name="usuario_cadastro.html"):
    user = request.user

    if user.is_staff:
        if request.method == "POST":

            # Recebendo valores do formulário
            nome = request.POST['nome']
            sobrenome = request._post['sobrenome']
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

            # Cadastro
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
        return redirect('/projeto_lista/')

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
        return redirect('/projeto_lista/')

    return render(request, template_name, {'usuario':usuario})


@login_required
def usuario_editar(request, pk, template_name='usuario_editar.html'):
    user = request.user
    usuario = User.objects.get(pk=pk)

    if user.is_staff:
        if request.method=="POST":
            # Recebendo valores do formulário
            nome = request.POST['nome']
            sobrenome = request._post['sobrenome']
            matricula = request.POST['matricula']
            tipo = request.POST['tipo_usuario']

            usuario.first_name=nome
            usuario.last_name=sobrenome
            usuario.profile.matricula=matricula

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

    return render(request, template_name, {'usuario': usuario})


@login_required
def usuario_configuracao(request, template_name='usuario_configuracao.html'):
    if request.method == "POST":
        usuario = request.user
        tema = request.POST['tema']
        usuario.profile.tema = tema
        usuario.save()
    return render(request, template_name)


@login_required
def usuario_lista(request, template_name="usuario_lista.html"):
    if request.user.is_staff:
        usuarios = User.objects.all()
        usuario = {'lista': usuarios}
        return render(request, template_name, usuario)
    else:
        messages.error(request, "Permissão Negada!")
        return redirect('/projeto_lista/')


class ProjetoForm(ModelForm):
    class Meta:
        model = Projeto
        fields = ['titulo', 'descricao', 'membros', 'lider']


@login_required
def projeto_cadastro(request, template_name="projeto_cadastro.html"):
    # Busca usuário logado
    user = request.user
    membro = Membro.objects.all()
    # Recebe formulário e transforma em um objeto
    projeto = ProjetoForm(request.POST or None)
    if projeto.is_valid():
        projeto.lider = user # Define usuário logado como líder do projeto
        projeto.ult_alt = user.username # Salva ultima pessoa que alterou o projeto
        projeto.data_ult_alt = datetime.date.today()
        projeto.save()

        # Redirecionamento
        return redirect('/projeto_lista/')
    return render(request, template_name, {'form': projeto, 'membro_list':membro})

@login_required
def projeto_delete(request, pk, template_name='projeto_delete.html'):
    user = request.user
    try:
        projeto = Projeto.objects.get(pk=pk)
    except:
        messages.error(request, "Projeto não encontrado!")
        return redirect('/projeto_lista/')

    if projeto.lider == user:
        if request.method == "POST":
            projeto.delete()
            return redirect('projeto_lista')
    else:
        messages.error(request, "Permissão Negada!")
        return redirect('/projeto_lista/')

    return render(request, template_name, {'projeto':projeto})


@login_required
def projeto_editar(request, pk, template_name="projeto_editar.html"):
    user = request.user
    try:
        projeto = Projeto.objects.get(pk=pk)
    except:
        messages.error(request, "Projeto não encontrado!")
        return redirect('/projeto_lista/')

    if request.method == "POST":
        # Recebendo valores do formulário
        titulo = request.POST['titulo']
        descricao = request._post['descricao']

        if titulo is None or titulo == "":
            messages.error(request, "Título não pode ser removido!")
            return redirect('/projeto_cadastro/')

        if descricao is None or descricao == "":
            messages.error(request, "Descrição não pode ser removida!")
            return redirect('/projeto_cadastro/')

        projeto.titulo = titulo
        projeto.descricao = descricao
        projeto.save()
        return redirect('/projeto_lista/')


    return render(request, template_name, {'projeto': projeto})


@login_required
def projeto_lista(request, template_name="projeto_lista.html"):
    projetos = Projeto.objects.all()
    context = {"context": projetos}
    return render(request, template_name, context)


@login_required
def projeto_visao(request, pk, template_name="visao_projeto.html"):
    tarefas = Tarefa.objects.filter(projeto_id=pk)
    categoria = Categoria.objects.all()

    try:
        projeto = Projeto.objects.get(pk=pk)
    except:
        messages.error(request, "Projeto não encontrado!")
        return redirect('/projeto_lista/')

    context = {'projeto': projeto, 'tarefas': tarefas, 'categorias': categoria}
    return render(request, template_name, context)


class TarefaForm(ModelForm):
    class Meta:
        model = Tarefa
        fields = ['titulo', 'resp', 'projeto', 'categoria', 'prioridade']


def tarefa_cadastro(request, pk, template_name="tarefa_cadastro.html"):
    try:
        projeto = Projeto.objects.get(pk=pk)
    except:
        messages.error(request, "Projeto não encontrado!")
        return redirect('/projeto_lista/')

    membro = Membro.objects.all()
    categoria = Categoria.objects.all()
    # Recebe formulário e transforma em um objeto
    tarefa = TarefaForm(request.POST or None)
    if tarefa.is_valid():
        tarefa.save()

        # Redirecionamento
        return redirect('/visao_projeto/' + pk)
    context = {'form': tarefa, 'membro_list':membro, 'categoria_list':categoria, 'projeto':projeto}
    return render(request, template_name, context)