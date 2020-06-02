from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login

from .forms import LoginForm

# Attempt to login in user.
def user_login(request):
    # request method will be 'POST' or 'GET'
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data

            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                # user exists
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    # user's account is disabled.
                    return HttpResponse('Disabled account')

            else:
                return HttpResponse('Invalid login')
    else:
        # Set form for user to login
        form = LoginForm()

    return render(request, 'account/login.html', {'form': form})