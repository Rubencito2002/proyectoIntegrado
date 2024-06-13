from django.db import models
from almacenApp.models import *
from gestionUsuarios.models import *

# Modelos de datos para poder crear las ordenes de compra de los productos.
class DatosEnvio(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    direccion = models.CharField(max_length=255)
    ciudad = models.CharField(max_length=100)
    pais = models.CharField(max_length=100)
    codigo_postal = models.CharField(max_length=20)

    def __str__(self):
        return f"Datos de Envio de {self.usuario.username}"
    
class Forma_Pago(models.Model):
    METODO_PAGO = (
        ('tarjeta', 'Tarjeta de crédito/débito'),
        ('transferencia', 'Transferencia bancaria'),
        ('saldo_cuenta', 'Saldo de cuenta'),
    )

    usuario = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    metodo_pago = models.CharField(max_length=255, choices=METODO_PAGO)

    def __str__(self):
        return f"Datos de Pago de {self.usuario.username} - {self.metodo_pago}"
    
class DetallesTarjeta(models.Model):
    forma_Pago = models.OneToOneField(Forma_Pago, on_delete=models.CASCADE, related_name='detalles_tarjeta')
    num_tarjeta = models.CharField(max_length=16)
    fecha_vencimiento = models.DateField()
    codigo_seguridad = models.CharField(max_length=4)

    def __str__(self):
        return f"Detalles de Tarjeta de {self.forma_Pago.metodo_pago}"

class DetallesPayPal(models.Model):
    forma_Pago = models.OneToOneField(Forma_Pago, on_delete=models.CASCADE, related_name='detalles_paypal')
    correo = models.EmailField()

    def __str__(self):
        return f"Detalles de Tarjeta de {self.forma_Pago.metodo_pago}"
    
class OrdenCompraProducto(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    fecha = models.DateField(auto_now=True, blank=True, null=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()

    def __str__(self):
        return f"{self.producto.nombre} en {self.fecha}"
    
# Modelos de datos futuros.
class Valoracion(models.Model):
    VALORACIONES = (
        (1, '★'),
        (2, '★★'),
        (3, '★★★'),
        (4, '★★★★'),
        (5, '★★★★★')
    )

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    valoracion = models.IntegerField(choices=VALORACIONES, default=0)
    comentario = models.TextField(blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.producto.nombre} - {self.valoracion} estrellas"
    
class Favorito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('usuario', 'producto')

    def __str__(self):
        return f'{self.usuario.username} - {self.producto.nombre}'
