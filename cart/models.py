from django.db import models

from store.models import Product


class CartProduct(models.Model):
    product: Product = models.ForeignKey(Product, on_delete=models.CASCADE)
    counter: int = models.PositiveIntegerField(default=1, verbose_name='quantity')

    @property
    def total_product_price(self) -> float:
        return self.counter * self.product.sale_price


    def get_total_cost(self) -> float:
        total_cost: float = 0
        for cart_product in CartProduct.objects.all():
            total_cost += cart_product.product.sale_price * cart_product.counter
        return total_cost


    def get_total_with_shipping(self) -> float:
        shipping: float = 12.99
        total_with_shipping = float(self.get_total_cost())

        if total_with_shipping < 500.00:
            total_with_shipping += shipping
        return total_with_shipping


