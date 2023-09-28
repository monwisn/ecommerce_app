from django.urls import path
from . import views


app_name: str = 'store'

urlpatterns = [
    path('', views.all_products, name='all_products'),
    path('categories/', views.category_list, name='category_list'),
    path('new/', views.new_in, name='new_in'),
    path('sale/', views.on_sale, name='on_sale'),
    path('treats/', views.treats, name='treats'),
    path('brands/', views.brand_products, name='brands'),
]
