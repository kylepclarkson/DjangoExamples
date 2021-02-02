from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class PublishedManager(models.Manager):
    """ A custom manager that gets only published posts. """
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')


class Post(models.Model):

    # set query managers.
    objects = models.Manager()  # default
    published = PublishedManager()

    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published')
    )

    title =         models.CharField(max_length=250)
    slug =          models.SlugField(max_length=250, unique_for_date='publish') # build url using slug and publish date
    author =        models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    body =          models.TextField()
    publish =       models.DateTimeField(default=timezone.now)      # when post was published.
    created =       models.DateTimeField(auto_now_add=True)         # when the post was first created.
    updated =       models.DateTimeField(auto_now=True)             # when the post was last updated.
    status =        models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return f'{self.title}, {self.status}'

