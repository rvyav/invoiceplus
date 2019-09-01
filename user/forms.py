from django import forms
from django.contrib.auth import authenticate, get_user_model
from .models import Customer, Manager


User = get_user_model()


class UserForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email')



class ManagerForm(forms.ModelForm):
	class Meta:
		model = Manager
		fields = ('title', 'company_name')


class UserLoginForm(forms.Form):
    """Validate Login form username and password."""
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('This user does not exist')
            if not user.check_password(password):
                raise forms.ValidationError('Incorrect password')
            if not user.is_active:
                raise forms.ValidationError('This user is not active')
        return super(UserLoginForm, self).clean(*args, **kwargs)














