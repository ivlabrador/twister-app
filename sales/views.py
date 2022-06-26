"""
Exportado de Modulos
"""
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required # evita que se pueda entrar a la url sin estar logueado
from .forms import AddCreditForm, TransactionForm # Formularios
from .models import Wallet, Transactions # Modelos principales
from stock.models import Stock # Modelo de Stock
from django.contrib import messages # Mensajes flash
from djmoney.money import Money # DJ Money APP extra para usar dinero como un field
from django.core.paginator import Paginator
# Modelos necesarios para la factura de ventas
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from datetime import datetime
from django.db.models.functions import Coalesce
from djmoney.models.fields import MoneyField
from django.db.models import Sum
import csv # CSV




"""
show_wallet: Nos muestra por pantalla nuestra billetera personal
"""
@login_required(login_url='/accounts/login-user/')
def show_wallet(request):
    user_id = request.user.id
    my_wallet = Wallet.objects.get(user_id=user_id)
    return render(request, 'show_wallet.html', {'wallet': my_wallet})

"""
add_credit: Formulario para agregar credito a la billetera
"""
@login_required(login_url='/accounts/login-user/')
def add_credit(request):
    user_id = request.user.id
    my_wallet = Wallet.objects.get(user_id=user_id)
    add_credit_form = AddCreditForm
    if request.method == 'POST':
        add_credit_form = AddCreditForm(request.POST)
        if add_credit_form.is_valid():
            instance = add_credit_form.save(commit=False)
            instance.user_id = user_id
            instance.wallet_id = my_wallet.id
            quantity_add = Money(request.POST['quantity_0'], 'EUR')
            wallet_quantity = my_wallet.quantity
            total_credit = (quantity_add + wallet_quantity)
            my_wallet.quantity = total_credit
            my_wallet.save()
            instance.save()
            messages.success(request, f"Credito cargado con exito!")
            return redirect('ver_monedero')
        else:
            messages.warning(request, f"Hay errores en el formulario!")

    return render(request, 'add_credit.html', {'form': add_credit_form})

"""
transaction: la transaccion se basa en la eleccion de un producto que se encuentre en STOCK
elegido el producto y la cantidad deseada la funcion comprueba que exista la cantidad desea del producto
y tu disponibilidad de dinero. En caso de poder comprar el producto, la transaccion será realizada.
El dinero se moverá desde la billetera del cliente hacia la del proveedor y el stock bajará.
"""
@login_required(login_url='/accounts/login-user/')
def transaction(request, stock_id):
    user_id = request.user.id
    my_wallet = Wallet.objects.get(user_id=user_id)
    stock = Stock.objects.get(pk=stock_id)
    prove_id = stock.proveedor.id
    prove_wallet = Wallet.objects.get(user_id=prove_id)
    product = stock.product
    discount = float(product.discount)
    iteration = range(1, (int(stock.act_stock)+1))
    transaction_form = TransactionForm
    if request.method == 'POST':
        transaction_form = TransactionForm(request.POST)
        quantity_select = int(request.POST['quantity'])
        if stock.act_stock >= quantity_select:
            if discount == 0:
                total_price = (quantity_select * product.price)
            else:
                total_price = (quantity_select * product.price)-((quantity_select * product.price)/100)*discount
            if transaction_form.is_valid():
                instance = transaction_form.save(commit=False)
                instance.user_id = user_id
                instance.wallet_id = my_wallet.id
                instance.proveedor_id = stock.proveedor.id
                instance.stock_from_id = stock_id
                instance.price = total_price
                instance.product_id = product.id
                if my_wallet.quantity >= total_price:
                    my_wallet.quantity = (my_wallet.quantity - total_price)
                    prove_wallet.quantity = (prove_wallet.quantity + total_price)
                    stock.act_stock = (stock.act_stock - quantity_select)
                    stock.sold_products = (stock.sold_products + quantity_select)
                    instance.save()
                    my_wallet.save()
                    prove_wallet.save()
                    stock.save()
                    messages.success(request, 'Gracias por su compra!!')
                    return redirect('ver_monedero')
                else:
                    messages.warning(request, 'Usted no tiene saldo para realizar esta operacion')
            else:
                messages.warning(request, f"Hay errores en el formulario!")
        else:
            messages.warning(request, 'No se encuentran tantas unidades del producto en Stock, intente nuevamente')

    return render(request, 'transaction.html', {
        'form': transaction_form,
        'stock': stock,
        'product': product,
        'iteration': iteration,
    }
                  )

"""
list_transaction: Aqui se alistarán todas las transacciones dependiendo si el usuario es cliente o proveedor
"""
@login_required(login_url='/accounts/login-user/')
def list_transaction(request):
    user_id = request.user.id
    if request.user.user_type == 'CLIENTE':
        my_transactions = Transactions.objects.filter(user_id=user_id).all()
        paginator = Paginator(my_transactions, 10)
        page = request.GET.get('page')
        page_transactions = paginator.get_page(page)
    elif request.user.user_type == 'PROVEEDOR':
        my_transactions = Transactions.objects.filter(proveedor_id=user_id).all()
        paginator = Paginator(my_transactions, 10)
        page = request.GET.get('page')
        page_transactions = paginator.get_page(page)
    else:
        None

    return render(request, 'my_transactions.html', {'transactions': page_transactions})

"""
pdf_generation: Esta funcion creará la factura para el cliente, esta se vera dentro de la tabla de transacciones
"""
@login_required(login_url='/accounts/login-user/')
def pdf_check(request, transactions_id):
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont('Helvetica', 14)
    t = Transactions.objects.get(pk=transactions_id)

    lines = [
        '###Factura de Compra###',
        f'Producto: {t.product.name}',
        f'Cantidad: {t.quantity}',
        f'Precio: {t.price}',
        f'IVA: %{t.product.iva}',
        f'Descuento: %{t.product.discount}',
        f'Proveedor: {t.proveedor}',
        '',
        f'Muchas gracias por su compra {t.user}!!!',

    ]

    for line in lines:
        textob.textLine(line)

    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)

    return FileResponse(buf, as_attachment=True, filename='factura.pdf')

"""
csv_sales: Crea un CSV de las ventas del usuario-proveedor
"""
@login_required(login_url='/accounts/login-user/')
def csv_sales(request):
    my_id = request.user.id
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=sales.csv'
    writer = csv.writer(response)
    sales = Transactions.objects.filter(proveedor_id=my_id).all()
    writer.writerow(['Producto', 'Cantidad', 'Moneda', 'Costo', 'Fecha y Hora', 'Stock Actual', 'Cliente'])
    for s in sales:
        writer.writerow([s.product.name, s.quantity, s.price_currency, s.price, s.created_at, s.user])
    return response


"""
sales_report: Esta funcion exportará una grafico de las ventas de cada proveedor
"""
@login_required(login_url='/accounts/login-user/')
def sales_report(request):
    data = []
    my_id = request.user.id
    year = datetime.now().year
    for m in range(1, 13):
        total = Transactions.objects.filter(proveedor_id=my_id, created_at__year=year, created_at__month=m).aggregate(r=Coalesce(Sum('price'), 0, output_field=MoneyField())).get('r')
        data.append(float(total))

    return render(request, 'sales_report.html', {'data': data})




