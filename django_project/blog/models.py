from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

class Post(models.Model):
    # Set fields of database corresponding to post.
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    # TODO P10 31:30
    def get_absolute_url(self):
        """ Return path to specific post. Called after post is created. """
        return reverse('post-detail', kwargs={'pk': self.pk})