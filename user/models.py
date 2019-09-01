from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models


User = settings.AUTH_USER_MODEL


class User(AbstractUser):
	is_customer = models.BooleanField(default=True)

class Customer(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
	phone_number = models.CharField(max_length=10)
	city = models.CharField(max_length=30)
	state = models.CharField(max_length=30)
	postal_code = models.CharField(max_length=30)
	active = models.BooleanField(default=False)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.user.username
	

	# def get_absolute_url(self):
	# 	return reverse('user:customer_detail', kwargs={'pk': self.pk })

class Manager(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
	title = models.CharField(max_length=50)
	company_name = models.CharField(max_length=30)
	active = models.BooleanField(default=False)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.user.username
