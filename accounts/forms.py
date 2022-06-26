"""
Exportado de Modulos
"""
from django.forms import ModelForm
from accounts.models import User
from django.contrib.auth.forms import UserCreationForm

""" Creacion del formulario de registro de usuarios utilizando los modelos utilizando la clase Meta """
class registerForm(UserCreationForm, ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'user_type', 'email', 'first_name', 'last_name','address', 'city', 'country', 'cp', 'personal_id', 'fiscal_id', 'contact') #Aqui se pueden pasar los campos especificos Ej: 'username', 'password', etc"

""" Creacion del formulario de Inicio de Sesion """
class loginForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')