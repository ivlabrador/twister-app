"""
Exportado de Modulos
"""
from django.contrib import admin
from .models import Lot, Stock

"""
Configuarion del panel de administracion
Clases: 
    Lot
    Stock
"""
class AdminLot(admin.ModelAdmin):
    search_fields = ('product', 'warehouse')
    list_display = ('product', 'warehouse', 'quantity', 'proveedor')

class AdminStock(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at')
    list_filter = ('product', 'warehouse', 'proveedor')
    search_fields = ('product', 'warehouse', 'proveedor')
    list_display = ('product', 'warehouse', 'act_stock', 'proveedor', 'updated_at')

"""
Registro de modelos
"""
admin.site.register(Lot, AdminLot)
admin.site.register(Stock, AdminStock)

