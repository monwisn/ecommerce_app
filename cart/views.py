from django.http import HttpResponse
from django.shortcuts import render

from store.models import Product


def cart_summary(request) -> HttpResponse:
    products = Product.objects.all()[0:4]
    total = Product.objects.all().values_list('price', flat=True).distinct()

    return render(request, 'cart/cart_summary.html', {'products': products, 'total': total})


def cart_add(request) -> HttpResponse:
    pass


def cart_update(request) -> HttpResponse:
    pass


def cart_delete(request) -> HttpResponse:
    pass
