from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import ModelForm
from django.shortcuts import redirect, render

from core.models import *


# noinspection PyShadowingNames
class RequisitoForm(ModelForm):
    class Meta:
        model = Requisito
        fields = ['titulo', 'categoria', 'projeto']


# noinspection PyShadowingNames
@login_required
def requisito_cadastro(request):
    form = RequisitoForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('/visao_requisito/' + form.instance.projeto.id.__str__())


# noinspection PyShadowingNames
@login_required
def requisito_delete(request):
    if request.method == "POST":
        pk = request.POST['pk']
        projeto = request.POST['projeto']

        try:
            requisito = Requisito.objects.get(pk=pk)
        except:
            messages.error(request, "Tarefa não encontrada!")
            return redirect('/visao_requisito/' + projeto)

        requisito.delete()
        return redirect('/visao_requisito/' + projeto)


# noinspection PyShadowingNames
@login_required
def visao_requisitos(request, pk, template_name="visao_requisitos.html"):
    try:
        projeto = Projeto.objects.get(pk=pk)
    except:
        messages.error(request, "Projeto não encontrado!")
        return redirect('/projeto_lista/')

    requisitos = Requisito.objects.filter(projeto_id=projeto.pk)

    context = {"projeto": projeto, "requisitos": requisitos, "template": "visao_requisito", "menu": "projetos"}
    return render(request, template_name, context)
