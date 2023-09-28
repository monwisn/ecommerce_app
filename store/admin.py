from typing import Type

from django.contrib import admin
from django.db import models

from store.models import Category, Customer, Product, Order


# admin.site.register(Category)
admin.site.register(Customer)
# admin.site.register(Product)
admin.site.register(Order)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    model: Category = Category
    fields: list[str] = ['name']
    list_display: list[str] = ['name']


# @admin.register(Customer)
# class CustomerAdmin(admin.ModelAdmin):
#     model = Customer
#
#
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
