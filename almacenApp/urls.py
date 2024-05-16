from django.urls import path
from . import views
from .views import *

urlpatterns = [
    # Generales.
    path('', views.welcome, name='almacen'),
    # Gestion de Productos.
    path('productos/', ListProducts.as_view(), name='listado_products'),
    path('productos/created/', CreatedProducts.as_view(), name='created_products'),
    path('productos/details/<int:pk>/', DetailsProducts.as_view(), name='details_products'),
    path('productos/update/<int:pk>/', UpdateProducts.as_view(), name='update_products'),
    path('productos/delete/<int:pk>/', DeleteProducts.as_view(), name='delete_products'),
    # Gestion de Categorias.
    path('categoria/created/', CreatedCategorias.as_view(), name='created_categoria'),
    path('categoria/update/<int:pk>/', UpdateCategoria.as_view(), name='update_categoria'),
    path('categoria/delete/<int:pk>/', DeleteCategoria.as_view(), name='delete_categoria'),
    # Gestion de Marca.
    path('marca/created/', CreatedMarca.as_view(), name='created_marca'),
    path('marca/update/<int:pk>/', UpdateMarca.as_view(), name='update_marca'),
    path('marca/delete/<int:pk>/', DeleteMarca.as_view(), name='delete_marca'),
    # Gestion de Marcas y Categoria.
    path('listadoMarcaYCategoria/', ListMarcaYCategoria.as_view(), name='listadoMarcaYCategoria'),
    # Gestion de Pedidos.
    path('pedidos/', ListProductsPeds.as_view(), name='listProductsPeds'),
    path('pedidos/solicitar/<int:pk>/', RealizarPeds.as_view(), name='realizar_pedido'),
    path('pedidos/confirmar/<int:pk>/', ConfirmarPeds.as_view(), name='confirmar_pedido'),
    # Gestion de Proveedor.
    path('proveedor/', ListProveedor.as_view(), name='listProveedor'),
    path('proveedor/created/', CreatedProveedor.as_view(), name='created_proveedor'),
    path('proveedor/update/<int:pk>/', UpdateProveedor.as_view(), name='update_proveedor'),
    path('proveedor/delete/<int:pk>/', DeleteProveedor.as_view(), name='delete_proveedor'),
    # Informes.
    path('informes/', views.informes, name='informes'),
    path('informes/informePedido/', informePedido.as_view(), name='informePedido'),
    path('informes/productoMásPeds/', informeProdsMasPeds.as_view(), name='informeProdsMasPeds'),

]