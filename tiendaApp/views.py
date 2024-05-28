from typing import Any
from django.db.models.query import QuerySet
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from .models import *
from .forms import *
from almacenApp.models import *
from django.views.generic import ListView, DetailView, UpdateView
from django.http import JsonResponse
import json

# Create your views here.

# # Vista de página principal de la tienda.
# def welcome(request):
#     return render(request, 'tiendaApp/index.html')

# Vista para mostrar todos los productos sin filtrar.
class ListProducts(ListView):
    model = Producto
    template_name = 'tiendaApp/productos/listProducts.html'
    context_object_name = 'productos'
    ordering = 'nombre'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.all()  # Obtener todas las categorías
        context['filter_form'] = ProductsFilterForms(self.request.GET)  # Pasar el formulario de filtro al contexto
        return context
    
    def get_queryset(self):
        queryset = super().get_queryset()

        # Obtener los datos del formulario
        form = ProductsFilterForms(self.request.GET)

        if form.is_valid():
        # Captura de los parametros del filtrado del formulario.
            nombre = form.cleaned_data.get('nombre')
            categoria = form.cleaned_data.get('categoria')
            precio_min = form.cleaned_data.get('precio_min')
            precio_max = form.cleaned_data.get('precio_max')

            # Filtra los productos en base a los parámetros recibidos
            if nombre:
                queryset = queryset.filter(nombre__icontains=nombre)
            if categoria:
                queryset = queryset.filter(categoria=categoria)
            if precio_min:
                queryset = queryset.filter(precio__gte=precio_min)
            if precio_max:
                queryset = queryset.filter(precio__lte=precio_max)

        return queryset

# Vista de los productos de la categoria supermercado.
class ListProductsSuperMarket(ListView):
    model = Producto
    template_name = 'tiendaApp/productos/listProductsMarket.html'
    context_object_name = 'productos'
    ordering = 'nombre'

    def get_queryset(self):
        queryset = super().get_queryset()

        # Captura de los parametros del filtrado del formulario.
        nombre = self.request.GET.get('nombre')
        precio_min = self.request.GET.get('precio_min')
        precio_max = self.request.GET.get('precio_max')

        # Filtra los productos en base a los parámetros recibidos
        if nombre:
            queryset = queryset.filter(nombre__icontains=nombre)
        if precio_min:
            queryset = queryset.filter(precio__gte=precio_min)
        if precio_max:
            queryset = queryset.filter(precio__lte=precio_max)

        return queryset
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['productos'] = Producto.objects.filter(categoria__nombre='Supermercado').order_by('nombre')
        return context

class ListProductsModa(ListView):
    model = Producto
    template_name = 'tiendaApp/productos/listProductsModa.html'
    context_object_name = 'productos'
    ordering = 'nombre'

    def get_queryset(self):
        queryset = super().get_queryset()

        # Captura de los parametros del filtrado del formulario.
        nombre = self.request.GET.get('nombre')
        precio_min = self.request.GET.get('precio_min')
        precio_max = self.request.GET.get('precio_max')

        # Filtra los productos en base a los parámetros recibidos
        if nombre:
            queryset = queryset.filter(nombre__icontains=nombre)
        if precio_min:
            queryset = queryset.filter(precio__gte=precio_min)
        if precio_max:
            queryset = queryset.filter(precio__lte=precio_max)

        return queryset
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['productos'] = Producto.objects.filter(categoria__nombre='Moda').order_by('nombre')
        return context
    
class ListProductsInformatica(ListView):
    model = Producto
    template_name = 'tiendaApp/productos/listProductsInformatica.html'
    context_object_name = 'productos'
    ordering = 'nombre'

    def get_queryset(self):
        queryset = super().get_queryset()

        # Captura de los parametros del filtrado del formulario.
        nombre = self.request.GET.get('nombre')
        precio_min = self.request.GET.get('precio_min')
        precio_max = self.request.GET.get('precio_max')

        # Filtra los productos en base a los parámetros recibidos
        if nombre:
            queryset = queryset.filter(nombre__icontains=nombre)
        if precio_min:
            queryset = queryset.filter(precio__gte=precio_min)
        if precio_max:
            queryset = queryset.filter(precio__lte=precio_max)

        return queryset
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['productos'] = Producto.objects.filter(categoria__nombre='Informática').order_by('nombre')
        return context

class DetailsProducts(DetailView):
    model = Producto
    template_name = 'tiendaApp/productos/details_products.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        producto = self.get_object()
        context['valoraciones'] = Valoracion.objects.filter(producto=producto)
        return context

# Vista para la realizacion de la toma de los datos de envios.
# def datosEnvio(request):
#     total = request.GET.get('total', 0)
#     carrito = request.POST.get('carrito', [])
#     return render(request, 'tiendaApp/compras/datosEnvio.html', {'carrito': carrito, 'total': total})

# # Vista para la realizacion de la toma de los datos de forma de pago.
# def formaPago(request):
#     total = request.GET.get('total', 0)
#     carrito = request.POST.get('carrito', [])
#     return render(request, 'tiendaApp/compras/formaPago.html', {'carrito': carrito, 'total': total})

# Vista para la confirmacion de la compra de los productos.
def confirmarCompra(request):
    total = request.GET.get('total', 0)
    carrito = request.POST.get('carrito', [])
    return render(request, 'tiendaApp/compras/confirmarCompra.html', {'carrito': carrito, 'total': total})

# Vista para procesar la compra de los productos.
def procesarCompra(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        carrito = data.get('carrito')

        # Obtener el usuario actual
        usuario = request.user

        # Obtener los datos de envio y forma de pago.
        datos_envio = data.get('datosEnvio')
        metodo_pago = data.get('formaPago')

        if metodo_pago == 'tarjeta':
            numero_tarjeta = data.get('numero_tarjeta')
            fecha_vencimiento = data.get('fecha_vencimiento')
            codigo_seguridad = data.get('codigo_seguridad')

            if numero_tarjeta and fecha_vencimiento and codigo_seguridad:
                detalles_tarjeta = DetallesTarjeta.objects.create(
                    num_tarjeta = numero_tarjeta,
                    fecha_vencimiento = fecha_vencimiento,
                    codigo_seguridad = codigo_seguridad
                )
            else:
                detalles_tarjeta = None

            detalles_paypal = None
        elif metodo_pago == 'paypal':
            correo_paypal = data.get('correo_paypal')
            
            if correo_paypal:
                detalles_paypal = DetallesPayPal.objects.create(
                    correo = correo_paypal
                )
            else:
                detalles_paypal = None

            detalles_tarjeta = None
        else:
            detalles_tarjeta = None
            detalles_paypal = None

        formaPago = Forma_Pago.objects.create(
            usuario = usuario,
            metodo_pago = metodo_pago
        )

        if detalles_tarjeta:
            detalles_tarjeta.forma_Pago = formaPago
            detalles_tarjeta.save()
        elif detalles_paypal:
            detalles_paypal.forma_Pago = formaPago
            detalles_paypal.save()


        for item in carrito:
            # Cogemos del listado de los productos que estan el carrito y vamos creando un objecto de orden de compra con los datos de ese productos.
            producto = Producto.objects.get(nombre=item['nombre'])
            cantidad_comprada = item['cantidad']
            OrdenCompraProducto.objects.create(producto=producto, cantidad=cantidad_comprada, usuario = usuario)
            # Al producto que se ha creado su orden de compra le restamos la cantidad que se ha comprado para actualizar los datos de ese productos.
            producto.cantidad -= cantidad_comprada
            producto.save()

        datosEnvios = DatosEnvio.objects.create(
            usuario = usuario,
            direccion = datos_envio.get('direccion'),
            ciudad = datos_envio.get('ciudad'),
            pais = datos_envio.get('pais'),
            codigo_postal = datos_envio.get('codigo_postal')
        )


        return JsonResponse({'success': True, 'message': 'Compra realizada con éxito'})
    else:
        # La solicitud no es POST, retornar un error
        return JsonResponse({'success': False, 'message': 'La solicitud debe ser de tipo POST'})
    
# Vista para realizar valoraciones de los productos del comercio.
def agregarValoracion(request, pk):
    if request.method == 'POST':
        form = ValoracionForms(request.POST)
        if form.is_valid():
            valoracion = form.save(commit=False)
            valoracion.usuario = request.user
            valoracion.producto_id = pk
            valoracion.save()
            return redirect('listProducts')
    else:
        form = ValoracionForms()
        return render(request, 'tiendaApp/valoraciones/agregarValoracion.html', {'form':form})
    
# Vista para la modificacion de una valoracion.
class UpdateValoracion(UpdateView):
    model = Valoracion
    fields = ['valoracion', 'comentario']
    template_name = 'tiendaapp/valoraciones/update_valoracion.html'

    def get_success_url(self):
        return reverse_lazy('details_productsComprar', kwargs={'pk': self.object.pk})