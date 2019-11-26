from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect


# Create your views here.

@login_required
def usuario_cadastro(request, template_name="usuario_cadastro.html"):
    user = request.user

    if user.is_staff:
        if request.method == "POST":
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            tipo = request.POST['tipo_usuario']

            user = User.objects.create_user(username, email, password)
            if tipo == "administrador":
                user.is_staff = True
                user.save()

            return redirect('/usuario_lista/')
    else:
        return HttpResponse("Permissão Negada!")

    return render(request, template_name, {})


@login_required
def usuario_delete(request, pk, template_name='usuario_delete.html'):
    user = request.user

    try:
        usuario = User.objects.get(pk=pk)
    except:
        return HttpResponse("Usuário não encontrado!")

    if user.has_perm('user.delete_user'):
        if request.method == "POST":
            usuario.delete()
            return redirect('usuario_lista')
    else:
        return HttpResponse("Permissão Negada!")

    return render(request, template_name, {'usuario':usuario})


@login_required
def usuario_lista(request, template_name="usuario_lista.html"):
    usuarios = User.objects.all()
    usuario = {'lista': usuarios}
    return render(request, template_name, usuario)


def efetuar_login(request, template_name="login.html"):
    next = request.GET.get('next', '/usuario_lista/')
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(next)
        else:
            return HttpResponseRedirect(settings.LOGIN_URL)

    return render(request, template_name, {'redirect_to': next})


def efetuar_logout(request):
    logout(request)
    return HttpResponseRedirect(settings.LOGIN_URL)