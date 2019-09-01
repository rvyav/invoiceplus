from decimal import Decimal
from django.conf import settings
from service.models import Service

class Cart(object):

	def __init__(self, request):
		"""Initialize the cart with the request."""
		# store the current session
		self.session = request.session

		# try to get the cart from the current session
		cart = self.session.get(settings.CART_SESSION_ID)
		if not cart:
			# save an empty cart in the session
			cart = self.session[settings.CART_SESSION_ID] = {}
		self.cart = cart


	def add(self, service, quantity=1, update_quantity=False):
		"""Add a service to the cart or update its quantity."""
		service_id = str(service.id)

		if service_id not in self.cart:
			self.cart[service_id] = {'quantity': 0, 'price':str(service.price)}

		if update_quantity:
			self.cart[service_id]['quantity'] = quantity
		else:
			self.cart[service_id]['quantity'] += quantity
		self.save()

	def save(self):
		# mark the session as "modified" to make sure it gets saved
		self.session.modified = True


	def remove(self, service):
		"""Remove a service from the cart."""
		service_id = str(service.id)

		if service_id in self.cart:
			del self.cart[service_id]
			
			# save the state of item being removed from cart
			self.save()


	def __iter__(self):
		"""
		Iterate over the items in the cart and get the services
		from the database.
		"""
		service_ids = self.cart.keys()

		# get the service objects and add them to the cart
		services = Service.objects.filter(id__in=service_ids)

		cart = self.cart.copy()

		for service in services:
			cart[str(service.id)]['service'] = service

		for item in cart.values():
			item['price'] = Decimal(item['price'])
			item['total_price'] = item['price'] * item['quantity']
			yield item

	def __len__(self):
		"""Count all items in the cart."""
		# Return the sum of the quantities of all the cart items.
		return sum(item['quantity'] for item in self.cart.values())

	def get_total_price(self):
		"""Calculate the total price of items in the cart."""
		return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())


	def clear(self):
		# remove cart after session
		del self.session[settings.CART_SESSION_ID]
		self.save()

