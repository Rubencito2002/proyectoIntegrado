from django.urls import path
from . import views
from .views import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
    # Generales.
    # path('', views.welcome, name='welcome'),

    # Productos.
    path('', ListProducts.as_view(), name='listProducts'),
    path('products/details/<int:pk>/', DetailsProducts.as_view(), name='details_productsComprar'),
    path('listSupermercado/', ListProductsSuperMarket.as_view(), name='listSuperMarket'),
    path('listInformatica/', ListProductsInformatica.as_view(), name='listInformatica'),
    path('listModa/', ListProductsModa.as_view(), name='listModa'),
    path('favoritos/<int:producto_id>/', AñadirFavorito.as_view(), name='añadirFavorito'),

    # Compra de Producto.
    path('procesarCompra/', views.procesarCompra, name='procesarCompra'),
    path('confirmarCompra/', views.confirmarCompra, name='confirmarCompra'),

    # Valoraciones.
    path('valoracion/<int:pk>/', login_required(views.agregarValoracion), name='agregarValoracion'),
    path('valoracion/update/<int:pk>/', login_required(UpdateValoracion.as_view()), name='updateValoracion'),
]