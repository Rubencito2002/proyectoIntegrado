from django.urls import path
from . import views
from .views import *
from .decorators import *

urlpatterns = [
    # Generales.
    path('', views.welcome, name='almacen'),
    # Gestion de Productos.
    path('productos/', ListProducts.as_view(), name='listado_products'),
    path('productos/created/', administrador_sistema(CreatedProducts.as_view()), name='created_products'),
    path('productos/details/<int:pk>/', DetailsProducts.as_view(), name='details_products'),
    path('productos/update/<int:pk>/', administrador_sistema(UpdateProducts.as_view()), name='update_products'),
    path('productos/delete/<int:pk>/', administrador_sistema(DeleteProducts.as_view()), name='delete_products'),
    # Gestion de Categorias.
    path('categoria/created/', administrador_sistema(CreatedCategorias.as_view()), name='created_categoria'),
    path('categoria/update/<int:pk>/', administrador_sistema(UpdateCategoria.as_view()), name='update_categoria'),
    path('categoria/delete/<int:pk>/', administrador_sistema(DeleteCategoria.as_view()), name='delete_categoria'),
    # Gestion de Marca.
    path('marca/created/', administrador_sistema(CreatedMarca.as_view()), name='created_marca'),
    path('marca/update/<int:pk>/', administrador_sistema(UpdateMarca.as_view()), name='update_marca'),
    path('marca/delete/<int:pk>/', administrador_sistema(DeleteMarca.as_view()), name='delete_marca'),
    # Gestion de Marcas y Categoria.
    path('listadoMarcaYCategoria/', ListMarcaYCategoria.as_view(), name='listadoMarcaYCategoria'),
    # Gestion de Pedidos.
    path('pedidos/', ListProductsPeds.as_view(), name='listProductsPeds'),
    path('pedidos/solicitar/<int:pk>/', RealizarPeds.as_view(), name='realizar_pedido'),
    path('pedidos/confirmar/<int:pk>/', ConfirmarPeds.as_view(), name='confirmar_pedido'),
    # Gestion de Proveedor.
    path('proveedor/', ListProveedor.as_view(), name='listProveedor'),
    path('proveedor/created/', administrador_sistema(CreatedProveedor.as_view()), name='created_proveedor'),
    path('proveedor/update/<int:pk>/', administrador_sistema(UpdateProveedor.as_view()), name='update_proveedor'),
    path('proveedor/delete/<int:pk>/', administrador_sistema(DeleteProveedor.as_view()), name='delete_proveedor'),
    # Informes.
    path('informes/informePedido/', informePedido.as_view(), name='informePedido'),
    path('descargarInformeUsuario/', descargarInformeUsuario, name='descargarInformePedido'),
    path('informes/productoMásPeds/', informeProdsMasPeds.as_view(), name='informeProdsMasPeds'),
    path('descargarInformeProdsMasPeds/', descargarInformeProdsMasPeds, name='descargarInformeProdsMasPeds'),
    path('informes/usuarioActivo/', informeUsuarioActivo.as_view(), name='informeUsuarioActivo'),
    path('descargarInformeUsuario/', descargarInformeUsuario, name='descargarInformeUsuario'),
]