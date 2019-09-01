from django.shortcuts import (
		render,
		redirect,
)

from .models import InvoiceItem


def index(request):
	return render(request, 'product/index.html')	
