from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from functools import wraps

def administrador_sistema(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Verificar si el usuario está autenticado y es un empleado
        if request.user.is_authenticated and hasattr(request.user, 'Administrador del Sistema') or request.user.is_staff or request.user.is_superuser:
            # Si es un empleado, ejecutar la vista normalmente
            return view_func(request, *args, **kwargs)
        else:
            # Si no es un empleado, redirigir a una página de error o a donde desees
            return redirect('inicio_sesion')  # Reemplaza 'pagina_de_error' con la URL de tu página de error
    return _wrapped_view