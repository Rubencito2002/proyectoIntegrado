from django.db import models
from django.contrib.auth.models import AbstractUser
from gestionUsuario.models import *
# Modelos de datos para la gestion de usuarios.
# class Empleados(AbstractUser):
#     dni = models.CharField(max_length=20)
#     direccion = models.CharField(max_length=255, blank=True, null=True)
#     telefono = models.CharField(max_length=20, blank=True, null=True)

#     def __str__(self):
#         return self.username

# Modelo de datos para organizar los productos en diferentes grupos. Para más adelante pensar que cada producto tiene una subcategoria.
class Categoria(models.Model):
    nombre = models.CharField(max_length=100, null=True, blank=True)
    
    def __str__(self):
        return self.nombre
    
# Modelo de datos para almacenar los datos de las marcas de los productos.
class Marca(models.Model):
    nombre = models.CharField(max_length=100, null=True, blank=True)
    
    def __str__(self):
        return self.nombre
    
# Modelo de datos donde se almacena los datos de cada producto.
class Producto(models.Model):
    DISPONIBILIDAD = (
        ('disponible', 'DISPONIBLE'),
        ('pedido', 'SIN STOCK'),
    )

    nombre = models.CharField(max_length=100, null=True, blank=True)
    descripcion = models.TextField()
    muestra = models.ImageField(upload_to='productos/', null=True, blank=True)
    precio = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    estado = models.CharField(max_length=20, choices=DISPONIBILIDAD, default='disponible')
    cantidad = models.IntegerField(default=0, null=True, blank=True)
    fecha_entrada = models.DateTimeField(auto_now_add=True)
    categoria = models.ManyToManyField(Categoria)
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE, null=True, blank=True)
    limite_cant = 5

    def __str__(self):
        return self.nombre    

# Modelo de datos para la realizacion de Pedidos para abastecer los productos del comercio.
class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    logo = models.ImageField(upload_to='proveedor/', null=True, blank=True)

    def __str__(self):
        return self.nombre

class Pedido(models.Model):
    DISPONIBILIDAD = (
        ('pedido', 'PEDIDO'),
        ('finalizado', 'FINALIZADO'),
    )

    cantidad_pedida = models.IntegerField(default=0)
    fecha_pedida = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=DISPONIBILIDAD, default='pedido')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return f"Pedido {self.producto.nombre} a {self.usuario}"