from django.test import TestCase
from .models import OrderLineItem, Customer, ProductList, Order
from django.contrib.auth.models import User
# from . import signals
import datetime


class TestViews(TestCase):
    """
    def setUp(self) -> None:
        self.user = User(username='abc2')
        #self.user.save()
        self.customer = Customer(user=self.user, name=self.user.username)
        #self.user.save()
        self.product = ProductList(name="Tea pot", brand="Le Creuset", price="47.00GBP", in_stock_quantity=50)
        self.order = Order(customer=self.customer, create_dt=datetime.datetime.now())
        self.line_item = OrderLineItem(order=self.order, product=self.product, customer=self.customer, quantity=10)
    """
    def _populate_user_data(self, usr):
        """
        Private helper function to create user record and the subsequent signal execution
        for customer creation.
        """
        self.user = User.objects.create(username=usr, password='abc', is_superuser=0, first_name=usr, email='abc@abc.com',
                                        is_staff=0, is_active=1, last_name=usr)
        return Customer.objects.all()

    def test_signal_user_customer_creation(self):
        """
        Tests the Customer creation signal when a new user is created.
        """
        usr = self._populate_user_data('abc1')
        cust = Customer.objects.all()
        self.assertEqual(usr[0].name, cust[0].name)


