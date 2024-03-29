import random
from typing import Optional, List
from urllib.parse import urlencode

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, Page
from django.http import HttpResponse, QueryDict
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import QuerySet, Q

from cart.cart import Cart
from .models import Product, Category, FavoriteProduct
from .pagination import paginate_queryset


def all_products(request) -> HttpResponse:
    cart: Cart = Cart(request)
    products: QuerySet[Product] = Product.objects.all().order_by('name')
    num_items: int = 4  # Number of items per page
    page_obj: list[QuerySet] = paginate_queryset(request, products, num_items)

    # if request.user.is_authenticated:
    #     favorite_list: QuerySet[FavoriteProduct] = FavoriteProduct.objects.filter(user=request.user).values_list(
    #         'product', flat=True).distinct()
    #     return render(request, 'store.html',
    #                   {'products': page_obj, 'page_obj': page_obj, 'favorite_list': favorite_list})

    return render(request, 'store.html', {'products': page_obj,
                                          'page_obj': page_obj,
                                          'cart': cart,
                                          })


def category_list(request) -> HttpResponse:
    categories: QuerySet[Category] = Category.objects.all()
    num_items: int = 8
    page_obj: list[QuerySet] = paginate_queryset(request, categories, num_items)
    return render(request, 'store/category_list.html', {'categories': page_obj, 'page_obj': page_obj})


def category_view(request, slug) -> HttpResponse:
    # categories: Category = get_object_or_404(Category, pk=pk)
    categories: Category = get_object_or_404(Category, slug=slug)
    products: QuerySet[Product] = Product.objects.filter(category=categories)
    num_items: int = 8
    page_obj: list[QuerySet] = paginate_queryset(request, products, num_items)
    return render(request, 'store.html', {'products': page_obj, 'page_obj': page_obj})


def new_in(request) -> HttpResponse:
    # newest: QuerySet[Product] = Product.objects.all().order_by('-updated', 'created')[:8]  # first 8 items
    newest: QuerySet[Product] = Product.objects.all().order_by('-updated', 'created')
    num_items: int = 8
    page_obj: list[QuerySet] = paginate_queryset(request, newest, num_items)
    return render(request, 'store.html', {'products': page_obj, 'page_obj': page_obj})


def on_sale(request) -> HttpResponse:
    sale: QuerySet[Product] = Product.objects.all().filter(is_sale=True).order_by('-updated', 'created')
    num_items: int = 8  # Number of items per page
    page_obj: list[QuerySet] = paginate_queryset(request, sale, num_items)
    return render(request, 'store.html', {'products': page_obj, 'page_obj': page_obj})


# def treats(request) -> HttpResponse:
#     treat: QuerySet[Product] = Product.objects.all().filter(category__name='Treats')
#     num_items: int = 12
#     page_obj: list[QuerySet] = paginate_queryset(request, treat, num_items)
#     return render(request, 'store.html', {'products': page_obj, 'page_obj': page_obj})


def brand_products(request) -> HttpResponse:
    brands: QuerySet[Product] = Product.objects.all().values_list('brand', flat=True).distinct().order_by('brand')
    # flat parameter ensures that the values are returned as a flat list rather than a tuple.
    # distinct() func returns list of objects without repeats.
    num_items: int = 8
    page_obj: list[QuerySet] = paginate_queryset(request, brands, num_items)
    return render(request, 'store/brand_list.html', {'brands': page_obj, 'page_obj': page_obj})


def brand_view(request, name) -> HttpResponse:
    products: QuerySet[Product] = Product.objects.filter(brand=name)
    num_items: int = 8
    page_obj: list[QuerySet] = paginate_queryset(request, products, num_items)
    return render(request, 'store.html', {'products': page_obj, 'page_obj': page_obj})


def add_to_favorites(request, product_id: int) -> HttpResponse:
    product: Product = Product.objects.get(id=product_id)
    favorite_exists: bool = FavoriteProduct.objects.filter(user=request.user, product=product).exists()
    if not favorite_exists:
        favorite_product: FavoriteProduct = FavoriteProduct(user=request.user, product=product)
        favorite_product.save()
        messages.info(request, 'Product successfully added to favorites list.')
    else:
        messages.warning(request, 'This product already exists in your favorites list.')
    return redirect(request.META.get('HTTP_REFERER'))  # http header referer- redirect to referring header
    # return redirect("store:all_products")


def remove_from_favorites(request, product_id: int) -> HttpResponse:
    product: Product = Product.objects.get(id=product_id)
    favorite_exists: bool = FavoriteProduct.objects.filter(user=request.user, product=product).exists()
    if favorite_exists:
        favorite_product: FavoriteProduct = FavoriteProduct.objects.get(product_id=product_id, user=request.user)
        favorite_product.delete()
        messages.info(request, f'Product successfully removed from favorites list.')
    else:
        messages.warning(request, 'This product is not in favorites list, you cannot remove it.')
    return redirect(request.META.get('HTTP_REFERER'))
    # return redirect("store:all_products")


@login_required(login_url='main:login')
def fav_list(request) -> HttpResponse:
    favorites: QuerySet[FavoriteProduct] = FavoriteProduct.objects.filter(user=request.user).order_by('-add_date')
    num_items: int = 8
    page_obj: list[QuerySet] = paginate_queryset(request, favorites, num_items)
    return render(request, 'store/favorite_products_list.html', {'favorites': page_obj, 'page_obj': page_obj})


def product(request, product_id: int) -> HttpResponse:
    prod: Product = Product.objects.get(id=product_id)
    # Get recently viewed product in session
    recently_viewed: List[int] = request.session.get('recently_viewed', [])
    recently_viewed_products = None

    # If product already in recently_viewed list then delete this product, and insert it on index 0
    if 'recently_viewed' in request.session:
        if product_id in recently_viewed:
            recently_viewed.remove(product_id)

        recently_viewed_products = Product.objects.filter(pk__in=recently_viewed)

        # Sort products from last viewed to the oldest one in recently_viewed list
        recently_viewed_products = sorted(recently_viewed_products, key=lambda x: recently_viewed.index(x.id))
        recently_viewed.insert(0, product_id)

        # If recently viewed products list is more than 5, then delete the last product from this list (the oldest one)
        if len(recently_viewed) > 5:
            recently_viewed.pop()
    else:
        request.session['recently_viewed'] = [product_id]
    # Save changes in session
    request.session.modified = True

    # related_products = Product.objects.filter(Q(category=prod.category) & ~Q(id=product_id))[:3]
    related_products: QuerySet[Product] = Product.objects.all().filter(category__name=prod.category.name).exclude(id=product_id)
    random_prod: list = []
    if related_products.count() > 3:
        random_prod: list[Product] = random.sample(list(related_products), 4)
    return render(request, 'store/product.html', {'product': prod,
                                                  'random': random_prod,
                                                  'related': related_products,
                                                  'recently': recently_viewed_products
                                                  })


def search_product(request) -> HttpResponse:
    # query: Optional[str] = request.GET.get('q')  # name of form input field
    # searched: Product = Product.objects.filter(Q(name__icontains=query) | Q(brand__icontains=query))
    #
    # return render(request, 'store.html', {'products': searched})

    query: Optional[str] = request.GET.get('q')
    searched: Product = Product.objects.filter(Q(name__icontains=query) | Q(brand__icontains=query))

    paginator: Paginator = Paginator(searched, 4)  # Set the number of items per page here
    page_number: Optional[str] = request.GET.get('page')
    page_obj: Page = paginator.get_page(page_number)

    context: dict = {
        'products': page_obj,
        'page_obj': page_obj,
        'query': query,
    }

    # Add the query and page number to the HTTP address
    base_url: str = request.path
    query_params: QueryDict = request.GET.copy()
    query_params['query'] = query
    query_params['page'] = page_number
    encoded_query_params: str = urlencode(query_params)
    full_url: str = f"{base_url}?{encoded_query_params}"
    context['full_url'] = full_url

    return render(request, 'store.html', context)


def sort_products(request) -> HttpResponse:
    products: QuerySet[Product] = Product.objects.all()

    # # Retrieve the sorting option from the session, or set a default option
    # sort_option = request.session.get('sort_option', 'newest')

    # Get the selected sorting option from the request parameters
    # sort_option: Optional[str] = request.GET['sort', 'name']
    sort_option: Optional[str] = request.GET.get('sort', 'name')  # default sort products by 'name'

    # Sort the products based on the selected option
    if sort_option == 'lowest':
        products = products.order_by('sale_price')
    elif sort_option == 'highest':
        products = products.order_by('-sale_price')
    elif sort_option == 'newest':
        products = products.order_by('-updated')
    elif sort_option == 'name':
        products = products.order_by('name')

    # # Save the sorting option in the session
    # cart.session['sort'] = sort_option
    # cart.save()
    #
    # num_items: int = 4  # Number of items per page
    # page_obj: list[QuerySet] = paginate_queryset(request, products, num_items)

    paginator: Paginator = Paginator(products, 4)
    page_number: Optional[str] = request.GET.get('page')
    page_obj: Page = paginator.get_page(page_number)

    context: dict = {
        'products': page_obj,
        'page_obj': page_obj,
        'sort_option': sort_option,
    }

    base_url: str = request.path
    query_params: QueryDict = request.GET.copy()
    query_params['sort'] = sort_option
    query_params['page'] = page_number
    encoded_query_params: str = urlencode(query_params)
    full_url: str = f"{base_url}?{encoded_query_params}"
    context['full_url'] = full_url

    return render(request, 'store.html', {'products': page_obj, 'page_obj': page_obj, 'sort_option': sort_option})

