"""
Exportado de Modulos
"""
from django.db import models # Modelos
from django.contrib.auth.models import AbstractUser # Usuario abstracto - USER hereda de esta clase los principales atributos de un usuario. Ej. username y password
from django.urls import reverse
from django.utils.translation import gettext_lazy as _ # Traduccion de texto similar a verbose_name

"""
Class User - Hereda de AbstractUser - Django Class
"""
class User(AbstractUser):
    """Clase Type: Tiene dos tipos el Cliente y el Proveedor"""
    class Types(models.TextChoices):
        CLIENTE = 'CLIENTE', 'Cliente'
        PROVEEDOR = 'PROVEEDOR', 'Proveedor'

    user_type = models.CharField(_('Type'), max_length=50, choices=Types.choices, default=Types.CLIENTE)
    personal_id = models.CharField(max_length=100, null=True, default='', blank=True, verbose_name='NIE/NIF')
    fiscal_id = models.CharField(max_length=100, null=False, default='', blank=True, verbose_name='DNI/Pasaporte')
    address = models.CharField(max_length=100, null=False, default='', blank=True, verbose_name='Domicilio')
    city = models.CharField(max_length=55, null=False, default='', blank=True, verbose_name='Ciudad')
    country = models.CharField(max_length=55, null=False, default='', blank=True, verbose_name='Pais')
    cp = models.CharField(max_length=55, null=False, default='', blank=True)
    contact = models.CharField(max_length=55, null=False, default='', blank=True, verbose_name='Contacto')
    updated_at = models.DateTimeField(auto_now=True, null=False, blank=True)

    """ Definimos la funcion de la clase USER """
    def get_absolute(self):
        return reverse('users:details', kwargs={'username': self.username})

""" Se creará una clase Manager de cada clase, para que Django realice la diferencia entre un tipo y el otro """
class ClienteManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs). filter(type=User.Types.CLIENTE) # Query

class ProveedorManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs). filter(type=User.Types.PROVEEDOR) # Query

""" Clase Cliente - Hereda de USER """
class Cliente(User):
    # instanciamos cliente manager
    objects = ClienteManager()
    class Meta:
        proxy = True # No crea nuevas tablas
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

""" Clase Proveedor - Hereda de USER """
class Proveedor(User):
    objects = ProveedorManager()
    class Meta:
        proxy = True
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'