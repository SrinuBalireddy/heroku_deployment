from django.db import models
from django.contrib.auth.forms import User


class ProductList(models.Model):
    """
    Stores the list of products added by the couples
    """

    name = models.CharField(max_length=200)
    brand = models.CharField(max_length=200, blank=True)
    price = models.FloatField()
    in_stock_quantity = models.IntegerField()

    def __str__(self):
        return self.name


class Customer(models.Model):
    """
    Stores the couple information
    """

    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    """
    Stores the orders placed by the customers
    """
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    create_dt = models.DateTimeField(auto_now_add=True)
    order_fulfilled = models.BooleanField(default=False)


class OrderLineItem(models.Model):
    """
    Order line item information of each order.
    1:M relationship with orders to Products
    """
    product = models.ForeignKey(ProductList, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=200, null=True, default='Pending')
    quantity_purchased = models.IntegerField(default=0, null=True, blank=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total