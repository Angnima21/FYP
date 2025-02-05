from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.utils import timezone
from .models import Product, Inventory, Order
from .forms import ProductForm, InventoryForm
from .models import Supplier, OrderDetails
from .forms import SupplierForm, OrderForm




def inventory_list(request):
    inventory = Inventory.objects.all().order_by('PurchaseDate')
    return render(request, 'base/inventory_list.html', {'inventory': inventory})


def add_inventory(request):
    if request.method == 'POST':
        form = InventoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventory_list')
    else:
        form = InventoryForm()
    return render(request, 'base/add_inventory.html', {'form': form})

def auth_view(request):
    action = request.GET.get('action', 'login')  # Default to login
    is_login = action == 'login'

    if request.method == 'POST':
        if is_login:
            form = AuthenticationForm(request, data=request.POST)
            if form.is_valid():
                user = form.get_user()
                login(request, user)
                return redirect('dashboard')
        else:
            form = UserCreationForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm() if is_login else UserCreationForm()

    context = {
        'form': form,
        'is_login': is_login,
        'title': 'Login Here' if is_login else 'Sign Up',
    }
    return render(request, 'base/auth.html', context)

def logout_view(request):
    logout(request)
    return redirect('auth')

def home_view(request):
    return render(request, 'base/home.html')

def dashboard_view(request):
    context = {
        'low_stock_count': 5,  # Replace with actual data
        'expiry_warnings_count': 3,  # Replace with actual data
        'alerts': [
            {'product': 'Bread', 'type': 'Low Stock', 'date': '2024-01-01'},
            {'product': 'Cake', 'type': 'Expiry Warning', 'date': '2024-01-05'},
        ],  # Replace with actual data
    }
    return render(request, 'base/dashboard.html', context)

############################################################################################################

def product_list(request):
    products = Product.objects.all()
    return render(request, 'base/product_list.html', {'products': products})

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'base/add_product.html', {'form': form})

###############################################################################

def inventory_list(request):
    inventory = Inventory.objects.all().order_by('PurchaseDate')
    return render(request, 'base/inventory_list.html', {'inventory': inventory})

def add_inventory(request):
    if request.method == 'POST':
        form = InventoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventory_list')
    else:
        form = InventoryForm()
    return render(request, 'base/add_inventory.html', {'form': form})

############################################################################

def order_list(request):
    orders = Order.objects.all()
    return render(request, 'base/order_list.html', {'orders': orders})


def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('order_list')
    else:
        form = OrderForm()
    return render(request, 'base/create_order.html', {'form': form})

###########################################################################

def alerts_list(request):
    # Low stock alerts: Products with stock below reorder level
    low_stock_products = Product.objects.filter(ReorderLevel__lt=10)

    # Expiry alerts: Inventory items expiring within the next 7 days
    expiry_alerts = Inventory.objects.filter(ExpiryDate__lt=timezone.now() + timezone.timedelta(days=7))

    return render(request, 'base/alerts_list.html', {
        'low_stock_products': low_stock_products,
        'expiry_alerts': expiry_alerts,
    })
    
##################################################################################################################

def supplier_list(request):
    suppliers = Supplier.objects.all()
    return render(request, 'base/supplier_list.html', {'suppliers': suppliers})

def add_supplier(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('supplier_list')
    else:
        form = SupplierForm()
    return render(request, 'base/add_supplier.html', {'form': form})