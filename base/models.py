from django.db import models
from django.contrib.auth.models import User  # Import the User model

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('Bread', 'Bread'),
        ('Cake', 'Cake'),
        ('Doughnut', 'Doughnut'),
    ]
    ProductID = models.AutoField(primary_key=True)
    ProductName = models.CharField(max_length=100)
    Category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    UnitPrice = models.DecimalField(max_digits=10, decimal_places=2)
    ReorderLevel = models.IntegerField()

    def __str__(self):
        return self.ProductName

class Inventory(models.Model):
    InventoryID = models.AutoField(primary_key=True)
    ProductID = models.ForeignKey(Product, on_delete=models.CASCADE)
    BatchNumber = models.CharField(max_length=50)
    Quantity = models.IntegerField()
    ExpiryDate = models.DateField()
    PurchaseDate = models.DateField()

    def __str__(self):
        return f"{self.ProductID.ProductName} - Batch {self.BatchNumber}"

class Order(models.Model):
    OrderID = models.AutoField(primary_key=True)
    UserID = models.ForeignKey(User, on_delete=models.CASCADE)  # Use the imported User model
    OrderDate = models.DateField(auto_now_add=True)
    TotalAmount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order {self.OrderID} by {self.UserID.username}"

class OrderDetails(models.Model):
    OrderDetailsID = models.AutoField(primary_key=True)
    OrderID = models.ForeignKey(Order, on_delete=models.CASCADE)
    ProductID = models.ForeignKey(Product, on_delete=models.CASCADE)
    Quantity = models.IntegerField()
    UnitPrice = models.DecimalField(max_digits=10, decimal_places=2)
    Subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order {self.OrderID.OrderID} - {self.ProductID.ProductName}"

class Supplier(models.Model):
    SupplierID = models.AutoField(primary_key=True)
    SupplierName = models.CharField(max_length=100)
    ContactNumber = models.CharField(max_length=15)
    Email = models.EmailField()
    Address = models.TextField()

    def __str__(self):
        return self.SupplierName

class Supply(models.Model):
    SupplyID = models.AutoField(primary_key=True)
    SupplierID = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    ProductID = models.ForeignKey(Product, on_delete=models.CASCADE)
    SupplyDate = models.DateField()
    Quantity = models.IntegerField()

    def __str__(self):
        return f"Supply {self.SupplyID} - {self.ProductID.ProductName}"