from django.shortcuts import render, redirect
from .models import ProductList, Customer, Order, OrderLineItem
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm


def home(request):
    """
    Homepage
    """

    return render(request, 'prezola/home.html')


@login_required()
def shop(request):
    """
    Products display for a customer
    """

    context = {
        'products': ProductList.objects.all(),
        'type': 'main_view'
    }
    return render(request, 'prezola/shop.html', context)


def add_remove_products(request, id, action):
    """
    update order line items of a customer.
    Handles the line items status logic and purchased quantity updates.
    :param request: get request
    :param id: product Id
    :param action: add/remove
    :return: redirection to /shop/ url
    """
    product = ProductList.objects.get(id=id)
    customer = request.user.customer
    order, create = Order.objects.get_or_create(customer=customer)
    orderlineitem, create = OrderLineItem.objects.get_or_create(order=order, product=product, customer=customer)

    if action == 'added' or action == 'cart_added':
        orderlineitem.quantity += 1
        if orderlineitem.status == 'Complete':
            orderlineitem.status = 'Pending'
        messages.success(request, f"{product.name} has been {action.replace('cart_', '')} to your list")
    elif action == 'removed' or action == 'cart_removed':
        orderlineitem.quantity -= 1
        if orderlineitem.quantity <= 0 and orderlineitem.quantity_purchased > 0:
            orderlineitem.status = 'Complete'
        messages.warning(request, f"{product.name} has been {action.replace('cart_', '')} from your list")

    orderlineitem.save()

    if orderlineitem.quantity <= 0 and orderlineitem.status != 'Complete':
        orderlineitem.delete()

    if action == 'added':
        return redirect('shop')
    elif action == 'removed':
        return redirect('mylist', usr=None)
    elif action == 'cart_added' or action == 'cart_removed':
        return redirect('cart')


def cart(request):
    """"
    Call the cart template file to display the selected products
    """
    try:
        usr = request.user.customer
    except AttributeError:
        # TO BE: for guest checkout
        usr = None

    orderlineitems = OrderLineItem.objects.all().filter(customer=usr).order_by('-date_added')
    context = {
        'lineitems': orderlineitems
    }
    return render(request, 'prezola/cart.html', context)


def mylist(request, usr):
    """
    view to display the customer wish list
    """

    try:
        customer = request.user.customer
        category = 'mylist'
        context = {
            'orderlineitems': OrderLineItem.objects.all().filter(customer=customer),
            'type': category
        }
        # messages.success(request, f"Congratulations on completing your wishlist!")
    except AttributeError:
        customer = Customer.objects.get(user=usr)
        category = 'purchase'
        context = {
            'orderlineitems': OrderLineItem.objects.all().filter(customer=customer, quantity__gt=0),
            'type': category
        }

    # messages.success(request, f"Congratulations on completing your wishlist!")

    return render(request, 'prezola/shop.html', context)


def buy(request):
    """
    Handles the gift purchase logic
    """
    if request.method == "POST":
        customer = Customer.objects.all().filter(name=request.POST.get('name'))
        context = {
            'customer': customer,
        }
    else:
        context = {
            'customer': None,
        }

    return render(request, 'prezola/query.html', context)


def reports(request):
    """
    Generates reports for purchased and non purchased products.
    """
    context = {
        'orderlineitems': OrderLineItem.objects.all().filter(customer=request.user.customer),
        'purchased_items': OrderLineItem.objects.all().filter(customer=request.user.customer, quantity_purchased__gt=0),
        'to_be_purchased_items': OrderLineItem.objects.all().filter(customer=request.user.customer, quantity__gt=0)
    }
    return render(request, 'prezola/reports.html', context)


def purchase(request, id, usr):
    """
    Allows the guest users to purchase the product and handles the orderline item updates
    """
    product = ProductList.objects.get(id=id)
    customer = Customer.objects.get(user=usr)
    order, create = Order.objects.get_or_create(customer=customer)
    orderlineitem, create = OrderLineItem.objects.get_or_create(order=order, product=product, customer=customer)

    orderlineitem.quantity -= 1
    orderlineitem.quantity_purchased += 1

    if orderlineitem.quantity <= 0:
        orderlineitem.status = 'Complete'

    orderlineitem.save()
    messages.success(request, f"{product.name} has been purchased")

    return redirect('mylist', usr)


def register(request):
    """
    user registration form
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f'Account created for {username}')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'prezola/register.html', {'form': form})

