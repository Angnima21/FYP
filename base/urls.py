from django.urls import path
from . import views


urlpatterns = [
    path('auth/', views.auth_view, name='auth'),  # Combined login/registration
    path('logout/', views.logout_view, name='logout'),
    path('', views.home_view, name='home'), 
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('products/', views.product_list, name='product_list'),
    path('products/add/', views.add_product, name='add_product'),
    path('inventory/', views.inventory_list, name='inventory_list'),
    path('inventory/add/', views.add_inventory, name='add_inventory'),   
    path('orders/', views.order_list, name='order_list'),
    path('orders/create/', views.create_order, name='create_order'),
    path('alerts/', views.alerts_list, name='alerts_list'),
    path('suppliers/', views.supplier_list, name='supplier_list'),
    path('suppliers/add/', views.add_supplier, name='add_supplier'),
]
