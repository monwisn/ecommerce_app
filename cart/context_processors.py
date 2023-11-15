from .cart import Cart


# Create context processor - our cart can work on all pages of the site
def cart(request) -> dict:
    return {'cart': Cart(request)}  # Return the default data from Cart
