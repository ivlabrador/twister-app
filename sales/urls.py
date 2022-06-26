from django.urls import path
from . import views

urlpatterns = [
    path('show-wallet/', views.show_wallet, name='ver_monedero'),
    path('add-credit/', views.add_credit, name='agregar_saldo'),
    path('transaction/<stock_id>', views.transaction, name='transaction'),
    path('transaction-list/', views.list_transaction, name='transaction_list'),
    path('pdf-check/<transactions_id>', views.pdf_check, name='pdf_check'),
    path('csv-sales/', views.csv_sales, name='csv_sales'),
    path('sales-report/', views.sales_report, name='sales_report')
]