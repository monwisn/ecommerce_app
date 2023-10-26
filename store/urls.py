from django.urls import path
from . import views


app_name: str = 'store'

urlpatterns: list = [
    path('', views.all_products, name='all_products'),
    path('categories/', views.category_list, name='category_list'),
    # path('category/<int:pk>/', views.category_view, name='category_view'),
    path('category/<slug:slug>/', views.category_view, name='category_view'),
    path('new/', views.new_in, name='new_in'),
    path('sale/', views.on_sale, name='on_sale'),
    # path('treats/', views.treats, name='treats'),
    path('brands/', views.brand_products, name='brands'),
    path('brands/<str:name>/', views.brand_view, name='brand_view'),
    path('add-to-favorites/<int:product_id>/', views.add_to_favorites, name='add_to_favorites'),
    path('remove-from-favorites/<int:product_id>/', views.remove_from_favorites, name='remove_from_favorites'),
    path('favorite-products/', views.fav_list, name='fav_list'),
    path('product/<int:pk>/', views.product, name='product'),
]
