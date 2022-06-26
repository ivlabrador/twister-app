"""
Exportado de Modulos
"""
from .models import Lot
from django.forms import ModelForm

"""
Formulario de Lotes
"""
class LotForm(ModelForm):
    class Meta:
        model = Lot
        fields = ['product', 'warehouse', 'quantity',]
        db_table = ['lot']