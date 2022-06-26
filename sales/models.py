"""
Exportado de Modulos
"""
from django.db import models
from djmoney.models.fields import MoneyField
from stock.models import Stock
from warehouse.models import Product
from accounts.models import User

"""
Class Billetera: La billetera contendrá el dinero del usuario, la misma se instancia al crear un usuario
"""
class Wallet(models.Model):
    quantity = MoneyField(default=0, max_digits=14, decimal_places=2, default_currency='EUR', verbose_name='Cantidad')
    created_at = models.DateField(auto_now_add=True, verbose_name='Fecha de Creacion')
    user = models.ForeignKey(User, editable=True, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ultima Carga")
    class Meta():
        verbose_name = "Monedero"
        verbose_name_plural = "Monederos"
        ordering = ['-created_at']

"""
Class AddCredit: Simula el uso de una tarjeta de credito para ingresar dinero a la cuenta/billetera
"""
class AddCredit(models.Model):
    wallet = models.ForeignKey(Wallet, editable=False, on_delete=models.CASCADE)
    user = models.ForeignKey(User, editable=False, on_delete=models.CASCADE)
    quantity = MoneyField(default=0, max_digits=14, decimal_places=2, default_currency='EUR', verbose_name='Cantidad')
    card_number = models.BigIntegerField(null=False, unique=True)
    security_code = models.IntegerField(null=False)
    expiration_date = models.DateField(null=False)
    class Meta():
        verbose_name = 'Agregar Credito'

"""
Class Transaction: Contiene todos los atributos de una transaccion
"""
class Transactions(models.Model):
    product = models.ForeignKey(Product, editable=False, verbose_name='Producto', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0, verbose_name='Cantidad')
    price = MoneyField(max_digits=14, decimal_places=2, default_currency='EUR', verbose_name='Precio')
    created_at = models.DateField(auto_now_add=True, verbose_name='Fecha de Transaccion')
    user = models.ForeignKey(User, editable=True, related_name='CLIENTE', on_delete=models.CASCADE)
    proveedor = models.ForeignKey(User, editable=False, related_name='PROVEEDOR', on_delete=models.CASCADE)
    stock_from = models.ForeignKey(Stock, editable=False, on_delete=models.CASCADE)
    class Meta():
        verbose_name = "Transaccion"
        verbose_name_plural = "Transacciones"
        ordering = ['-created_at']