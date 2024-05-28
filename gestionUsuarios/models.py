from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_empleado = models.BooleanField(default=False)
    is_cliente = models.BooleanField(default=False)

    def __str__(self):
        return self.username
    
# Modelos de datos para la gestion de usuarios.
class Cargo(models.Model):
    nombre = models.CharField(max_length=100)
    salario = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.nombre

class Empleado(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    dni = models.CharField(max_length=20)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    cargo = models.ForeignKey(Cargo, on_delete=models.Model, blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    def __str__(self):
        return self.user.username

class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dni = models.CharField(max_length=20)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    tipo_pago = models.CharField(max_length=20, blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    def __str__(self):
        return self.user.username