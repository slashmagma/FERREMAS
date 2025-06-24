from django.forms import ModelForm, ValidationError
from .models import Categoria, articulo
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CategoriaForm(ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombrecat', 'descripcion', 'imagen']
        
class ArticuloForm(ModelForm):
    class Meta:
        model = articulo
        fields = ['nombreart', 'descripcion', 'imagen', 'valorunidad', 'cantidad']

class CustomAuthenticationForm(AuthenticationForm):

    username = forms.CharField(
        label="Nombre de usuario",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa tu usuario'})
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa tu contraseña'})
    )

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        label="Nombre de usuario",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario'})
    )
    email = forms.EmailField(
        label="Correo electrónico",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'correo@ejemplo.com'})
    )
    password1 = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'})
    )
    password2 = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmar contraseña'})
    )
    def __init__(self, *args, **kwargs):
        self.request_user = kwargs.pop('request_user', None)  # obtenemos el usuario que hace el registro
        super().__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if email.endswith('@gmail.com'):
            return email

        # Si el email NO es gmail.com, validamos si quien crea es superusuario
        if not self.request_user or not self.request_user.is_superuser:
            raise forms.ValidationError("Solo un superusuario puede registrar correos personalizados (@admin, @empresa, etc.).")

        if email.endswith('@admin.com') or email.endswith('@bodegero.com'):
            return email
        if email.endswith('@admin.com'):
            user = User(username=self.cleaned_data['username'], email=email)
            user.set_password(self.cleaned_data['password1'])
            user.is_superuser = True
            user.is_staff = True
            user.save()
            return user
            
        raise forms.ValidationError(
        "El correo personalizado debe terminar en @admin.com o @bodegero.com."
    )  
    class Meta:
        model = User
        fields = ["username","email", "password1", "password2"]