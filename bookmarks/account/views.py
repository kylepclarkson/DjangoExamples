from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# from .forms import LoginForm
from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile

@login_required
def dashboard(request):
    # Redirects user to dashboard.
    return render(request, 'account/dashboard.html', {'section': 'dashboard'})


# Allows for registering new user.
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

            # Create profile for user
            Profile.objects.create(user=new_user)

            return render(request,
                          'account/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()

    return render(request,
                  'account/register.html',
                  {'user_form': user_form})

# Allows for editing of profile.
@login_required
def edit(request):

    if request.method == 'POST':

        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            # Update User and Profile models.
            user_form.save()
            profile_form.save()

            messages.success(request, 'Profile updated successfully.')

        else:
            messages.error(request, 'Error updating your profile. ')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    return render(request,
                  'account/edit.html',
                  {'user_form': user_form,
                   'profile_form': profile_form})

@login_required
def user_list(request):
    # Get all active users
    users = User.objects.filter(is_active=True)

    return render(request,
                  'account/user/list.html',
                  {'section': 'people',
                   'users': users})

@login_required
def user_detail(request, username):
    # Get active user with specified username.
    user = get_object_or_404(User,
                             username=username,
                             is_active=True)

    return render(request,
                  'account/user/detail.html',
                  {'section': 'people',
                   'user': user})


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
