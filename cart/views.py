from django.contrib import messages
from django.db.models import QuerySet
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from cart.models import CartProduct
from store.models import Product


def cart_summary(request) -> HttpResponse:
    cart_products: QuerySet[CartProduct] = CartProduct.objects.all()
    total_products: int = sum(CartProduct.objects.all().values_list('counter', flat=True))
    cart: CartProduct = CartProduct.objects.first()  # Retrieve the cart object

    return render(request, 'cart/cart_summary.html', {'cart_products': cart_products,
                                                      'total_products': total_products,
                                                      'cart': cart,
                                                      })


def cart_add(request, product_id: int) -> HttpResponse:
    product: Product = get_object_or_404(Product, pk=product_id)
    cart_product, created = CartProduct.objects.get_or_create(product=product)
    messages.info(request, 'Product has been added to your cart.')
    if not created:
        cart_product.counter += 1
        cart_product.save()
    return redirect(request.META.get('HTTP_REFERER'))


def cart_update(request) -> HttpResponse:
    pass


def cart_delete(request, product_id: int) -> HttpResponse:
    pass
