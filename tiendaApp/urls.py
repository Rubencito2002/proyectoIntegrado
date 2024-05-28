from django.urls import path
from . import views
from .views import *

urlpatterns = [
    # Generales.
    # path('', views.welcome, name='welcome'),

    # Productos.
    path('', ListProducts.as_view(), name='listProducts'),
    path('products/details/<int:pk>/', DetailsProducts.as_view(), name='details_productsComprar'),
    path('listSupermercado/', ListProductsSuperMarket.as_view(), name='listSuperMarket'),
    path('listInformatica/', ListProductsInformatica.as_view(), name='listInformatica'),
    path('listModa/', ListProductsModa.as_view(), name='listModa'),

    # Compra de Producto.
    path('procesarCompra/', views.procesarCompra, name='procesarCompra'),
    path('confirmarCompra/', views.confirmarCompra, name='confirmarCompra'),

    # Valoraciones.
    path('valoracion/<int:pk>/', views.agregarValoracion, name='agregarValoracion'),
    path('valoracion/update/<int:pk>/', UpdateValoracion.as_view(), name='updateValoracion'),
]