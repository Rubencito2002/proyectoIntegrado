from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def administrador_sistema(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Verificar si el usuario está autenticado y es un empleado con los cargos necesario
        if request.user.is_authenticated and hasattr(request.user, 'Administrador del Sistema') or request.user.is_staff or request.user.is_superuser:
            # Si es un empleado con el cargo, ejecutar la vista normalmente
            return view_func(request, *args, **kwargs)
        else:
            # Si no es un empleado con el cargo, redirigir a la pagina de login
            return redirect('login')
    return _wrapped_view

def gerente_compras(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Verificar si el usuario está autenticado y es un empleado con los cargos necesario
        if request.user.is_authenticated and hasattr(request.user, 'Gerente de Compras') or request.user.is_staff or request.user.is_superuser:
            # Si es un empleado con el cargo, ejecutar la vista normalmente
            return view_func(request, *args, **kwargs)
        else:
            # Si no es un empleado con el cargo, redirigir a la pagina de login
            return redirect('login')
    return _wrapped_view

def analista_datos(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Verificar si el usuario está autenticado y es un empleado con los cargos necesario
        if request.user.is_authenticated and hasattr(request.user, 'Analista de Datos') or request.user.is_staff or request.user.is_superuser:
            # Si es un empleado con el cargo, ejecutar la vista normalmente
            return view_func(request, *args, **kwargs)
        else:
            # Si no es un empleado con el cargo, redirigir a la pagina de login
            return redirect('login')
    return _wrapped_view