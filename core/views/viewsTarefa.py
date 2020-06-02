from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import ModelForm
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.datetime_safe import date

from core.models import *


class TarefaForm(ModelForm):
    class Meta:
        model = Tarefa
        fields = ['titulo', 'resp', 'projeto', 'categoria', 'prioridade', 'data_limite']


# noinspection PyShadowingNames
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

        projeto.ult_alt = request.user.username  # Salva ultima pessoa que alterou o projeto
        projeto.data_ult_alt = date.today()
        projeto.save()

        # Redirecionamento
        return redirect('/visao_projeto/' + pk)
    context = {'form': tarefa, 'membro_list': membro, 'categoria_list': categoria, 'projeto': projeto,
               "menu": "projetos"}
    return render(request, template_name, context)


# noinspection PyShadowingNames
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
    data_limite_tratada = tarefa.data_limite.strftime('%Y-%m-%d')

    if request.method == "POST":
        form = TarefaForm(request.POST, instance=tarefa)
        if form.is_valid():
            tarefa.save()

            projeto.ult_alt = request.user.username  # Salva ultima pessoa que alterou o projeto
            projeto.data_ult_alt = date.today()
            projeto.save()

            return redirect('/visao_projeto/' + projeto.id.__str__())

    context = {'membro_list': membro, 'categoria_list': categoria, 'projeto': projeto, 'tarefa': tarefa,
               'data_limite_tratada': data_limite_tratada, "menu": "projetos"}
    return render(request, template_name, context)


# noinspection PyShadowingNames
@login_required
def concluir_tarefa(request, pk):
    try:
        tarefa = Tarefa.objects.get(pk=pk)
    except:
        messages.error(request, "Tarefa não encontrada!")
        return redirect('/projeto_lista/')

    tarefa.concluido = not tarefa.concluido
    tarefa.save()
    return redirect('/visao_projeto/' + tarefa.projeto.id.__str__())


# noinspection PyShadowingNames
@login_required
def tarefa_delete(request):
    if request.method == "POST":
        pk = request.POST['pk']
        projeto_pk = request.POST['projeto']
        try:
            tarefa = Tarefa.objects.get(pk=pk)
        except:
            messages.error(request, "Tarefa não encontrada!")
            return redirect('/visao_projeto/' + projeto_pk)

        if request.method == "POST":
            tarefa.delete()

            projeto = Projeto.objects.get(pk=projeto_pk)
            projeto.ult_alt = request.user.username  # Salva ultima pessoa que alterou o projeto
            projeto.data_ult_alt = date.today()
            projeto.save()

            return redirect('/visao_projeto/' + projeto_pk)


@login_required
def tarefa_visao(request, template_name="visao_tarefas.html"):
    user = request.user
    if user.is_superuser:
        projetos = Projeto.objects.all()
    else:
        projetos = Projeto.objects.filter(membros__user_id=user.id)

    tarefas = Tarefa.objects.all()
    categorias = Categoria.objects.all()

    context = {"projetos": projetos, "tarefas": tarefas, "categorias": categorias, "menu": "tarefas"}
    return render(request, template_name, context)


# noinspection PyShadowingNames
@login_required
def tarefas_do_usuario_projeto(request, pk, template_name="visao_projeto.html"):
    tarefas = Tarefa.objects.filter(Q(resp=request.user.membro.id) & Q(projeto_id=pk))
    categoria = Categoria.objects.all()

    for item in categoria:
        count_total = 0
        count_concluido = 0

        for tarefa in tarefas:
            if item.id == tarefa.categoria.id:
                count_total += 1
                if tarefa.concluido:
                    count_concluido += 1

        if count_total == 0:
            item.porcentagem = -1
        else:
            if count_concluido == 0:
                item.porcentagem = 0
            else:
                percent = 100 * (count_concluido / count_total)
                item.porcentagem = percent

    try:
        projeto = Projeto.objects.get(pk=pk)
    except:
        messages.error(request, "Projeto não encontrado!")
        return redirect('/projeto_lista/')

    context = {'projeto': projeto, 'tarefas': tarefas, 'categorias': categoria, 'template': "visao_projeto_tarefa",
               "menu": "projetos"}
    return render(request, template_name, context)
