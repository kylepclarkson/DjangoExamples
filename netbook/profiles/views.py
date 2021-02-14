from django.shortcuts import render

from.forms import ProfileModelForm
from .models import Profile, Relationship

def my_profile_view(request):
    """ Render user's profile"""
    profile = Profile.objects.get(user=request.user)
    form = ProfileModelForm(request.POST or None,
                            request.FILES or None,
                            instance=profile)
    confirm = False     # Track if profile is updated.

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            confirm = True

    context = {
        'profile': profile,
        'form': form,
        'confirm': confirm,
    }

    return render(request, 'profiles/myprofile.html', context)


def invites_received_view(request):
    profile = Profile.objects.get(user=request.user)
    qs = Relationship.objects.invitations_received(receiver=profile)

    context = {
        'qs': qs
    }

    return render(request, 'profiles/my_invites.html', context)


def profiles_list_view(request):
    qs = Profile.objects.get_all_profiles(request.user)

    context = {
        'qs': qs
    }

    return render(request, 'profiles/profile_list.html', context)


def invites_profiles_list_view(request):
    qs = Profile.objects.get_all_profiles_to_invite(request.user)
    context = {
        'qs': qs
    }

    return render(request, 'profiles/to_invite_list.html', context)


