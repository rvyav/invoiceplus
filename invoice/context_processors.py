from .cart import Cart

def cart(request):
	"""Set the current cart into the request context."""
	return {'cart': Cart(request)}