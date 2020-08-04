from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('shop/', views.shop, name='shop'),
    path('cart/', views.cart, name='cart'),
    path('buy/', views.buy, name='buy'),
    path('purchase/<int:id>/<str:usr>/', views.purchase, name='purchase'),
    path('reports/', views.reports, name='reports'),
    path('register/', views.register, name='register'),
    path('mylist/<str:usr>/', views.mylist, name='mylist'),
    path('shop/<int:id>/<str:action>/', views.add_remove_products, name='add_remove_products'),

]