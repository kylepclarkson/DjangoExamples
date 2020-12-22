from datetime import datetime, date

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    ''' Blog post '''

    title =         models.CharField(max_length=255)
    title_tag =     models.CharField(max_length=255)
    author =        models.ForeignKey(User, on_delete=models.CASCADE)
    body =          models.TextField()
    created_date =  models.DateField(auto_now_add=True)

    # Upon creation of post in model, redirect to article-detail page.
    def get_absolute_url(self):
        return reverse('article-detail', args=(str(self.id)))

    def __str__(self):
        return self.title + ' | ' + str(self.author)


