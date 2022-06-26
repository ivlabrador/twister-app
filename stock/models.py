"""
Exportado de Modulos
"""
from django.db import models
from warehouse.models import Product, Warehouse
from accounts.models import User

"""
Class Lote: Instacia un Lote de un producto x dentro de un almacen x. Para sumarlo al Stock general del producto.
"""
class Lot(models.Model):
    product = models.ForeignKey(Product, editable=True, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True, verbose_name='Fecha de Creacion')
    quantity = models.IntegerField(default=0, blank=True, verbose_name='Cantidad')
    proveedor = models.ForeignKey(User, editable=True, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouse, editable=True, on_delete=models.CASCADE)

    class Meta():
        verbose_name = "Lote"
        verbose_name_plural = "Lotes"
        ordering = ['-created_at']

    def __str__(self):
        return self.product.name

"""
Class Stock: Instancia un Stock - Por cada producto existe solo un Stock que se actualizará con la carga de lotes
"""
class Stock(models.Model):
    product = models.ForeignKey(Product, editable=True, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouse, editable=True, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True, verbose_name='Fecha de Creacion')
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de Actualizacion")
    act_stock = models.IntegerField(default=0, blank=True, verbose_name='Stock Actual')
    is_active = models.BooleanField(default=False)
    proveedor = models.ForeignKey(User, editable=True, on_delete=models.CASCADE)
    sold_products = models.IntegerField(default=0, blank=True, verbose_name='Vendidos')
    class Meta():
        verbose_name = "Stock"
        verbose_name_plural = "Stocks"
        ordering = ['-created_at']

    """
    save: Se modifica la funcion nativa de SAVE. en este caso controla que el stock actual sea mayor a 0
    para que el atributo de stock is_stock se modifique de ser necesario.
    """
    def save(self, *args, **kwargs):
        if self.act_stock > 0:
            self.is_active = True
            return super(Stock, self).save(*args, **kwargs)
        elif self.act_stock == 0:
            self.is_active = False
            return super(Stock, self).save(*args, **kwargs)
        else:
            None

    """
    alert_stock: Esta funcion comprueba al iniciar sesion que tus productos en stock cumplan sean mayor que el
    minimo de referencia. Para enviarte una alerta de stock informativa
    """
    def alert_stock(self):
        if self.act_stock <= self.product.min_alert:
            return True
        else:
            return False