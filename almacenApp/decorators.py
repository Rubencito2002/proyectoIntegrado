from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def administrador_sistema(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Verificar si el usuario está autenticado y es un empleado con los cargos necesario
        if request.user.is_authenticated:
            # Permitir acceso a usuarios con el cargo asignado.
            if request.user.empleado.cargo.nombre == 'Administrador del Sistema':
                return view_func(request, *args, **kwargs)
            # Permitir acceso a usuarios con permisos de administración
            if request.user.is_staff or request.user.is_superuser:
                return view_func(request, *args, **kwargs)
        else:
            # Si no es un empleado con el cargo, redirigir a la pagina de login
            return redirect('login')
    return _wrapped_view

def gerente_compras(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Verificar si el usuario está autenticado y es un empleado con los cargos necesario
        if request.user.is_authenticated:
            # Permitir acceso a usuarios con el cargo asignado.
            if request.user.empleado.cargo.nombre == 'Gerente de Compras':
                return view_func(request, *args, **kwargs)
            # Permitir acceso a usuarios con permisos de administración
            if request.user.is_staff or request.user.is_superuser:
                return view_func(request, *args, **kwargs)
        else:
            # Si no es un empleado con el cargo, redirigir a la pagina de login
            return redirect('login')
    return _wrapped_view

def analista_datos(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Verificar si el usuario está autenticado y es un empleado con los cargos necesario
        if request.user.is_authenticated:
            # Permitir acceso a usuarios con el cargo asignado.
            if request.user.empleado.cargo.nombre == 'Analista de Datos':
                return view_func(request, *args, **kwargs)
            # Permitir acceso a usuarios con permisos de administración
            if request.user.is_staff or request.user.is_superuser:
                return view_func(request, *args, **kwargs)
        else:
            # Si no es un empleado con el cargo, redirigir a la pagina de login
            return redirect('login')
    return _wrapped_view