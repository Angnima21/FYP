from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.utils import timezone
from .models import Product, Inventory, Order
from .forms import ProductForm, InventoryForm
from .models import Supplier, OrderDetails
from .forms import SupplierForm, OrderForm, OrderDetailsForm
from django.db.models import F
from django.http import Http404


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


def edit_item(request, item_type, item_id):
    """
    Generic view to edit a product or order.
    """
    if item_type == 'product':
        model = Product
        form_class = ProductForm
        redirect_url = 'product_list'
    elif item_type == 'order':
        model = Order
        form_class = OrderForm
        redirect_url = 'order_list'
    else:
        raise Http404("Invalid item type.")

    item = get_object_or_404(model, pk=item_id)

    if request.method == 'POST':
        if item_type == 'order':
            # Handle order details for orders
            order_form = form_class(request.POST, instance=item)
            if order_form.is_valid():
                order = order_form.save(commit=False)
                order.TotalAmount = 0  # Reset total amount for recalculation
                order.save()

                # Process each product in the order
                for key, value in request.POST.items():
                    if key.startswith('product_'):
                        product_id = key.split('_')[1]
                        quantity = int(value)  # Convert quantity to integer
                        product = Product.objects.get(ProductID=product_id)
                        unit_price = float(product.UnitPrice)  # Get unit price from the product

                        # Update or create OrderDetails
                        OrderDetails.objects.update_or_create(
                            OrderID=order,
                            ProductID=product,
                            defaults={'Quantity': quantity, 'UnitPrice': unit_price}
                        )

                        # Update the total amount
                        order.TotalAmount += quantity * unit_price

                # Save the updated total amount
                order.save()
                return redirect(redirect_url)
        else:
            # Handle products
            form = form_class(request.POST, instance=item)
            if form.is_valid():
                form.save()
                return redirect(redirect_url)
    else:
        if item_type == 'order':
            # Pre-fill the form with the current order data
            order_form = form_class(instance=item)
            order_details = item.order_details.all()
            products = Product.objects.all()

            # Create a dictionary to store product quantities
            product_quantities = {detail.ProductID.ProductID: detail.Quantity for detail in order_details}

            return render(request, 'base/edit_item.html', {
                'form': order_form,
                'item': item,
                'item_type': item_type,
                'order_details': order_details,
                'products': products,
                'product_quantities': product_quantities,  # Pass product quantities to the template
            })
        else:
            # Pre-fill the form with the current product data
            form = form_class(instance=item)
            return render(request, 'base/edit_item.html', {'form': form, 'item': item, 'item_type': item_type})

def delete_item(request, item_type, item_id):
    """
    Generic view to delete a product or order.
    """
    if item_type == 'product':
        model = Product
        redirect_url = 'product_list'
    elif item_type == 'order':
        model = Order
        redirect_url = 'order_list'
    else:
        raise Http404("Invalid item type.")

    item = get_object_or_404(model, pk=item_id)

    if request.method == 'POST':
        item.delete()
        return redirect(redirect_url)

    return render(request, 'base/confirm_delete.html', {'item': item, 'item_type': item_type})

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
    order_data = []

    for order in orders:
        # Fetch all order details for the current order
        order_details = order.order_details.all()
        products = []

        # Collect product names and quantities
        for detail in order_details:
            products.append({
                'name': detail.ProductID.ProductName,
                'quantity': detail.Quantity,
            })

        # Add order data to the list
        order_data.append({
            'order': order,
            'products': products,
        })

    return render(request, 'base/order_list.html', {'order_data': order_data})

def order_details(request, order_id):
    # Fetch the order and its details
    order = get_object_or_404(Order, OrderID=order_id)
    order_details = order.order_details.all()  # Use the related_name 'order_details'

    return render(request, 'base/order_details.html', {'order': order, 'order_details': order_details})



def create_order(request):
    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            order.TotalAmount = 0  # Initialize total amount
            order.save()

            # Process each product in the order
            for key, value in request.POST.items():
                if key.startswith('product_'):
                    product_id = key.split('_')[1]
                    quantity = int(value)  # Convert quantity to integer

                    try:
                        # Fetch the product
                        product = Product.objects.get(ProductID=product_id)
                        unit_price = float(product.UnitPrice)  # Get unit price from the product

                        # Create OrderDetails
                        OrderDetails.objects.create(
                            OrderID=order,
                            ProductID=product,
                            Quantity=quantity,
                            UnitPrice=unit_price
                        )

                        # Update the total amount
                        order.TotalAmount += quantity * unit_price

                        # Update product stock based on order type
                        if order.OrderType == 'dealer':
                            # Increase stock for dealer orders
                            product.ReorderLevel += quantity
                        elif order.OrderType == 'customer':
                            # Decrease stock for customer orders
                            product.ReorderLevel -= quantity

                        # Save the updated product stock
                        product.save()

                    except Product.DoesNotExist:
                        # Handle the case where the product does not exist
                        print(f"Product with ID {product_id} does not exist.")
                        continue  # Skip this product

            # Save the updated total amount
            order.save()
            return redirect('order_list')
    else:
        order_form = OrderForm()
        products = Product.objects.all()  # Fetch all products
    return render(request, 'base/create_order.html', {'order_form': order_form, 'products': products})

def deduct_stock(product_id, quantity):
    """
    Deduct the ordered quantity from inventory using FIFO.
    """
    # Fetch inventory batches for the product, ordered by PurchaseDate (FIFO)
    batches = Inventory.objects.filter(ProductID=product_id).order_by('PurchaseDate')

    for batch in batches:
        if quantity <= 0:
            break  # Stop if the required quantity is deducted

        if batch.Quantity >= quantity:
            # Deduct the full quantity from this batch
            batch.Quantity = F('Quantity') - quantity
            batch.save()
            quantity = 0
        else:
            # Deduct the entire batch's quantity
            quantity -= batch.Quantity
            batch.Quantity = 0
            batch.save()

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

