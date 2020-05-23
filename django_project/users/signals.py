from django.db.models.signals import post_save  # signal is fired once an object is saved.
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

# When user is saved, a post_save signal is sent.
# This signal is received by this function (with arguments from signal)
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    '''
    :param sender:
    :param instance: Instance of user created.
    :param created:  If user is created.
    :param kwargs:
    :return:
    '''
    if created:
        ''' If user is created, '''
        Profile.objects.create(user=instance)

# Save profile instance.
@receiver(post_save, sender=User)
def save_profile(sender, instance, created, **kwargs):
    instance.profile.save()
