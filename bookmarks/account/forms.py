from django import forms
from django.contrib.auth.models import User

from .models import Profile


class LoginForm(forms.Form):
    """ Authenticates users against the database. """
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    """ Registers new user with username, password, firstname, and email. """
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        # Uses Django's auth. model.
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_password2(self):
        """ Verifies that both passwords match. """
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords do not match!')
        return cd['password2']


class UserEditForm(forms.ModelForm):
    """ Allows users to edit their names and email. """
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileEditForm(forms.ModelForm):
    """ Allows users to edit their DOB and profile photo. """
    class Meta:
        model = Profile
        fields = ('date_of_birth', 'photo')
