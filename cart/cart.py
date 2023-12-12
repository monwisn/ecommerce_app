import datetime
from django.contrib import messages

from ecommerce_app.settings import CART_SESSION_ID
from store.models import Product


class Cart:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        cart = self.session.get(CART_SESSION_ID)
        if not cart:
            cart = self.session[CART_SESSION_ID] = {}
        self.cart = cart

        # or:
        # self.request = request
        # self.session = request.session
        # # Get current session key if it exists
        # cart = self.session.get('session_key')  # or change 'session_key' to 'cart'
        # # If the User is new, no session key -> create session
        # if 'session_key' not in self.session:
        #     cart = self.session['session_key'] = {}
        # # Check if cart is available on all pages of site
        # self.cart = cart

    def add_to_cart(self, product_id, product):
        product_id = str(product_id)
        # Check if the product is already in the cart
        if product_id in self.cart:
            # Check if max stock added to cart
            if self.cart[product_id]['quantity'] == self.cart[product_id]['stock']:
                messages.error(self.request, 'You can\'t add more product to the cart.')
            # Increment the quantity if the product is already in the cart
            else:
                self.cart[product_id]['quantity'] += 1
                messages.info(self.request, f'Product quantity has been updated.')
        else:
            # Add the product to the cart with a quantity of 1
            self.cart[product_id] = {
                'name': product.name,
                'price': float(product.price),
                'sale_price': float(product.sale_price),
                'brand': product.brand,
                'image': product.image.url,
                'quantity': 1,
                'stock': product.quantity,
            }
            messages.info(self.request, 'Product has been added to your cart.')
        # Save the updated cart back to the session
        self.save()

    def remove_from_cart(self, product_id):
        # Remove product from the cart
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def update_quantity(self, product_id, quantity):
        # Update cart product quantity
        product_id = str(product_id)
        if product_id in self.cart:
            self.cart[product_id]['quantity'] = quantity
            self.save()

    def clear_cart(self):
        # Remove all products from the cart
        # The 'None' argument is provided as the default value to avoid raising a 'KeyError' if
        # the 'coupon_code' key does not exist in the session.
        self.session.pop('coupon_code', None)
        self.cart.clear()
        # self.cart = {}
        self.save()

    def get_total_price(self):
        # Get total price of all cart products
        return round(sum((item['sale_price']) * item['quantity'] for item in self.cart.values()), 2)

    def get_total_price_with_shipping(self):
        shipping_price = 12.99
        total = self.get_total_price()
        if self.get_coupon_code() is not None:
            total = self.total_price_after_discount()
        if total < 350.00:
            total += shipping_price
        return round(total, 2)

    def __len__(self):
        # Get the length of cart products = cart products quantity
        return sum(item['quantity'] for item in self.cart.values())

    def get_products(self):
        # Get ids from cart
        product_ids = self.cart.keys()
        # Use ids to lookup products in database model
        products = Product.objects.filter(id__in=product_ids)
        # Return those looked up products
        return products

    def __iter__(self):
        # Get the total price of each cart product
        for item in self.cart.values():
            item['total_price'] = item['sale_price'] * item['quantity']
            yield item

    def add_coupon(self, coupon):
        # Only retrieve codes that are in the database and check if the "valid_to" field has expired.
        if coupon:
            # Add discount coupon to the cart
            self.request.session['coupon_code'] = {
                'code': coupon.code,
                'discount': coupon.discount,
                'valid_to': coupon.valid_to.strftime("%Y-%m-%d %H:%M:%S"),
                'added': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            messages.success(self.request, f'"{coupon.code}" has been successfully added to cart. Code is valid to: '
                                           f'{coupon.valid_to.strftime("%H:%M %p, %d %b %Y")}.')
        else:
            messages.error(self.request, f'Discount code does not exist or has expired.')
        self.save()

    def delete_coupon(self):
        # Delete the coupon code from the cart
        if 'coupon_code' in self.request.session:
            del self.request.session['coupon_code']
            self.save()

    def get_coupon_code(self):
        return self.request.session.get('coupon_code')

    def calculate_discount(self):
        # Calculate the discount amount
        amount = self.request.session['coupon_code']['discount']
        discount = self.get_total_price() * amount / 100
        return round(discount, 2)

    def total_price_after_discount(self):
        # Calculate the total price after discount coupon
        total_after_discount = self.get_total_price() - self.calculate_discount()
        return round(total_after_discount, 2)

    def save(self):
        # Save changes
        self.session.modified = True
