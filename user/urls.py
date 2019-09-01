from django.contrib import admin

from django.conf.urls import (
    handler404, 
    handler500
)

from django.urls import path, include
from . import views

handler404 = 'user.views.custom_404'
handler500 = 'user.views.custom_500'


app_name = 'user'
urlpatterns = [
	path('', views.index, name='index'),	
	path('login/', views.login_view, name='login'),
	path('logout/', views.logout_view, name='logout'),
	path('list-of-invoices/', views.list_invoices, name='list_invoices'),
	path('detail-invoice/', views.detail_invoice, name='detail_invoice'),
	path('profile/', views.customer_profile, name='customer_profile'),
]