from django.urls import path
from . import views


app_name: str = 'store'

urlpatterns: list = [
    path('', views.all_products, name='all_products'),
    path('categories/', views.category_list, name='category_list'),
    path('category/<int:pk>/', views.category_view, name='category_view'),
    path('new/', views.new_in, name='new_in'),
    path('sale/', views.on_sale, name='on_sale'),
    # path('treats/', views.treats, name='treats'),
    path('brands/', views.brand_products, name='brands'),
    path('brands/<str:name>/', views.brand_view, name='brand_view'),
]
