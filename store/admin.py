from typing import List
from django.contrib import admin

from store.models import Category, Customer, Product, Order, FavoriteProduct

# admin.site.register(Category)
# admin.site.register(Customer)
# admin.site.register(Product)
admin.site.register(Order)
# admin.site.register(FavoriteProduct)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    model: Category = Category
    fields: list[str] = ['name']
    list_display: list[str] = ['name']


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    model: Customer = Customer
    list_display: list[str] = ['username', 'first_name', 'last_name', 'email', 'phone', 'street', 'address', 'postal_code',
                               'city', 'additional_info', 'instagram', 'dog_name']
    search_fields = ['last_name', 'email', 'postal_code', 'city', 'instagram', 'dog_name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    model: Product = Product
    fields: list[str] = ['name', 'price', 'brand', 'category', 'description', 'image', 'is_sale', 'sale_price']
    list_display: list[str] = ['name', 'price', 'is_sale', 'sale_price', 'brand', 'category', 'created', 'updated']
    list_filter: list[str] = ['brand', 'category', 'is_sale']
    search_fields: list[str] = ['name', 'brand', 'category']


# @admin.register(Order)
# class OrderAdmin(admin.ModelAdmin):
#     model = Order


@admin.register(FavoriteProduct)
class FavoriteProductAdmin(admin.ModelAdmin):
    list_display: List[str] = ['product', 'user', 'add_date']
