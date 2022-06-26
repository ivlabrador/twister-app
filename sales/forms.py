"""
Exportado de Modulos
"""
from .models import AddCredit, Transactions
from django.forms import ModelForm, DateField, SelectDateWidget
from django.conf import settings as s

"""
Formulario Agregado de Dinero
"""
class AddCreditForm(ModelForm):
    expiration_date = DateField(widget=SelectDateWidget(), input_formats=s.DATE_INPUT_FORMATS)
    class Meta:
        model = AddCredit
        fields = ['quantity', 'card_number', 'security_code', 'expiration_date']

"""
Formulario de transaccion
"""
class TransactionForm(ModelForm):
    class Meta:
        model = Transactions
        fields = ['quantity']
