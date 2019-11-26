from django.contrib.auth.models import User
from django.shortcuts import render, redirect


# Create your views here.
def usuario_cadastro(request, template_name="usuario_cadastro.html"):
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

    return render(request, template_name, {})

def usuario_lista(request, template_name="usuario_lista.html"):
    usuarios = User.objects.all()
    usuario = {'lista': usuarios}
    return render(request, template_name, usuario)
