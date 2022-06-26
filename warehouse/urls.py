from django.urls import path
from . import views

urlpatterns = [
    # URL ADMIN
    path('', views.home, name='home'),
    # URLS GENERALES
    path('home/', views.home, name='home'),
    # URLS PARA PROVEEDORES
    # DROPDOWN PRODUCTOS:
    path('agregar-producto/', views.add_product, name='add_producto'),
    path('agregar-categoria/', views.add_category, name='add_categoria'),
    path('mis-productos/', views.product_list, name='ver_productos'),
    path('editar-producto/<product_id>', views.product_edit, name='editar_producto'),
    path('eliminar-producto/<product_id>', views.product_delete, name='eliminar_producto'),
    # DROPDOWN ALMACENES:
    path('agregar-almacen/', views.ware_add, name='add_almacen'),
    path('ver-almacenes/', views.ware_list, name='ver_almacenes'),
    path('editar-almacen/<warehouse_id>', views.ware_edit, name='editar_almacen'),
    path('eliminar-almacen/<warehouse_id>', views.ware_delete, name='eliminar_almacen'),
    path('productos-en-almacen/<warehouse_id>', views.ware_products, name='productos_almacen'),
    #
    # URLS PARA CLIENTES
    path('productos/', views.product_show, name='show_productos'),
]