from django.contrib import admin
from .models import (
	Invoice, 
	InvoiceItem
)


class InvoiceItemInline(admin.TabularInline):
	model = InvoiceItem
	raw_id_fields = ['product']

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
	list_display = [
		'id',
		'user',
	]

	list_filter = ['is_paid', 'created', 'updated']
	inlines = [InvoiceItemInline]

