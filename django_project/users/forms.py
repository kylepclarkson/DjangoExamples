from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from.models import Profile
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        # Specify type of model and what field (and order) we will get.
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    """ Form for updating username and email. """
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    """ Form for updating image. """
    class Meta:
        model = Profile
        fields = ['image']