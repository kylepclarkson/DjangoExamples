from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
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
            messages.success(request, f'Account created! Please log in!')
            # Redirect user
            return redirect('blog-home')
    else:
        print("else")
        form = UserRegisterForm()
    return render(request, 'users/register.html', context={'form':form})


# Require that user is logged in to view profile page.
@login_required()
def profile(request):
    """ View for Users profile. """
    return render(request, 'users/profile.html')