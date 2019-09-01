from django.contrib.auth import get_user_model
from django.forms import ModelChoiceField
from django import forms
from .models import Invoice

User = get_user_model()


class CartAddServiceForm(forms.Form):
	"""Add service to the cart between quantity 1-20."""
	SERVICE_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)] 

	# allow user to select quantity between 1-20
	quantity = forms.TypedChoiceField(choices=SERVICE_QUANTITY_CHOICES, coerce=int)
	# This indicate whether the quantity has to be added to the cart (False)
	# quantity has to be updated with the quantity (True)
	update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)



class SendInvoiceToDropDownForm(forms.ModelForm):
	"""Save Username to send invoice to."""
	# Choice DropDown to select
	# customer to send to
	user = forms.ModelChoiceField(queryset=User.objects.order_by('id').filter(is_customer='True'))

	class Meta:
		model = Invoice
		fields = ('user',)
		labels = {'user': 'Username'}

