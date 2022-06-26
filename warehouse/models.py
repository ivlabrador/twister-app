"""
Exportado de Modulos
"""
from django.db import models
from accounts.models import User
from djmoney.models.fields import MoneyField

"""
Class Categoria: Se crean categorias con nombre y descripcion para hacer realicion Many to Many con los productos
"""
class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nombre')
    description = models.CharField(max_length=255, verbose_name='Descripcion')
    created_ad = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creacion: ')

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

    def __str__(self):
        return self.name


"""
Class Prducto: Atributos de los productos
"""
class Product(models.Model):
    name = models.CharField(max_length=110, null=True, blank=True, verbose_name='Nombre')
    brand = models.CharField(max_length=110, null=True, blank=True, verbose_name='Marca')
    model = models.CharField(max_length=110, null=True, blank=True, verbose_name='Modelo')
    price = MoneyField(max_digits=14, decimal_places=2, default_currency='EUR', verbose_name='Precio')
    iva = models.FloatField(default=0, blank=True, verbose_name='IVA')
    created_at = models.DateField(auto_now_add=True, verbose_name='Fecha de Creacion')
    description = models.TextField(max_length=500, verbose_name='Descripcion')
    image = models.ImageField(default='null', verbose_name="Imagen", upload_to='products/')
    min_alert = models.IntegerField(default=0, blank=True, verbose_name='Alerta Minimo')
    discount = models.FloatField(default=0, blank=True, verbose_name='Descuento')
    public = models.BooleanField(default=False, verbose_name="Publicado")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de Actualizacion")
    categories = models.ManyToManyField(Category, verbose_name='Categorias', blank=True)
    proveedor = models.ForeignKey(User, editable=True, on_delete=models.CASCADE)
    # META
    class Meta():
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['-created_at']

    def __str__(self):
        return self.name


"""
Class Almacen: Los almacenes tendran relaciones con el Stock. todo stock debe encontrarse dentro de un almacen
"""
class Warehouse(models.Model):
    name = models.CharField(max_length=110, null=True, blank=True, verbose_name='Nombre')
    created_at = models.DateField(auto_now_add=True, verbose_name='Fecha de Creacion')
    address = models.CharField(max_length=100, null=False, default='', blank=True, verbose_name='Domicilio')
    city = models.CharField(max_length=55, null=False, default='', blank=True, verbose_name='Ciudad')
    country = models.CharField(max_length=55, null=False, default='', blank=True, verbose_name='Pais')
    cp = models.CharField(max_length=55, null=False, default='', blank=True)
    contact = models.CharField(max_length=55, null=False, default='', blank=True, verbose_name='Contacto')
    updated_at = models.DateTimeField(auto_now=True, null=False, blank=True, verbose_name='Fecha de Actualizacion')
    description = models.TextField(max_length=500, verbose_name='Descripcion')
    proveedor = models.ForeignKey(User, editable=True, on_delete=models.CASCADE)

    class Meta():
        verbose_name = "Almacen"
        verbose_name_plural = "Almacenes"
    def __str__(self):
        return self.name

