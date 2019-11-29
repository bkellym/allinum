import datetime

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.forms import ModelForm
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now

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

            user = User.objects.create_user(username=usuario, password=senha, first_name=nome, last_name=sobrenome)

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
def usuario_editar(request, pk, template_name='usuario_editar.html'):
    user = request.user
    try:
        usuario = User.objects.get(pk=pk)
    except:
        messages.error(request, "Usuário não encontrado!")
        return redirect('/projeto_lista/')

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
    form = ProjetoForm(request.POST or None)
    if form.is_valid():
        form.save()
        projeto = form.instance
        projeto.membros.add(user.membro)
        projeto.ult_alt = user.username
        projeto.data_ult_alt = date.today()
        projeto.save()

        # Redirecionamento
        return redirect('/projeto_lista/')
    return render(request, template_name, {'membro_list':membro})

@login_required
def projeto_editar(request, pk, template_name="projeto_editar.html"):
    user = request.user
    projeto = get_object_or_404(Projeto, pk=pk)
    membro = Membro.objects.all()
    if user.id == projeto.lider.id or user.is_superuser:
        if request.method == "POST":
            form = ProjetoForm(request.POST, instance=projeto)
            if form.is_valid():
                projeto.ult_alt = user.username  # Salva ultima pessoa que alterou o projeto
                projeto.data_ult_alt = date.today()
                projeto.save()
                return redirect('/projeto_lista/')
        else:
            form = projeto
    else:
        messages.error(request, "Permissão Negada!")
        return redirect('/projeto_lista/')
    return render(request, template_name, {'projeto': form, 'membro_list':membro})

@login_required
def projeto_delete(request, pk, template_name='projeto_delete.html'):
    user = request.user
    try:
        projeto = Projeto.objects.get(pk=pk)
    except:
        messages.error(request, "Projeto não encontrado!")
        return redirect('/projeto_lista/')

    if projeto.lider == user or user.is_superuser:
        if request.method == "POST":
            projeto.delete()
            return redirect('projeto_lista')
    else:
        messages.error(request, "Permissão Negada!")
        return redirect('/projeto_lista/')

    return render(request, template_name, {'projeto':projeto})


@login_required
def projeto_lista(request, template_name="projeto_lista.html"):
    user = request.user
    if user.is_superuser:
        projetos = Projeto.objects.all()
    else:
        projetos = Projeto.objects.filter(membros__user_id=user.id)
    context = {"context": projetos}
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

    membro = projeto.membros.all()
    categoria = Categoria.objects.all()
    # Recebe formulário e transforma em um objeto
    tarefa = TarefaForm(request.POST or None)
    if tarefa.is_valid():
        tarefa.save()

        # Redirecionamento
        return redirect('/visao_projeto/' + pk)
    context = {'form': tarefa, 'membro_list':membro, 'categoria_list':categoria, 'projeto':projeto}
    return render(request, template_name, context)


@login_required
def tarefa_editar(request, pk, template_name="tarefa_editar.html"):
    tarefa = get_object_or_404(Tarefa, pk=pk)
    try:
        projeto = Projeto.objects.get(pk=tarefa.projeto.pk)
    except:
        messages.error(request, "Projeto não encontrado!")
        return redirect('/projeto_lista/')

    membro = projeto.membros.all()
    categoria = Categoria.objects.all()

    if request.method == "POST":
        form = TarefaForm(request.POST, instance=tarefa)
        if form.is_valid():
            tarefa.save()
            return redirect('/visao_projeto/' + projeto.id.__str__())

    context = {'membro_list': membro, 'categoria_list': categoria, 'projeto': projeto, 'tarefa':tarefa}
    return render(request, template_name, context)

@login_required
def tarefa_delete(request, pk, projeto_pk, template_name='projeto_delete.html'):
    try:
        tarefa = Tarefa.objects.get(pk=pk)
    except:
        messages.error(request, "Tarefa não encontrada!")
        return redirect('/visao_projeto/' + projeto_pk)

    if request.method == "POST":
            tarefa.delete()
            return redirect('/visao_projeto/' + projeto_pk)

    return render(request, template_name, {'projeto':tarefa})

@login_required
def projeto_visao(request, pk, template_name="visao_projeto.html"):
    tarefas = Tarefa.objects.filter(projeto_id=pk)
    categoria = Categoria.objects.all()

    try:
        projeto = Projeto.objects.get(pk=pk)
    except:
        messages.error(request, "Projeto não encontrado!")
        return redirect('/projeto_lista/')

    context = {'projeto': projeto, 'tarefas': tarefas, 'categorias': categoria, 'template': "visao_projeto"}
    return render(request, template_name, context)

@login_required
def tarefas_do_usuario_projeto(request, pk, template_name="visao_projeto.html"):
    tarefas = Tarefa.objects.filter(Q(resp=request.user.membro.id) & Q(projeto_id=pk))
    categoria = Categoria.objects.all()
    try:
        projeto = Projeto.objects.get(pk=pk)
    except:
        messages.error(request, "Projeto não encontrado!")
        return redirect('/projeto_lista/')

    context = {'projeto': projeto, 'tarefas': tarefas, 'categorias': categoria, 'template': "visao_projeto_tarefa"}
    return render(request, template_name, context)

@login_required
def tarefa_visao(request, template_name="visao_tarefas.html"):
    user = request.user
    if user.is_superuser:
        projetos = Projeto.objects.all()
    else:
        projetos = Projeto.objects.filter(membros__user_id=user.id)

    tarefas = Tarefa.objects.all()
    categorias = Categoria.objects.all()

    context = {"projetos": projetos, "tarefas":tarefas, "categorias":categorias}
    return render(request, template_name, context)