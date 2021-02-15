from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

from.forms import ProfileModelForm
from .models import Profile, Relationship


@login_required
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



@login_required
def invites_received_view(request):
    profile = Profile.objects.get(user=request.user)
    qs = Relationship.objects.invitations_received(receiver=profile)
    # get the users that sent the friendship requests
    results = list(map(lambda x: x.sender, qs))
    is_empty = True if len(results) == 0 else False
    context = {
        'qs': results,
        'is_empty': is_empty,
    }

    return render(request, 'profiles/my_invites.html', context)



@login_required
def accept_invitation(request):
    """ Change relationship status to accepted """
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        sender = Profile.objects.get(pk=pk)
        receiver = Profile.objects.get(user=request.user)

        relationship = get_object_or_404(Relationship, sender=sender, receiver=receiver)
        if relationship.status == 'send':
            relationship.status = 'accepted'
            relationship.save()

    return redirect('profiles:my-invites-view')


@login_required
def reject_invitation(request):
    """ Delete relationship from database. """
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        sender = Profile.objects.get(pk=pk)
        receiver = Profile.objects.get(user=request.user)

        relationship = get_object_or_404(Relationship, sender=sender, receiver=receiver)
        relationship.delete()

    return redirect('profiles:my-invites-view')


# def profiles_list_view(request):
#     qs = Profile.objects.get_all_profiles(request.user)
#
#     context = {
#         'qs': qs
#     }
#
#     return render(request, 'profiles/profile_list.html', context)

class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'profiles/detail.html'

    def get_object(self, queryset=None):
        slug = self.kwargs.get('slug')
        profile = Profile.objects.get(slug=slug)
        return profile

    def get_context_data(self, *, object_list=None, **kwargs):
        """ Add additional data to context """
        context = super().get_context_data(**kwargs)
        # Get user of session
        user = User.objects.get(username__iexact=self.request.user)
        profile = Profile.objects.get(user=user)
        # Get relationships of user.
        relationship_receiver = Relationship.objects.filter(sender=profile)
        relationship_sender = Relationship.objects.filter(receiver=profile)
        rel_receiver = []
        rel_sender = []
        for item in relationship_receiver:
            rel_receiver.append(item.receiver.user)
        for item in relationship_sender:
            rel_sender.append(item.receiver.user)

        context['rel_receiver'] = rel_receiver
        context['rel_sender'] = rel_sender
        context['posts'] = self.get_object().get_all_authors_posts()
        context['len_posts'] = True if len(self.get_object().get_all_authors_posts()) > 0 else False

        return context


class ProfileListView(LoginRequiredMixin, ListView):
    model = Profile
    template_name = 'profiles/profile_list.html'
    context_object_name = 'qs'

    def get_queryset(self):
        qs = Profile.objects.get_all_profiles(self.request.user)
        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        """ Add additional data to context """
        context = super().get_context_data(**kwargs)
        # Get user of session
        user = User.objects.get(username__iexact=self.request.user)
        profile = Profile.objects.get(user=user)
        # Get relationships of user.
        relationship_receiver = Relationship.objects.filter(sender=profile)
        relationship_sender = Relationship.objects.filter(receiver=profile)
        rel_receiver = []
        rel_sender = []
        for item in relationship_receiver:
            rel_receiver.append(item.receiver.user)
        for item in relationship_sender:
            rel_sender.append(item.receiver.user)

        context['rel_receiver'] = rel_receiver
        context['rel_sender'] = rel_sender
        context['is_empty'] = False
        # Get if no other profiles exists.
        if len(self.get_queryset()) == 0:
            context['is_empty'] = True

        return context


@login_required
def invites_profiles_list_view(request):
    qs = Profile.objects.get_all_profiles_to_invite(request.user)
    context = {
        'qs': qs
    }

    return render(request, 'profiles/to_invite_list.html', context)


@login_required
def send_invitation(request):
    """ The user has sent a friend request."""
    if request.method == 'POST':
        # the pk of the profile in which the user has requested to be friends.
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)

        relationship = Relationship.objects.create(sender=sender, receiver=receiver, status='send')

        return redirect(request.META.get('HTTP_REFERER'))

    return redirect('profiles:my-profile-view')


@login_required
def remove_from_friends(request):
    """ Remove the friends request. Does not know who the sender/receiver is. """
    if request.method == 'POST':
        # the pk of the profile in which the user has requested to be friends.
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)

        # two either party created the relationship
        relationship = Relationship.objects.get(
            Q(sender=sender) & Q(receiver=receiver) |
            Q(sender=receiver) & Q(receiver=sender)
        )
        relationship.delete()

        return redirect(request.META.get('HTTP_REFERER'))

    return redirect('profiles:my-profile-view')

