from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .forms import *
from .models import *

def register_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_empleado = form.cleaned_data.get('user_type') == 'empleado'
            user.is_cliente = form.cleaned_data.get('user_type') == 'cliente'
            user.save()
            if user.is_empleado:
                # Guardar datos adicionales de empleado
                dni = form.cleaned_data.get('dni')
                direccion = form.cleaned_data.get('direccion')
                telefono = form.cleaned_data.get('telefono')
                cargo = form.cleaned_data.get('cargo')
                Empleado.objects.create(user=user, dni=dni, direccion=direccion, telefono=telefono, cargo=cargo)
            elif user.is_cliente:
                # Guardar datos adicionales de cliente
                dni = form.cleaned_data.get('dni')
                direccion = form.cleaned_data.get('direccion')
                telefono = form.cleaned_data.get('telefono')
                tipo_pago = form.cleaned_data.get('tipo_pago')
                Cliente.objects.create(user=user, dni=dni, direccion=direccion, telefono=telefono, tipo_pago=tipo_pago)
            login(request, user)
            return redirect('success')
    else:
        form = CustomUserCreationForm()
    return render(request, 'gestionUsuarios/registroUsuario/register_user.html', {'form': form})

def success(request):
    return render(request, 'gestionUsuarios/registroUsuario/success.html')

def redirect_to_home(request):
    return redirect('/')

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')  # Redirige a la página de inicio después de iniciar sesión
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'gestionUsuarios/login/login.html')

def logout_view(request):
    logout(request)
    return redirect('/')  # Redirige a la página de inicio de sesión después de cerrar sesión

# def signup_view(request):
#     if request.method == "POST":
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('login')  # Redirige a la página de inicio de sesión después de registrarse
#     else:
#         form = UserCreationForm()
#     return render(request, 'signup.html', {'form': form})