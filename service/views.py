from django.shortcuts import (
		render, 
		redirect, 
		get_object_or_404
)

from django.contrib.auth.decorators import login_required

from django.http import Http404

import datetime

from django.contrib.auth import get_user_model


from invoice.models import Invoice, InvoiceItem

from invoice.forms import (
	CartAddServiceForm,
	SendInvoiceToDropDownForm

)


from django.views.decorators.http import require_POST

from .models import Service

from invoice.cart import Cart


from .models import (
	Category,
	Service,
)


from django.core.paginator import (
	Paginator, 
	EmptyPage,
	PageNotAnInteger
)


from django.db.models import Q


User = get_user_model()



def index(request):
	pass
	return render(request, 'service/index.html')


def home(request):
	pass
	return render(request, 'service/dashboard/home.html')

@login_required
def search(request):
	"""Search result."""
	query = request.GET.get('q')

	results = Invoice.objects.filter(Q(id__icontains=query)).distinct()

	context = {'results': results}

	return render(request, 'service/dashboard/manager/search.html', context)


@login_required
def invoice(request):
	"""List of invoices."""
	invoice_list = Invoice.objects.all()

	# Paginator
	paginator = Paginator(invoice_list, 5)

	page = request.GET.get('page')

	try:
		# create Page object for the given page
		invoice_list = paginator.page(page)

	except PageNotAnInteger:
		# If page is not an integer deliver first page
		invoice_list = paginator.page(1)
		
	except EmptyPage:
		# If page is out of range deliver last page of results
		invoice_list = paginator.page(paginator.num_pages)

	context = {
		'invoice_list':invoice_list,
		'page': page,
	}

	return render(request, 'service/dashboard/manager/invoices.html', context)	

@login_required
def add_invoice(request):
	"""
	create invoice and also display cart and items.
	"""
	if request.method == 'POST':
		cart = Cart(request)
		form = SendInvoiceToDropDownForm(request.POST or None)
		if form.is_valid():
			invoice = form.save()

			# persist item in cart
			for item in cart:
				InvoiceItem.objects.create(invoice=invoice,
											product=item['service'],
											price=item['price'],
											quantity=item['quantity']) 
			# clear the cart
			cart.clear()

			context = {'invoice':invoice}
			return render(request, 'service/dashboard/manager/created.html', context)

	else:
		form = SendInvoiceToDropDownForm()

	# Invoice Sender
	invoice_from = request.user

	# Today date
	today_date = datetime.datetime.today()

	cart = Cart(request)

	# Change service quantity before
	# placing an order
	for item in cart:
		# itinialize the form with the current quantity
		# and set the update field to True so that when
		# we submit the form to the cart_add view,
		# the current quantity is replaced with the new one.
		item['update_quantity_form'] = CartAddServiceForm(initial={'quantity': item['quantity'], 'update':True})


	context = {
			'form':form,
			'invoice_from': invoice_from,
			'cart': cart, 
			'today_date': today_date
	}
	

	return render(request, 'service/dashboard/manager/add_invoice.html', context)

@login_required
def invoice_detail(request, id):
	"""Include Foreign Key reverse look up."""
	invoice = get_object_or_404(Invoice, id=id)

	context = {'invoice':invoice}
	return render(request, 'service/dashboard/manager/invoice_detail.html', context)


@login_required
def select_item(request, id):
	"""Select invoice id on Invoice page."""
	invoice = get_object_or_404(Invoice, id=id)
	invoice.select = True
	invoice.save()

	return redirect('service:invoice')

@login_required
def unselect_item(request, id):
	"""Unselect invoice id on Invoice page."""
	invoice = get_object_or_404(Invoice, id=id)
	invoice.select = False
	invoice.save()

	return redirect('service:invoice')

@login_required
def delete_invoice(request, id):
	"""Delete invoice on Invoice page."""
	Invoice.objects.filter(select__exact=True).delete()

	return redirect('service:invoice')


@require_POST
def cart_add(request, service_id):
	"""
	Add service to cart or
	update quantities for existing services.
	"""
	cart = Cart(request)
	service = get_object_or_404(Service, id=service_id)
	form = CartAddServiceForm(request.POST)
	if form.is_valid():
		cd = form.cleaned_data
		cart.add(service=service, quantity=cd['quantity'], update_quantity=cd['update'])
	return redirect('service:add_invoice')

def cart_remove(request, service_id):
	"""Remove item from cart."""
	cart = Cart(request)
	service = get_object_or_404(Service, id=service_id)
	cart.remove(service)
	return redirect('service:add_invoice')

@login_required
def created(request):
	pass
	return render(request, 'service/dashboard/manager/created.html', context)

@login_required
def manager_profile(request):
	profile = User.objects.filter(manager=request.user.id)

	context = {'profile': profile }
	return render(request, 'service/dashboard/manager/manager_profile.html', context)

@login_required
def customer_list(request):
	customers = User.objects.filter(is_customer='True')

	context = {'customers':customers}
	return render(request, 'service/dashboard/manager/customer_list.html', context)


@login_required
def service_list(request, category_slug=None):
	"""
	List all the services.
	"""
	# Optional category_slug parameter 
	# used to filter by a given category
	category = None
	categories = Category.objects.all()
	services = Service.objects.filter(available=True)
	if category_slug:
		category = get_object_or_404(Category, slug=category_slug)
		services = services.filter(category=category)

	context = {
			'category':category,
			'categories': categories,
			'services':services,
	}
	return render(request, 'service/service_pages/list.html', context)

@login_required
def service_detail(request, id, slug):
	"""Detail of each service."""
	# Expect id and slug parameter to retrieve the
	# service instance.
	service = get_object_or_404(Service, id=id, slug=slug, available=True)

	# This will help add the cart button
	# to the service detail page.
	cart_service_form = CartAddServiceForm(request.POST)

	context = {
		'service':service,
		'cart_service_form':cart_service_form
	}

	return render(request, 'service/service_pages/detail.html', context)


def custom_404(request):
	"""Handle error 404."""
	return render(request, 'templates/404.html')

def custom_500(request):
	"""Handle error 500."""
	return render(request, 'templates/500.html')




























