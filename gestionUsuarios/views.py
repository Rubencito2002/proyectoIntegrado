from typing import Any
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .forms import *
from .models import *
from almacenApp.models import *
from tiendaApp.models import *
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth.views import PasswordChangeView

def register_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_empleado = form.cleaned_data.get('user_type') == 'empleado'
            user.is_cliente = form.cleaned_data.get('user_type') == 'cliente'
            user.save()

            avatar = form.cleaned_data.get('profile_image')

            if user.is_empleado:
                # Guardar datos adicionales de empleado
                dni = form.cleaned_data.get('dni')
                direccion = form.cleaned_data.get('direccion')
                telefono = form.cleaned_data.get('telefono')
                cargo = form.cleaned_data.get('cargo')
                Empleado.objects.create(user=user, dni=dni, direccion=direccion, telefono=telefono, cargo=cargo, profile_image=avatar)
            elif user.is_cliente:
                # Guardar datos adicionales de cliente
                dni = form.cleaned_data.get('dni')
                direccion = form.cleaned_data.get('direccion')
                telefono = form.cleaned_data.get('telefono')
                tipo_pago = form.cleaned_data.get('tipo_pago')
                Cliente.objects.create(user=user, dni=dni, direccion=direccion, telefono=telefono, tipo_pago=tipo_pago, profile_image=avatar)
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
            return render(request, 'gestionUsuarios/login/login.html', {'error': 'Invalid credentials'})
    return render(request, 'gestionUsuarios/login/login.html')

def logout_view(request):
    logout(request)
    return redirect('/')  # Redirige a la página de inicio de sesión después de cerrar sesión

# Vista para mostrar los datos de perfil de los usuarios.
class Perfil(DetailView):
    model = User
    template_name = 'gestionUsuarios/perfil/perfil.html'
    context_object_name = 'user'

    def get_object(self):
        user = self.request.user
        if hasattr(user, 'empleado'):
            return get_object_or_404(Empleado, user=user)
        elif hasattr(user, 'cliente'):
            return get_object_or_404(Cliente, user=user)
        return user

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if hasattr(user, 'empleado'):
            context['empleado'] = user.empleado
            context['pedidos'] = Pedido.objects.filter(usuario=user)
        elif hasattr(user, 'cliente'):
            context['cliente'] = user.cliente
            context['compras'] = OrdenCompraProducto.objects.filter(usuario=user)
            context['valoraciones'] = Valoracion.objects.filter(usuario=user)
            context['favorito'] = Favorito.objects.filter(usuario=user)

        return context
    
# Vista para poder cambiar la contraseña actual del usuario.
class ActualizarContraseña(PasswordChangeView):
    model = User
    template_name = 'gestionUsuarios/perfil/update_password.html'
    success_url = reverse_lazy('perfil')

# Vista para cambiar datos del usuario.
class UpdateUsuarioEmpleado(UpdateView):
    model = Empleado
    form_class = EmpleadoForm
    template_name = 'gestionUsuarios/perfil/editar_perfil.html'
    success_url = reverse_lazy('perfil')

    def get_object(self):
        return get_object_or_404(Empleado, user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_form'] = UserForm(instance=self.request.user)
        return context

    def form_valid(self, form):
        user_form = UserForm(self.request.POST, instance=self.request.user)
        if user_form.is_valid():
            user_form.save()
        else:
            return self.form_invalid(form)
        return super().form_valid(form)
    
class UpdateUsuarioCliente(UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'mi_aplicacion/editar_perfil.html'
    success_url = reverse_lazy('perfil')

    def get_object(self):
        return get_object_or_404(Cliente, user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_form'] = UserForm(instance=self.request.user)
        return context

    def form_valid(self, form):
        user_form = UserForm(self.request.POST, instance=self.request.user)
        if user_form.is_valid():
            user_form.save()
        else:
            return self.form_invalid(form)
        return super().form_valid(form)

# Vista para eliminar un usuario.
class DeleteUsuario(DeleteView):
    model = User
    template_name = 'gestionUsuarios/perfil/delete_perfil.html'
    success_url = reverse_lazy('welcome')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Usuario'  # Puedes personalizar el título según tus necesidades
        return context