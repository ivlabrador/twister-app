"""
Exportado de Modulos
"""
from django.shortcuts import render, redirect, HttpResponse
from .models import Lot, Stock # Modelos principales
from warehouse.models import Product, Warehouse # Modelos de productos y almacenes
from django.contrib.auth.decorators import login_required # Autenticaciones
from .forms import LotForm # Formularios
from django.contrib import messages # Mensajes Flash
from django.core.paginator import Paginator
import csv # CSV

"""
add_lot: Formulario para agregar un lote en un almacen, esta funcion puede recibir un id de almacen por parametro
de lo contrario nos dará a elegir un almacen
Una vez cargado el furmalio de lote, la funcion prueba que exista ya el producto en stock
Si existe sumará la cantidad al stock existente caso contrario instanciará un nuevo Stock
"""
@login_required(login_url='/accounts/login-user/')
def add_lot(request, warehouse_id=None):
    my_id = request.user.id
    lot_form = LotForm
    my_products = Product.objects.filter(public=True, proveedor_id=my_id).all()
    if warehouse_id == 'None':
        my_wares = Warehouse.objects.filter(proveedor_id=my_id).all()
    else:
        my_ware = Warehouse.objects.filter(id=warehouse_id).get()
        my_wares = [my_ware, ]
    if request.method == 'POST':
        lot_form = LotForm(request.POST)
        product = request.POST['product']
        if lot_form.is_valid():
            instance = lot_form.save(commit=False)
            instance.proveedor_id = request.user.id
            quantity = int(request.POST['quantity'])
            try:
                stock = Stock.objects.get(product_id=product)
                stock.act_stock = int(stock.act_stock) + int(request.POST['quantity'])
                stock.save()
                instance.save()
                messages.success(request, f"Lote cargado con exito!")
                return redirect('ver_stock')
            except:
                stock = Stock(
                    product_id=product,
                    warehouse_id=request.POST['warehouse'],
                    act_stock=quantity,
                    proveedor_id=my_id,
                )
                stock.save()
                instance.save()
                messages.success(request, f"Lote cargado con exito!")
                return redirect('ver_stock')
        else:
            messages.warning(request, "Hay errores en el formulario!")

    return render(request, 'lot_add.html', {
        'form': lot_form,
        'product': my_products,
        'warehouse': my_wares,
    }
    )

"""
lot_list: Listado de Lotes
"""
@login_required(login_url='/accounts/login-user/')
def lot_list(request):
    lots = Lot.objects.filter(proveedor_id=request.user.id)
    paginator = Paginator(lots, 10)
    page = request.GET.get('page')
    page_lots = paginator.get_page(page)
    return render(request, 'lot_list.html', {'lots': page_lots})

"""
csv_file: Crea un CSV de los lotes cargados por el usuario
"""
@login_required(login_url='/accounts/login-user/')
def csv_lot(request):
    my_id = request.user.id
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=lots.csv'
    writer = csv.writer(response)
    lots = Lot.objects.filter(proveedor_id=my_id).all()
    writer.writerow(['Producto', 'Almacen', 'Fecha de Carga', 'Cantidad', 'Proveedor'])
    for lot in lots:
        writer.writerow([lot.product.name, lot.warehouse.name, lot.created_at, lot.quantity, lot.proveedor ])
    return response

"""
ver_stock: Listado de Stock
"""
@login_required(login_url='/accounts/login-user/')
def ver_stock(request):
    my_id = request.user.id
    stock = Stock.objects.filter(is_active=True, proveedor=my_id).all()
    paginator = Paginator(stock, 10)
    page = request.GET.get('page')
    page_stock = paginator.get_page(page)
    return render(request, 'stock.html', {'stock': page_stock})


"""
csv_stock: Crea un CSV del Stock del usuario-proveedor
"""
@login_required(login_url='/accounts/login-user/')
def csv_stock(request):
    my_id = request.user.id
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=stock.csv'
    writer = csv.writer(response)
    stock = Stock.objects.filter(proveedor_id=my_id).all()
    writer.writerow(['Producto', 'Almacen', 'Fecha de Carga', 'Ultimo movimiento', 'Stock Actual', 'Activo', 'Vendidos'])
    for s in stock:
        writer.writerow([s.product.name, s.warehouse.name, s.created_at, s.updated_at, s.act_stock, s.is_active, s.sold_products, ])
    return response
