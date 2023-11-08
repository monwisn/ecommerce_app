
class Cart:
    def __init__(self, request):
        self.session = request.session

        # Get current session key if it exists
        cart = self.session.get('session_key')

        # If the User is new, no session key -> create session
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        # Check if cart is available on all pages of site
        self.cart = cart

