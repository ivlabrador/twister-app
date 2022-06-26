from django.urls import path
from . import views
# URL de nuestra app ACCOUNTS
urlpatterns = [
    path('create-user/', views.create_user, name='create_user'), #Formulario de registro
    path('login-user/', views.login_user, name='login_user'), #Formulario de ingreso
    path('logout-user/', views.logout_user, name='logout_user'), #Logout
    path('my-profile/', views.show_profile, name='my_profile'), #Mi perfil
]