from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *

class CustomUserCreationForm(UserCreationForm):
    # Agregar un campo de selección para el tipo de usuario
    user_type = forms.ChoiceField(choices=[('empleado', 'Empleado'), ('cliente', 'Cliente')])

    # Campos adicionales para empleado
    dni = forms.CharField(max_length=20, required=False)
    direccion = forms.CharField(max_length=255, required=False)
    telefono = forms.CharField(max_length=20, required=False)
    cargo = forms.ModelChoiceField(queryset=Cargo.objects.all(), required=False)

    # Campos adicionales para cliente
    tipo_pago = forms.CharField(max_length=20, required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'user_type', 'dni', 'direccion', 'telefono', 'cargo', 'tipo_pago')

    # Sobreescribir el método save para marcar el tipo de usuario
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_empleado = self.cleaned_data.get('user_type') == 'empleado'
        user.is_cliente = self.cleaned_data.get('user_type') == 'cliente'
        if commit:
            user.save()
            if user.is_empleado:
                # Guardar datos adicionales de empleado
                Empleado.objects.create(user=user, dni=self.cleaned_data.get('dni'), direccion=self.cleaned_data.get('direccion'), telefono=self.cleaned_data.get('telefono'), salario=self.cleaned_data.get('salario'), cargo=self.cleaned_data.get('cargo'))
            elif user.is_cliente:
                # Guardar datos adicionales de cliente
                Cliente.objects.create(user=user, dni=self.cleaned_data.get('dni'), direccion=self.cleaned_data.get('direccion'), telefono=self.cleaned_data.get('telefono'), tipo_pago=self.cleaned_data.get('tipo_pago'))
        return user

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = ['cargo', 'profile_image']

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['direccion', 'telefono', 'profile_image']