from cart.models import CartProduct
from store.models import Product


class Cart:
    def __init__(self, request):
        self.session = request.session
        # Get current session key if it exists
        cart = self.session.get('session_key')  # or change 'session_key' to 'cart'
        # If the User is new, no session key -> create session
        if 'session_key' not in self.session:
            cart = self.session['session_key'] = {}
        # Check if cart is available on all pages of site
        self.cart = cart

    def add_to_cart(self, product_id, product):
        product_id = str(product_id)
        # Check if the product is already in the cart
        if product_id in self.cart:
            # Increment the quantity if the product is already in the cart
            self.cart[product_id]['quantity'] += 1
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
        # Save the updated cart back to the session
        self.save()

    def remove_from_cart(self, product_id):
        # Remove product from cart
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
        # Remove all products from cart
        self.cart = {}
        self.save()

    def get_total_price(self):
        # Get total price of all cart products
        return round(sum((item['sale_price']) * item['quantity'] for item in self.cart.values()), 2)

    def get_total_price_with_shipping(self):
        shipping_price = 12.99
        total = self.get_total_price()
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

    def save(self):
        # Save changes
        self.session.modified = True


