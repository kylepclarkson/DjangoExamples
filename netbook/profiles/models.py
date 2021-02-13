from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

from .utils import get_random_code

class Profile(models.Model):
    """ A profile of a user. Uses Django's user model. """
    first_name  =       models.CharField(max_length=200, blank=True)
    last_name   =       models.CharField(max_length=200, blank=True)
    user        =       models.OneToOneField(User, on_delete=models.CASCADE)
    bio         =       models.TextField(default='No bio.', max_length=400)
    email       =       models.EmailField(max_length=60, blank=True)
    country     =       models.CharField(max_length=200, blank=True)
    avatar      =       models.ImageField(default='avatar.png', upload_to='avatars/')
    friends     =       models.ManyToManyField(User, blank=True, related_name='friends')
    slug        =       models.SlugField(unique=True, blank=True)
    updated     =       models.DateTimeField(auto_now=True)
    created     =       models.DateTimeField(auto_now_add=True)

    def get_friends(self):
        return self.friends.all()

    def get_friends_count(self):
        return self.friends.all().count()

    def get_posts_count(self):
        # use reverse relationship. Use related_name field of author in Post model.
        return self.posts.all().count()

    def get_all_authors_posts(self):
        return self.posts.all()

    def get_likes_given_count(self):
        # return number of likes user has given.
        likes = self.like_set.all()
        total_liked = 0
        for item in likes:
            if item.value == 'like':
                total_liked += 1

        return total_liked

    def get_likes_received_count(self):
        posts = self.posts.all()
        total_liked = 0
        for post in posts:
            total_liked += post.liked.all().count()

        return total_liked

    def __str__(self):
        return f"{self.user.username}--created:{self.created.strftime('%d-%m-%y')}"

    def save(self, *args, **kwargs):
        """ Save Profile. """
        exists = False

        if self.first_name and self.last_name:
            # create slug using first and last name. Check if slug already exists.
            to_slug = slugify(str(self.first_name) + " " + str(self.last_name))
            exists = Profile.objects.filter(slug=to_slug).exists()
            while exists:
                to_slug = slugify(to_slug + " " + str(get_random_code()))
                exists = Profile.objects.filter(slug=to_slug).exists()
        else:
            to_slug = str(self.user)
        self.slug = to_slug
        super().save(*args, **kwargs)


STATUS_CHOICES = (
    ('send', 'send'),
    ('accepted', 'accepted')
)

class Relationship(models.Model):
    """ A directed interaction between two users (using their profiles)"""
    sender      =       models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender')
    receiver    =       models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='receiver')
    status      =       models.CharField(max_length=8, choices=STATUS_CHOICES)
    updated     =       models.DateTimeField(auto_now=True)
    created     =       models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender}--{self.receiver}--{self.status}'