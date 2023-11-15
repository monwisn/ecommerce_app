from django.db import models

from store.models import Product


class CartProduct(models.Model):
    product: Product = models.ForeignKey(Product, on_delete=models.CASCADE)
    counter: int = models.PositiveIntegerField(default=1, verbose_name='quantity')

    @property
    def total_product_price(self):
        return self.counter * self.product.sale_price
