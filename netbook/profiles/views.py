from django.shortcuts import render

from.forms import ProfileModelForm
from .models import Profile

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