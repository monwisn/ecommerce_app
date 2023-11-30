from django.urls import path
from . import views

app_name: str = 'cart'

urlpatterns: list = [
    path('', views.session_cart_summary, name='session_cart_summary'),
    path('add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('delete/<int:product_id>/', views.cart_delete, name='cart_delete'),
    path('update/<int:product_id>/', views.cart_update, name='cart_update'),
    # path('', views.cart_summary, name='cart_summary'),
    # path('', views.session_cart_summary, name='session_cart_summary'),
]
