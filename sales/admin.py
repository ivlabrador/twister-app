"""
Exportado de Modulos
"""
from django.contrib import admin
from .models import Wallet, Transactions

"""
Configuarion del panel de administracion
Clases: 
    Wallet
    Wallet
"""
class WalletAdmin(admin.ModelAdmin):
    search_fields = ['user', ]
    list_display = ['user', 'quantity_currency', 'quantity']

class TransactionAdmin(admin.ModelAdmin):
    search_fields = ['product', 'proveedor', 'user']
    list_display = ['product', 'proveedor', 'quantity', 'price', 'user', 'created_at']

"""
Registro de modelos
"""
admin.site.register(Wallet, WalletAdmin)
admin.site.register(Transactions, TransactionAdmin)
