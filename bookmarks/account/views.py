from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

# from .forms import LoginForm
from .forms import UserRegistrationForm

@login_required
def dashboard(request):
    # Redirects user to dashboard.
    return render(request, 'account/dashboard.html', {'section': 'dashboard'})

def register(request):
    # Register new user.
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)

        if user_form.is_valid():
            # Create user, set password, then save.
            new_user = user_form.save(commit=False)
            new_user.set_password(
                user_form.cleaned_data['password2']     # set_password hashes password.
            )
            new_user.save()

            return render(request,
                          'account/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()

    return render(request,
                  'account/register.html',
                  {'user_form': user_form})


# Attempt to login in user.
# Custom login view. Replaced by using Django's login
# def user_login(request):
#     # request method will be 'POST' or 'GET'
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#
#         if form.is_valid():
#             cd = form.cleaned_data
#
#             user = authenticate(request,
#                                 username=cd['username'],
#                                 password=cd['password'])
#             if user is not None:
#                 # user exists
#                 if user.is_active:
#                     login(request, user)
#                     return HttpResponse('Authenticated successfully')
#                 else:
#                     # user's account is disabled.
#                     return HttpResponse('Disabled account')
#
#             else:
#                 return HttpResponse('Invalid login')
#     else:
#         # Set form for user to login
#         form = LoginForm()
#
#     return render(request, 'account/login.html', {'form': form})
