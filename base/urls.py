from django.urls import path
from . import views


urlpatterns = [
    path('auth/', views.auth_view, name='auth'),  # Combined login/registration
    path('logout/', views.logout_view, name='logout'),
    path('', views.home_view, name='home'), 
    path('dashboard/', views.dashboard_view, name='dashboard'),
 
    # Product URLs
    path('products/', views.product_list, name='product_list'),
    path('products/add/', views.add_product, name='add_product'),
    path('products/edit/<str:item_type>/<int:item_id>/', views.edit_item, name='edit_item'),  # Generic edit URL
    path('products/delete/<str:item_type>/<int:item_id>/', views.delete_item, name='delete_item'),  # Generic delete URL

    # Order URLs
    path('orders/', views.order_list, name='order_list'),
    path('orders/create/', views.create_order, name='create_order'),
    path('orders/edit/<str:item_type>/<int:item_id>/', views.edit_item, name='edit_item'),  # Generic edit URL
    path('orders/delete/<str:item_type>/<int:item_id>/', views.delete_item, name='delete_item'),  # Generic delete URL
    path('orders/<int:order_id>/', views.order_details, name='order_details'),

    path('inventory/', views.inventory_list, name='inventory_list'),
    path('inventory/add/', views.add_inventory, name='add_inventory'),   
    path('alerts/', views.alerts_list, name='alerts_list'),
    path('suppliers/', views.supplier_list, name='supplier_list'),
    path('suppliers/add/', views.add_supplier, name='add_supplier'),
    
    
]
