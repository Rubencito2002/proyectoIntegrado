from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Cargo)
admin.site.register(Empleado)
admin.site.register(Cliente)