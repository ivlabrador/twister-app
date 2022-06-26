from django.urls import path
from . import views

urlpatterns = [
    path('add-lot/<warehouse_id>', views.add_lot, name='add_lot'),
    path('lot-list/', views.lot_list, name='lot_list'),
    path('stock/', views.ver_stock, name='ver_stock'),
    path('csv-stock/', views.csv_stock, name='csv_stock'),
    path('csv-lots/', views.csv_lot, name='csv_lot')
    ]