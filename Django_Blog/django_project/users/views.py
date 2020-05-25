from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm

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

    if request.method == 'POST':
        # Set current user and profile for form, and pass POST data
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            messages.success(request, f"Your account has been updated!")
            # Redirect (POST/GET redirect pattern; causes browser to send GET request.)
            return redirect('profile')

    else:
        # Set current user and profile for form.
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)


    context = {
        'u_form' : user_form,
        'p_form' : profile_form
    }

    return render(request, 'users/profile.html', context=context)