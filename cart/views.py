from typing import List

from django.contrib import messages
from django.db.models import QuerySet
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from cart.models import CartProduct
from store.models import Product
from .cart import Cart


# Cart with session:

def cart_add(request, product_id: int) -> HttpResponse:
    cart: Cart = Cart(request)
    product: Product = get_object_or_404(Product, pk=product_id)
    cart.add_to_cart(product_id, product)
    messages.info(request, 'Product has been added to your cart.')
    return redirect(request.META.get('HTTP_REFERER'))


# def cart_add(request, product_id: int) -> HttpResponse:
#
#     # Get the product object based on the product_id
#     product: Product = Product.objects.get(id=product_id)
#
#     # Get the cart from the session, or create a new one if it doesn't exist
#     cart = request.session.get('session_key', {})
#
#     # Check if the product is already in the cart
#     if product_id in cart:
#         # Increment the quantity if the product is already in the cart
#         cart[product_id]['quantity'] += 1
#     else:
#         # Add the product to the cart with a quantity of 1
#         cart[product_id] = {
#             'name': product.name,
#             'price': float(product.price),
#             'sale_price': float(product.sale_price),
#             'brand': product.brand,
#             'image': product.image.url,
#             'quantity': 1
#         }
#     # Save the updated cart back to the session
#     request.session['session_key'] = cart
#     messages.info(request, 'Product has been added to your cart.')
#     return redirect(request.META.get('HTTP_REFERER'))


def cart_delete(request, product_id: int) -> HttpResponse:
    cart = Cart(request)
    product: Product = get_object_or_404(Product, pk=product_id)
    cart.remove_from_cart(product_id)
    messages.info(request, f'"{product.name}" has been successfully deleted.')
    return redirect(request.META.get('HTTP_REFERER'))


def cart_update(request, product_id: int) -> HttpResponse:
    cart = Cart(request)
    quantity = int(request.POST.get('quantity'))
    if product_id in cart:
        cart.update_quantity(product_id, quantity)
        messages.info(request, f'Product quantity has been updated.')
    return redirect(request.META.get('HTTP_REFERER'))


def session_cart_summary(request) -> HttpResponse:
    cart: Cart = Cart(request)
    total_price: float = 0
    total_with_shipping: float = 0
    total_products: int = 0
    shipping_price: float = 12.99
    cart_items: List[dict] = []
    for product_id, item in cart.cart.items():
        # Calculate the total price for each product
        product_price = item['quantity'] * float(item['sale_price'])
        total_price += product_price
        # Calculate all cart products
        total_products += item['quantity']
        cart_items.append({
            'product_id': int(product_id),
            'name': item['name'],
            'price': float(item['price']),
            'sale_price': float(item['sale_price']),
            'brand': item['brand'],
            'product_price': float(product_price),
            'quantity': item['quantity'],
            'image': item['image'],
            'stock': item['stock'],
        })
    # Calculate total price with shipping
    if 0 < total_price < 350.00:
        total_with_shipping = total_price + shipping_price
    else:
        total_with_shipping += total_price

    if str(request.user) is not 'AnonymousUser':
        fav_list = request.user.fav_product.all().values_list('favorites__user_fav__product_id', flat=True).distinct()
        return render(request, 'cart/session_cart_summary.html', {'total_price': round(total_price, 2),
                                                                  'total_with_shipping': round(total_with_shipping, 2),
                                                                  'cart_items': cart_items,
                                                                  'total_products': total_products,
                                                                  'shipping_price': shipping_price,
                                                                  'fav_list': fav_list,
                                                                  })
    else:
        return render(request, 'cart/session_cart_summary.html', {'total_price': total_price,
                                                                  'total_with_shipping': total_with_shipping,
                                                                  'cart_items': cart_items,
                                                                  'total_products': total_products,
                                                                  'shipping_price': shipping_price,
                                                                  })


# # Cart without session:

# def cart_add(request, product_id: int) -> HttpResponse:
#     """
#     Add a product to the cart.
#     """
#     product: Product = get_object_or_404(Product, pk=product_id)
#     cart_product, created = CartProduct.objects.get_or_create(product=product)
#     messages.info(request, 'Product has been added to your cart.')
#     if not created:
#         cart_product.counter += 1
#         cart_product.save()
#     return redirect(request.META.get('HTTP_REFERER'))
#
#
# def cart_delete(request, product_id: int) -> HttpResponse:
#     """
#     Remove a product from the cart.
#     """
#     product: Product = Product.objects.get(id=product_id)
#     cart_exists: bool = CartProduct.objects.filter(product=product).exists()
#     if cart_exists:
#         cart_product: CartProduct = CartProduct.objects.get(product_id=product_id)
#         cart_product.delete()
#         messages.info(request, f'"{cart_product.product.name}" successfully removed from cart.')
#     else:
#         messages.warning(request, 'This product is not in your cart, you cannot remove it.')
#     return redirect(request.META.get('HTTP_REFERER'))
#
#
# def cart_update(request, product_id: int) -> HttpResponse:
#     """
#     Update a cart product quantity.
#     """
#     cart_product: CartProduct = CartProduct.objects.get(product_id=product_id)
#     # Subtract 1 from the quantity
#     cart_product.counter -= 1
#     cart_product.save()
#     messages.info(request, f'Product quantity has been successfully updated.')
#     # If the quantity is now 0, then delete the item
#     if cart_product.counter == 0:
#         cart_product.delete()
#         messages.info(request, f'"{cart_product.product.name}" successfully removed from cart.')
#     return redirect(request.META.get('HTTP_REFERER'))
#
#
# def cart_summary(request) -> HttpResponse:
#     cart_products: QuerySet[CartProduct] = CartProduct.objects.all()
#     total_products: int = sum(CartProduct.objects.all().values_list('counter', flat=True))
#     cart: CartProduct = CartProduct.objects.first()  # Retrieve the cart object
#
#     return render(request, 'cart/cart_summary.html', {'cart_products': cart_products,
#                                                       'total_products': total_products,
#                                                       'cart': cart,
#                                                       })
