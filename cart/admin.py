from typing import List
from django.contrib import admin

from cart.models import CartProduct


@admin.register(CartProduct)
class CartProductAdmin(admin.ModelAdmin):
    list_display: List[str] = ['product', 'counter']
