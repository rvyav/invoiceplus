from django.conf import settings
from django.db.models import Max
from django.db import models
from service.models import Service


User = settings.AUTH_USER_MODEL


class Invoice(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_invoices')
	select = models.BooleanField(default=False, null=True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	is_paid = models.BooleanField(default=False)

	class Meta:
		ordering = ('-created',)

	def __str__(self):
		return '{}'.format(self.id)

	# def get_date(self):
	# 	return self.modified.date()

	def get_absolute_url(self):
		return reverse('product:service_detail', kwargs=[self.id, self.slug])


	def get_total_cost(self):
		return sum(item.get_cost() for item in self.items.all())

class InvoiceItem(models.Model):
	invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
	product = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='invoice_items')
	price = models.DecimalField(max_digits=10, decimal_places=2)
	quantity = models.PositiveIntegerField(default=1)

	# def __str__(self):
	# 	return '{}'.format(self.id)

	def get_cost(self):
		return self.price * self.quantity



