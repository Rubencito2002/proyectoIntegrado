from django import forms
from .models import *

class ProductsFilterForms(forms.ModelForm):
    categoria = forms.ModelChoiceField(queryset=Categoria.objects.all(), empty_label='Todas las categorias', required=False)
    
    class Meta:
        model = Producto
        fields = ['categoria']

class PedidoForm(forms.ModelForm):
    cantidad_pedida = forms.IntegerField(min_value=1)

    class Meta:
        model = Pedido
        fields = ['cantidad_pedida', 'proveedor']