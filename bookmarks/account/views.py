from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile


def user_login(request):
    """ Handle user login. If method is GET, user will fill out form.
    If method is POST, user has made an attempt to login."""

    if request.method == 'GET':
        form = LoginForm()

    elif request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])

            if user is not None:
                # password matches username.
                if user.is_active:
                    # User is active. Log them in.
                    login(request, user)
                    return HttpResponse('Authenticated successfully')

                else:
                    # User is not active.
                    return HttpResponse('Disabled account')

            else:
                # password does not match username.
                return HttpResponse('Invalid Login')

    return render(request,
                  'account/login.html',
                  {'form': form})


@login_required
def dashboard(request):
    # define section variable to track where the user is.
    return render(request,
                  'account/dashboard.html',
                  {'section': 'dashboard'})


def register(request):
    """ Registers a new user. """
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)

        if user_form.is_valid():
            # create new user, do not save yet.
            new_user = user_form.save(commit=False)
            # set user's password; error is thrown if issue with password.
            # password saved is handled by Django; a hash is stored.
            new_user.set_password(user_form.cleaned_data['password'])
            # save new user and their profile.
            new_user.save()
            Profile.objects.create(user=new_user)

            return render(request,
                          'account/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,
                'account/register.html',
                {'user_form': user_form})


def edit(request):
    """ Allows users to update their account. """
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            # update the user and their profile.
            user_form.save()
            profile_form.save()
    elif request.method == 'GET':
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user)

    return render(request,
                  'account/edit.html',
                  {'user_form': user_form,
                    'profile_form': profile_form})

