from django.contrib import admin
from .models import ProductList, Customer


admin.site.register(ProductList),
admin.site.register(Customer)
