from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import ModelForm
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.datetime_safe import date

from core.models import *


class ProjetoForm(ModelForm):
    class Meta:
        model = Projeto
        fields = ['titulo', 'descricao', 'membros', 'lider']


# noinspection PyShadowingNames
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
    return render(request, template_name, {'membro_list': membro, "menu": "projetos"})


# noinspection PyShadowingNames
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
    return render(request, template_name, {'projeto': form, 'membro_list': membro, "menu": "projetos"})


# noinspection PyShadowingNames
@login_required
def projeto_delete(request):
    user = request.user
    if request.method == "POST":
        pk = request.POST['pk']
        try:
            projeto = Projeto.objects.get(pk=pk)
        except:
            messages.error(request, "Projeto não encontrado!")
            return redirect('/projeto_lista/')

        if projeto.lider == user or user.is_superuser:
            projeto.delete()
            return redirect('projeto_lista')
        else:
            messages.error(request, "Permissão Negada!")
            return redirect('/projeto_lista/')


# noinspection PyShadowingNames
@login_required
def projeto_lista(request, template_name="projeto_lista.html"):
    user = request.user
    if user.is_superuser:
        projetos = Projeto.objects.all()
    else:
        projetos = Projeto.objects.filter(membros__user_id=user.id)
    context = {"context": projetos, "menu": "projetos"}
    return render(request, template_name, context)


# noinspection PyShadowingNames
@login_required
def projeto_visao(request, pk, template_name="visao_projeto.html"):
    tarefas = Tarefa.objects.filter(projeto_id=pk)
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

    context = {'projeto': projeto, 'tarefas': tarefas, 'categorias': categoria, 'template': "visao_projeto",
               "menu": "projetos"}
    return render(request, template_name, context)
