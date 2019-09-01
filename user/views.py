from django.shortcuts import (
	render,
	redirect,
	get_object_or_404
)


from django.http import Http404

from django.contrib.auth.decorators import login_required

from django.contrib.auth import authenticate, get_user_model

from django.contrib.auth import login, logout 

from .forms import UserLoginForm



def index(request):
	return render(request, 'user/index.html')	

def login_view(request):
    next = request.GET.get('next')
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password) 

        if user.is_active:
            if user.is_superuser or user.is_staff:
                login(request, user)
                return redirect('service:invoice')
            else:
                login(request, user)
                return redirect('user:list_invoices')

    context = {'form': form}
    return render(request, 'user/registration/login.html', context)


def logout_view(request):
	logout(request)
	return redirect('user:login')

@login_required
def list_invoices(request):
    pass
    return render(request, 'user/customer/list_invoices.html', context)

@login_required
def detail_invoice(request):
    pass
    return render(request, 'user/customer/list_invoices.html', context)

@login_required
def customer_profile(request):
    pass
    return render(request, 'user/customer/customer_profile.html', context)


def custom_404(request):
    """Handle error 404."""
    return render(request, 'templates/404.html')

def custom_500(request):
    """Handle error 500."""
    return render(request, 'templates/500.html')









