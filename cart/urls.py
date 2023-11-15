from django.urls import path
from . import views


app_name: str = 'cart'

urlpatterns: list = [
    path('', views.cart_summary, name='cart_summary'),
    path('add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('update/', views.cart_update, name='cart_update'),
    path('delete/', views.cart_delete, name='cart.delete'),
]
