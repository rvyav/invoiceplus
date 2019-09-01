from django.contrib import admin

from django.conf.urls import (
    handler404, 
    handler500
)

from django.urls import path, include
from . import views

handler404 = 'service.views.custom_404'
handler500 = 'service.views.custom_500'


app_name = 'service'
urlpatterns = [
	path('', views.index, name='index'),
	path('home/', views.home, name='home'),
	# Manager
	path('invoices/', views.invoice, name='invoice'),
	path('invoices/<int:id>/', views.invoice_detail, name='invoice_detail'),
	path('add-invoice/', views.add_invoice, name='add_invoice'),	
	path('select/<int:id>/', views.select_item, name='select_item'),
	path('unselect/<int:id>/', views.unselect_item, name='unselect_item'),
	path('delete-invoice/<int:id>/', views.delete_invoice, name='delete_invoice'),	
	path('add/<int:service_id>/', views.cart_add, name='cart_add'),
	path('search/results/', views.search, name='search'),
	path('remove/<int:service_id>/', views.cart_remove, name='cart_remove'),
	path('created/', views.created, name='created'),
	path('customer-list/', views.customer_list, name='customer_list'),
	path('manager/profile/', views.manager_profile, name='manager_profile'),
	path('services/', views.service_list, name='service_list'),	
	path('<slug:category_slug>/', views.service_list, name='service_list_by_category'),
	path('<int:id>/<slug:slug>/', views.service_detail, name='service_detail'),
	
]
