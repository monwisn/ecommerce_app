from django.http import HttpResponse
from django.shortcuts import render


def cart_summary(request) -> HttpResponse:
    return render(request, 'cart/cart_summary.html', {})


def cart_add(request) -> HttpResponse:
    pass


def cart_update(request) -> HttpResponse:
    pass


def cart_delete(request) -> HttpResponse:
    pass
