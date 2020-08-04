from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User
from prezola.models import OrderLineItem, Customer, Order, ProductList
from prezola.views import add_remove_products
from django.contrib.messages.storage.fallback import FallbackStorage
import datetime


class TestViews(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def _populate_db(self, usr):
        """
        Private helper function to create user record and the subsequent signal execution
        for customer creation.
        """
        self.user = User.objects.create(username=usr, password='abc', is_superuser=0, first_name=usr, email='abc@abc.com',
                                        is_staff=0, is_active=1, last_name=usr)
        self.customer = Customer.objects.all()
        self.product = ProductList.objects.create(name="Tea pot", brand="Le Creuset", price="47.00", in_stock_quantity=50)
        self.order = Order.objects.create(customer=self.customer[0], create_dt=datetime.datetime.now()
                                          , order_fulfilled=False)
        self.line_item = OrderLineItem.objects.create(order=self.order, product=self.product, customer=self.customer[0], quantity=10)

        return self.user, self.customer, self.product, self.order, self.line_item

    def test_homeview_url_accessible_by_name(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'prezola/home.html')

    def test_cart_view_url_accessible_by_name(self):
        response = self.client.get(reverse('cart'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'prezola/cart.html')

    """
    def test_add_remove_products(self):
        user, customer, product, order, line_item = self._populate_db('test')
        oli = OrderLineItem.objects.all()
        print(line_item.quantity)
        request = self.factory.get(reverse('add_remove_products', kwargs={'id': product.id, 'action': 'removed'}))
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        response = add_remove_products(request, product.id, 'removed')
    """







