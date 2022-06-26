"""
Exportado de Modulos
"""
from .models import Warehouse, Product, Category
from django.forms import ModelForm, ModelMultipleChoiceField, SelectMultiple

"""
Formulario de creacion de almacenes
"""
class wareForm(ModelForm):
    class Meta:
        model = Warehouse
        fields = ['name', 'address', 'city', 'country', 'cp', 'contact', 'description']
        db_table = 'warehouse'

"""
Formulario de productos
"""
class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'brand', 'model', 'categories', 'description', 'image', 'price', 'iva', 'discount', 'public', 'min_alert']
        db_table = 'product'

    categories = ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=SelectMultiple()
    )

"""
Formulario de categorias
"""
class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        db_table = ['category']

