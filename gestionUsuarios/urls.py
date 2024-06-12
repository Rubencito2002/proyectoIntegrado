from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/user/', views.register_user, name='register_user'),
    path('success/', views.success, name='success'),
    path('perfil/', Perfil.as_view(), name='perfil'),
    path('update_password/', ActualizarContraseña.as_view(), name='update_password'),
    path('perfil/editar/empleado/', UpdateUsuarioEmpleado.as_view(), name='editar_perfil_empleado'),
    path('perfil/editar/cliente/', UpdateUsuarioCliente.as_view(), name='editar_perfil_cliente'),
    path('delete/<int:pk>/', DeleteUsuario.as_view(), name='eliminar'),
]