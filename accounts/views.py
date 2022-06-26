"""
Exportado de Modulos
"""
from django.shortcuts import render, redirect
from .models import User # Modelo de Usuario
from .forms import registerForm # Formulario de Registro de Usuario
from django.contrib.auth import authenticate, login, logout # Autenticaciones
from sales.models import Wallet # Modulo Wallet -  Para instanciar una billetera al crear un usuario nuevo
from stock.models import Stock # Modulo Stock - Para hacer la comprobacion de falta de stock y dejar el mensaje al proveedor
from django.contrib import messages # Mensaje Flash
"""
create_user: Primeramente comprueba que el usuario no este ya autenticado.
Caso contratio, instancia en nuestra pantalla el formulario de creacion de usuario.
De recibir el formulario por POST verifica que el mismo sea valido para instanciar un nuevo Usuario
"""
def create_user(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        register_form = registerForm
        if request.method == 'POST':
            register_form = registerForm(request.POST)
            if register_form.is_valid():
                register_form.save()
                messages.success(request, 'Te has regisrado correctamente!')
                # Para instanciar automaticamente la billetera cuando el usuario es creado
                # Se solicita a la base de datos el ultimo registro
                last_register = User.objects.last()
                user_id = last_register.id
                wallet = Wallet(user_id=user_id)
                wallet.save()
                return redirect('login_user')
            else:
                messages.warning(request, "Hay errores en el formulario!")
        return render(request, 'create_user.html', {'form': register_form})

"""
login_user: Funcion de Log-in
"""
def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            my_id = request.user.id
            stock = Stock.objects.filter(proveedor_id=my_id).all()
            messages.success(request, f'Bienvenido {username}!')
            for s in stock:
                if s.alert_stock():
                    messages.warning(request, f'Alerta producto en falta: {s.product.name}')
                else:
                    pass
            return redirect('home')
        else:
            messages.warning(request, 'Error en el Login prueba nuevamente')
            return redirect('login_user')
    else:
        return render(request, 'login.html', {})

"""
logout_user: Funcion de Log-out
"""
def logout_user(request):
    logout(request)
    return redirect('login_user')

"""
show_profile: Muestra por pantalla nuestra info de usuario
"""
def show_profile(request):
    if request.user.is_authenticated:
        show_user = User.objects.get(pk=request.user.id)
        profile_form = registerForm(request.POST or None, instance=show_user)
        return render(request, 'profile.html', {
            'user': show_user,
            'form': profile_form
        }
        )