from typing import List
from django.contrib import admin

from store.models import Category, Customer, Product, Order, FavoriteProduct, DiscountCoupon

# admin.site.register(Category)
# admin.site.register(Customer)
# admin.site.register(Product)
admin.site.register(Order)
# admin.site.register(FavoriteProduct)
# admin.site.register(DiscountCoupon)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    model: Category = Category
    fields: list[str] = ['name', 'slug']
    list_display: list[str] = ['name', 'slug']


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    model: Customer = Customer
    list_display: list[str] = ['username', 'first_name', 'last_name', 'email', 'phone', 'street', 'address', 'postal_code',
                               'city', 'additional_info', 'instagram', 'dog_name']
    search_fields = ['last_name', 'email', 'postal_code', 'city', 'instagram', 'dog_name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    model: Product = Product
    fields: list[str] = ['name', 'price', 'quantity', 'brand', 'category', 'description', 'image', 'is_sale', 'sale_price']
    list_display: list[str] = ['name', 'price', 'quantity', 'is_sale', 'sale_price', 'brand', 'category', 'created', 'updated']
    list_filter: list[str] = ['brand', 'category', 'is_sale']
    search_fields: list[str] = ['name', 'brand', 'category']


@admin.register(FavoriteProduct)
class FavoriteProductAdmin(admin.ModelAdmin):
    list_display: List[str] = ['product', 'user', 'add_date']


@admin.register(DiscountCoupon)
class DiscountCouponAdmin(admin.ModelAdmin):
    list_display: List[str] = ['code', 'valid_from', 'valid_to', 'discount', 'is_active', 'created']
    list_filter: List[str] = ['is_active']
