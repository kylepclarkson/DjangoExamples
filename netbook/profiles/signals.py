from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

from .models import Profile, Relationship


@receiver(post_save, sender=User)
def post_save_create_profile(sender, instance, created, **kwargs):
    """ Upon creating a new user, create a new profile for this user.
        sender: The model that was create.
        instance: The instance that was created.
        created: True if instance is newly created; False if updated.
     """
    # print('sender', sender)
    # print('instance', instance)
    if created:
        # a new user instance is being created
        Profile.objects.create(user=instance)


@receiver(post_save, sender=Relationship)
def post_save_add_to_friends(sender, instance, created, **kwargs):
    """
    Upon relationship status being set to accepted, make the two
    users involved friends.
    """
    sender_ = instance.sender
    receiver_ = instance.receiver

    if instance.status == 'accepted':
        # request has been accepted. Make sender_ and receiver_ friends.
        sender_.friends.add(receiver_.user)
        receiver_.friends.add(sender_.user)
        sender_.save()
        receiver_.save()
