from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm

# Create your views here.

def register(request):
    """ Form to create new user. """
    if request.method == 'POST':
        # User is creating account.
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            # Save contents of form to database.
            form.save()
            username = form.cleaned_data.get('username')
            # Flash message to user that account is being created.
            messages.success(request, f'Account created for {username}')
            # Redirect user
            return redirect('blog-home')
    else:
        print("else")
        form = UserRegisterForm()
    return render(request, 'users/register.html', context={'form':form})