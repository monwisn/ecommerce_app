from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import QuerySet

from .models import Product, Category
from .pagination import paginate_queryset


def all_products(request) -> HttpResponse:
    products: QuerySet[Product] = Product.objects.all().order_by('name')
    num_items: int = 12  # Number of items per page
    page_obj = paginate_queryset(request, products, num_items)
    return render(request, 'store.html', {'products': page_obj, 'page_obj': page_obj})


def category_list(request) -> HttpResponse:
    categories: QuerySet[Category] = Category.objects.all()
    return render(request, 'store/category_list.html', {'categories': categories})


def new_in(request) -> HttpResponse:
    # newest: QuerySet[Product] = Product.objects.all().order_by('-updated', 'created')[:8]
    newest: QuerySet[Product] = Product.objects.all().order_by('-updated', 'created')
    num_items: int = 12
    page_obj = paginate_queryset(request, newest, num_items)
    return render(request, 'store.html', {'products': page_obj, 'page_obj': page_obj})


def on_sale(request) -> HttpResponse:
    sale: QuerySet[Product] = Product.objects.all().filter(is_sale=True)
    num_items: int = 8  # Number of items per page
    page_obj = paginate_queryset(request, sale, num_items)
    return render(request, 'store.html', {'products': page_obj, 'page_obj': page_obj})


def treats(request) -> HttpResponse:
    treat: QuerySet[Product] = Product.objects.all().filter(category__name='Treats')
    num_items: int = 12
    page_obj = paginate_queryset(request, treat, num_items)
    return render(request, 'store.html', {'products': page_obj, 'page_obj': page_obj})


def brand_products(request) -> HttpResponse:
    brands: QuerySet[Product] = Product.objects.all().values_list('brand', flat=True).distinct().order_by('brand')
    # flat parameter ensures that the values are returned as a flat list rather than a tuple.
    # distinct() func returns list of objects without repeats.
    products = Product.objects.all()
    num_items: int = 8
    page_obj = paginate_queryset(request, brands, num_items)
    return render(request, 'store/brand_list.html', {'brands': page_obj, 'page_obj': page_obj, 'products': products})
