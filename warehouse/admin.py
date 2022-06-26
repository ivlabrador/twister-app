"""
Exportado de Modulos
"""
from django.contrib import admin
from .models import Warehouse, Product, Category

"""
Configuarion del panel de administracion
Clases: 
    Category
    Product
    Warehouse
"""
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ('name', 'description')
    readonly_fields = ('created_ad', ) # CORREGIR ERROR de GRAMATICA DESDE LOS MODELOS
    list_display = ('name', 'description', 'created_ad')

class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at', 'price')
    list_filter = ('public', 'categories')
    search_fields = ('name', 'description')
    list_display = ('name', 'price', 'public', 'created_at', 'description')
    def save_model(self, request, obj, form, change):
        if not obj.proveedor_id:
            obj.proveedor_id = request.user_id
        obj.save()

class WareAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at')
    search_fields = ('address', 'proveedor')
    list_display = ('name', 'address', 'city', 'proveedor', 'created_at')
    list_filter = ('city', )
    def save_model(self, request, obj, form, change):
        if not obj.proveedor_id:
            obj.proveedor_id = form.request.user_id
        obj.save()

"""
Registro de modelos
"""
admin.site.register(Warehouse, WareAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
