from django import forms
from .models import *
from almacenApp.models import *

class ProductsFilterForms(forms.ModelForm):
    nombre = forms.CharField(label='Nombre', required=False)
    categoria = forms.ModelChoiceField(queryset=Categoria.objects.all(), label='Todas las categorias', required=False)
    precio_min = forms.DecimalField(label='Precio mínimo', required=False)
    precio_max = forms.DecimalField(label='Precio máximo', required=False)
    
    class Meta:
        model = Producto
        fields = ['nombre', 'categoria', 'precio_min', 'precio_max']

class ValoracionForms(forms.ModelForm):
    valoracion = forms.ChoiceField(choices=Valoracion.VALORACIONES, widget=forms.Select(attrs={'class':'form-select'}))
    
    class Meta:
        model = Valoracion
        fields = ['valoracion', 'comentario']

class DatosEnvioForms(forms.ModelForm):
    direccion = forms.CharField(max_length=255)
    ciudad = forms.CharField(max_length=100)
    pais = forms.CharField(max_length=100)
    codigo_postal = forms.CharField(max_length=20)

    class Meta:
        model = DatosEnvio
        fields = ['direccion', 'ciudad', 'pais', 'codigo_postal']