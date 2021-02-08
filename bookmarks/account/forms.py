from django import forms


class LoginForm(forms.Form):
    """ Authenticates users against the database. """
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)