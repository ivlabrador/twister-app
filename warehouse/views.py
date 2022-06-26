"""
Exportado de Modulos
"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import wareForm, ProductForm, CategoryForm
from django.contrib import messages
from .models import Warehouse, Product
from stock.models import Lot, Stock
from django.core.paginator import Paginator

"""
Home: En esta template se mostrara la informacion general de la APP
"""
def home(request):
    my_user = request.user
    return render(request, 'home.html', {'user': my_user})


### USUARIO PROVEEDOR ###
### PRODCUCTOS ###
"""
add_product: Cuenta con un formulario de registro de productos basado en sus modelos
"""
@login_required(login_url='/accounts/login-user/')
def add_product(request):
    product_form = ProductForm
    if request.method == 'POST':
        product_form = ProductForm(request.POST, request.FILES or None)
        if product_form.is_valid():
            instance = product_form.save(commit=False)
            instance.proveedor_id = request.user.id
            instance.save()
            messages.success(request, "Producto Creado con Exito")
            return redirect('ver_productos')
        else:
            messages.warning(request, "Hay errores en el formulario!")
    return render(request, 'product_add.html', {'form': product_form})

"""
add_category: Cuenta con un formulario de registro de categorias
"""
@login_required(login_url='/accounts/login-user/')
def add_category(request):
    category_form = CategoryForm
    if request.method == 'POST':
        category_form = CategoryForm(request.POST)
        if category_form.is_valid():
            category_form.save()
            messages.success(request, f"Categoria Creada con Exito: {request.POST['name']}")
            return redirect('add_categoria')
        else:
            messages.warning(request, "Hay errores en el formulario!")
    return render(request, 'category_add.html', {'form': category_form})

"""
product_list: listados de todos los productos del proveedor identificado
"""
@login_required(login_url='/accounts/login-user/')
def product_list(request):
        products = Product.objects.filter(proveedor_id=request.user.id)
        # Paginator - paginar los productos - cantidad 8 por pagina
        paginator = Paginator(products, 8)
        # Recoger numero de pagina
        page = request.GET.get('page')
        page_products = paginator.get_page(page)
        return render(request, 'product_list.html', {'products': page_products})

"""
product_edit: formulario de edicion de producto
"""
@login_required(login_url='/accounts/login-user/')
def product_edit(request, product_id):
    product = Product.objects.get(pk=product_id)
    edit_form = ProductForm(request.POST or None, request.FILES or None, instance=product)
    if edit_form.is_valid():
        edit_form.save()
        messages.success(request, f"Producto Editado con Exito")
        return redirect('ver_productos')
    else:
        messages.warning(request, "Hay errores en el formulario!")
    return render(request, 'product_edit.html', {
        'product': product,
        'form': edit_form
        }
    )

"""
product_delete: eliminar producto
"""
@login_required(login_url='/accounts/login-user/')
def product_delete(request, product_id):
    product = Product.objects.get(pk=product_id)
    product.delete()
    messages.success(request, f"Producto Eliminado con Exito")
    return redirect('ver_productos')


### ALMACENES ###


"""
ware_add: Formulario de registro de almacen
"""
@login_required(login_url='/accounts/login-user/')
def ware_add(request):
    ware_form = wareForm
    if request.method == 'POST':
        ware_form = wareForm(request.POST)
        if ware_form.is_valid():
            instance = ware_form.save(commit=False)
            instance.proveedor_id = request.user.id
            instance.save()
            messages.success(request, f"Almacen Creado con Exito para el Proveedor: {request.user.username}")
            return redirect('ver_almacenes')
        else:
            messages.warning(request, "Hay errores en el formulario!")
    else:
        return render(request, 'ware_add.html', {'form': ware_form})

"""
ware_list: Listado de almacenes del usuario identificado
"""
@login_required(login_url='/accounts/login-user/')
def ware_list(request):
    warehouses = Warehouse.objects.filter(proveedor_id=request.user.id)
    return render(request, 'ware_list.html', {'warehouses': warehouses})

"""
ware_products: Lista todos los lotes que el usuario ha cargado
"""
@login_required(login_url='/accounts/login-user/')
def ware_products(request, warehouse_id):
        warehouse = Warehouse.objects.get(pk=warehouse_id)
        lots = Lot.objects.filter(warehouse_id=warehouse_id).all()
        paginator = Paginator(lots, 8)
        page = request.GET.get('page')
        page_products = paginator.get_page(page)
        return render(request, 'ware_in_products.html', {'lots': page_products, 'warehouse': warehouse})

"""
ware_edit: Formulario de edicion de almacenes
"""
@login_required(login_url='/accounts/login-user/')
def ware_edit(request, warehouse_id):
    warehouse = Warehouse.objects.get(pk=warehouse_id)
    edit_form = wareForm(request.POST or None, instance=warehouse)
    if edit_form.is_valid():
        edit_form.save()
        messages.success(request, f"Almacen Editado con Exito")
        return redirect('ver_almacenes')
    else:
        messages.warning(request, "Hay errores en el formulario!")
    return render(request, 'ware_edit.html', {
        'warehouse': warehouse,
        'form': edit_form
        }
    )

"""
ware_delete: Elimina un almacen
"""
@login_required(login_url='/accounts/login-user/')
def ware_delete(request, warehouse_id):
    warehouse = Warehouse.objects.filter(pk=warehouse_id)
    warehouse.delete()
    messages.success(request, f"Almacen Eliminado con Exito")
    return redirect('ver_almacenes')


### USUARIO CLIENTE ###


"""
product_show: Muestra al cliente todos los productos que se encuentren actualmente en Stock
"""
@login_required(login_url='/accounts/login-user/')
def product_show(request):
        products = Stock.objects.filter(is_active=True).all()
        paginator = Paginator(products, 8)
        page = request.GET.get('page')
        page_products = paginator.get_page(page)
        return render(request, 'product_show.html', {'products': page_products})