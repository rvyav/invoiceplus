from django.db import models
from django.utils.text import slugify
from django.urls import reverse

class Category(models.Model):
	name = models.CharField(max_length=200, db_index=True)
	slug = models.SlugField(unique=True, max_length=200, db_index=True)
	image = models.ImageField(upload_to='category_pics', blank=True)
		
	class Meta:
		ordering = ('name',)
		verbose_name = ('category')
		verbose_name_plural = 'categories'

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('service:service_list_by_category', args=[self.slug])

class Service(models.Model):
	category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='services')
	name = models.CharField(max_length=200, db_index=True)
	slug = models.SlugField(unique=True, max_length=200, db_index=True)
	description = models.TextField(blank=True)
	price = models.DecimalField(max_digits=10, decimal_places=2)
	available = models.BooleanField(default=True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ('name',)
		index_together = (('id', 'slug'),)

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('service:service_detail', args=[self.id, self.slug])
