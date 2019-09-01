from django.contrib import admin
from .models import Category, Service


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ['name', 'slug']
	prepolulated_fields = {'slug', ('name',)}


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
	list_display = [
			'name', 
			'slug', 
			'price',
			'available',
			'created',
			'updated' 
	]

	list_filter = [
			'available',
			'created',
			'updated',
	]

	list_editable = ['price', 'available']

	prepolulated_fields = {'slug', ('name',)}


