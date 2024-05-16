from typing import Any
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.db.models import Sum
from django.views import View
from django.http import JsonResponse
from .models import *
from .forms import *
from django.views.generic import ListView,DetailView, CreateView, UpdateView, DeleteView

# Vista de página principal del sistema de almacenamiento.
def welcome(request):
    return render(request, 'almacenApp/index.html')

# Vista para crear un nuevo producto.
class CreatedProducts(CreateView):
    model = Producto
    fields = ['nombre', 'descripcion', 'muestra', 'precio', 'cantidad', 'categoria', 'marca']
    template_name = 'almacenApp/productos/created_products.html'
    success_url = reverse_lazy('listado_products')

# Vista para mostrar todos los productos del comercio.
class ListProducts(ListView):
    model = Producto
    template_name = 'almacenApp/listadosGenericos/list_products.html'
    context_object_name = 'productos'
    ordering = 'nombre'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filtro_form'] = ProductsFilterForms(self.request.GET)
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        categoria_seleccionada = self.request.GET.get('categoria')
        if categoria_seleccionada:
            queryset = queryset.filter(categoria=categoria_seleccionada)
        return queryset

class DetailsProducts(DetailView):
    model = Producto
    template_name = 'almacenApp/productos/details_products.html'

# Vista para la actualizacion de los datos de un producto.
class UpdateProducts(UpdateView):
    model = Producto
    fields = ['nombre', 'descripcion', 'muestra', 'precio', 'cantidad', 'categoria', 'marca']
    template_name = 'almacenApp/productos/update_products.html'
    
    #No se puede usar para una url que lo que quiere es la pk del producto.
    # success_url = reverse_lazy('details_products')
    # Para eso tendremos que usar esta funcion para modificar la vuelta para que se pueda pasar la pk del producto para que se redirija
    # bien a la url que queremos ya que esa url necesita la pk.
    def get_success_url(self):
        return reverse_lazy('details_products', kwargs={'pk': self.object.pk})

# Vista para la eliminacion de una categoria.
class DeleteProducts(DeleteView):
    model = Producto
    template_name = 'almacenApp/productos/delete_products.html'
    success_url = reverse_lazy('listado_products')

# Vista para mostrar las marcas y categoria del comercio.
class ListMarcaYCategoria(ListView):
    model = Marca
    template_name = 'almacenApp/listadosGenericos/listMarcaYCategoria.html'

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        # Modificamos el contexto creando dos context para poder mostrar todos los datos de categorias y marcas en una unica plantilla.
        context['categorias'] = Categoria.objects.all()
        context['marcas'] = Marca.objects.all()
        return context

# Vista para la creaccion de las marcas de los productos.
class CreatedMarca(CreateView):
    model = Marca
    fields = ['nombre']
    template_name = 'almacenApp/marca/created_marca.html'
    success_url = reverse_lazy('listado_products')

# Vista para la ediccion de los datos de marca.
class UpdateMarca(UpdateView):
    model = Marca
    fields = ['nombre']
    template_name = 'almacenApp/marca/update_marca.html'
    success_url = reverse_lazy('listado_products')

# Vista para la eliminacion de una marca.
class DeleteMarca(DeleteView):
    model = Marca
    template_name = 'almacenApp/marca/delete_marca.html'
    success_url = reverse_lazy('listado_products')

# Vista para la creaccion de las categorias de los productos.
class CreatedCategorias(CreateView):
    model = Categoria
    fields = ['nombre']
    template_name = 'almacenApp/categoria/created_categoria.html'

# Vista para la ediccion de los datos de categoria.
class UpdateCategoria(UpdateView):
    model = Categoria
    fields = ['nombre']
    template_name = 'almacenApp/categoria/update_categoria.html'
    success_url = reverse_lazy('listado_products')

# Vista para la eliminacion de una categoria.
class DeleteCategoria(DeleteView):
    model = Categoria
    template_name = 'almacenApp/categoria/delete_categoria.html'
    success_url = reverse_lazy('listado_products')

# Vista para el listado de los proveedores.
class ListProveedor(ListView):
    model = Proveedor
    template_name = 'almacenApp/listadosGenericos/listProveedor.html'
    context_object_name = 'proveedor'

# Vista para la creaccion de los proveedores de los productos.
class CreatedProveedor(CreateView):
    model = Proveedor
    fields = ['nombre']
    template_name = 'almacenApp/proveedor/created_proveedor.html'

# Vista para la ediccion de los datos de los proveedores.
class UpdateProveedor(UpdateView):
    model = Proveedor
    fields = ['nombre']
    template_name = 'almacenApp/proveedor/update_proveedor.html'
    success_url = reverse_lazy('listado_products')

# Vista para la eliminacion de un proveedor.
class DeleteProveedor(DeleteView):
    model = Proveedor
    template_name = 'almacenApp/proveedor/delete_proveedor.html'
    success_url = reverse_lazy('listado_products')

# Vista para el listado de los pedidos.
class ListProductsPeds(ListView):
    model = Producto
    template_name = 'almacenApp/listadosGenericos/listProductsPeds.html'
    context_object_name = 'productos'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        # Se modifica el contexto para poder mostrar las cantidades anteriores antes de abastecer los productos con un stock permitido
        context['productos'] = Producto.objects.annotate(cant_anterior=Sum('pedido__cantidad_pedida')).order_by('cantidad')
        return context
    
# Vista para realizar el pedido para abastecer los productos de unidades.
class RealizarPeds(View):
    pedido_template = 'almacenApp/pedidos/solicitarPedido.html'

    def get(self, request, pk):
        producto = get_object_or_404(Producto, pk=pk)
        form = PedidoForm()
        return render(request, self.pedido_template, {'producto': producto, 'form': form})
    
    def post(self, request, pk):
        producto = get_object_or_404(Producto, pk=pk)

        form = PedidoForm(request.POST)
        usuario = request.user

        if form.is_valid():
            proveedor_select = form.cleaned_data['proveedor']
            cant_pedido = form.cleaned_data['cantidad_pedida']

            if cant_pedido > 0:
                # Creaccion de un objecto pedido para almacenar los datos del pedido que se ha creado para los productos.
                pedido = Pedido.objects.create(cantidad_pedida=cant_pedido, producto=producto, usuario=usuario, estado='pedido', proveedor=proveedor_select)
                pedido.save()
                # Cuando se realiza un pedido el estado actual de un producto se cambia el que tiene por defecto.
                producto.estado = 'pedido'
                producto.save()
                return redirect('listProductsPeds')
            else:
                # Si la cantidad de pedido no es valido volvera de nuevo al formulario para que lo vuelvas a rellenar bien la cantidad de producto para ese pedido a realizar.
                return redirect('realizar_pedido', pk=pk)
            
        return render(request, self.pedido_template, {'producto': producto, 'form': form})
        
# Vista para la confirmarción de los pedidos que se ha realizado para poder dar la confirmacion de actualizar los datos del producto del que se ha realizado el pedido.
class ConfirmarPeds(View):
    confirmar_template = 'almacenApp/pedidos/confirmarPedido.html'

    def get(self, request, pk):
        producto = Producto.objects.get(pk=pk)
        # Se busca los datos de un pedido con los datos del producto, estado y del usuario para poder realizar la actualizacion de los datos de los productos.
        pedido_realizado = Pedido.objects.filter(producto=producto, estado='pedido', usuario=request.user).first()

        if pedido_realizado:
            # Si el pedido que se ha buscado se encuentra nos redirigira al formualrio de confirmacion de pedido para realizar las operaciones necesarias.
            return render(request, self.confirmar_template, {'producto': producto, 'pedido': pedido_realizado})
        else:
            # Si no se encuentra ese pedido volvera a la pagina del listado.
            return redirect('listProductsPeds')
    
    def post(self, request, pk):
        producto = Producto.objects.get(pk=pk)
        # Se busca los datos de un pedido con los datos del producto, estado y del usuario para poder realizar la actualizacion de los datos de los productos.
        pedido_realizado = Pedido.objects.filter(producto=producto, estado='pedido', usuario=request.user).first()

        if pedido_realizado:
            # Comprobamos si se el usuario le ha dado al boton de confirmar pedido en el formulario de la plantilla ya que puede darle sin querer al boton de cancelar y no se realiza ninguna operacion con ese pedido.
            if 'confirmar' in request.POST:
                # Como si le ha dado al boton de confirmar pues realizamos el cambio de estado del producto y actualizamos la cantidad de ese producto pero al añadir la cantidad no sobreescribimos con la que ya habia sino se lo sumamos para poder seguir sabiendo que quedaban de ese producto esa cantidad.
                producto.estado = 'disponible'
                producto.cantidad += pedido_realizado.cantidad_pedida 
                producto.save()
                # En el pedido le cambiamos su estado para marcarlo como finalizado ese pedido para que quede contancia que ese pedido ya esta cerrado.
                pedido_realizado.estado = 'finalizado'
                pedido_realizado.save()
                return redirect('listProductsPeds')
            elif 'cancelar' in request.POST:
                # Si el usuario le ha dado al boton de cancelar volveremos a la pagina del listado de los productos para realizar pedido.
                return redirect('listProductsPeds')
        
        return render(request, self.confirmar_template, {'producto': producto, 'pedido': pedido_realizado})
    
# Vista para mostrar todos los informes.
def informes(request):
    return render(request, 'almacenApp/informes/informes.html', {})

# Vista de un informes de los pedidos que se puede filtrar por su estado, por el usuario pedido, por el proveedor.
class informePedido(ListView):
    model = Pedido
    template_name = 'almacenApp/informes/informesPedido.html'
    context_object_name = 'pedidos'

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)

        context['pedidos'] = Pedido.objects.all()
        context['proveedor'] = Proveedor.objects.all()
        # context['usuarios']

        estadoPeds = self.request.GET.get('estadoPeds')
        proveedorPeds = self.request.GET.get('proveedorPeds')
        # usuarioPeds

        pedsFiltrado = Pedido.objects.all()

        if estadoPeds != None and estadoPeds != 'all':
            pedsFiltrado = Pedido.objects.filter(estado = estadoPeds)

        if proveedorPeds != None and proveedorPeds != 'all':
            pedsFiltrado = Pedido.objects.filter(proveedor = proveedorPeds)

        # if usuarioPeds != None and usuarioPeds != 'all':
        #     pedsFiltrado = Pedido.objects.filter(usuario = usuarioPeds)

        pedsFiltrado = pedsFiltrado.order_by('-fecha_pedida')

        context['pedidoFiltrado'] = pedsFiltrado
        return context
    
# Vista de los productos más pedido.
class informeProdsMasPeds(ListView):
    model = Producto
    template_name = 'almacenApp/informes/informeProdsMasPeds.html'
    context_object_name = 'productosMasPeds'

    def get_queryset(self):
        return Producto.objects.annotate(total_pedido=Sum('pedido__cantidad_pedida')).order_by('-total_pedido')
    
# 


# 