from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        # Specify type of model and what field (and order) we will get.
        model = User
        fields = ['username', 'email', 'password1', 'password2']