from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from .fields import OrderField

# Create your models here.

"""
    Models for education website. 
    Each course consists of multiple modules, with each 
    module containing various content - either text, file, image, or video files. Each 
    course will belong to a particular subject.
    
    Slug: A short label for something - generally used in URLS.
"""

class Subject(models.Model):
    title       = models.CharField(max_length=200)
    slug        = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

class Course(models.Model):
    # Creator of the course.
    owner       = models.ForeignKey(User,
                                    related_name='courses_created',
                                    on_delete=models.CASCADE)
    subject     = models.ForeignKey(Subject,
                                    related_name='courses',
                                    on_delete=models.CASCADE)
    title       = models.CharField(max_length=200)
    slug        = models.SlugField(max_length=200)
    overview    = models.TextField()
    created     = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title

class Module(models.Model):
    course      = models.ForeignKey(Course,
                                    related_name='modules',
                                    on_delete=models.CASCADE)
    title       = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    # Order is determined wrt. the course field.
    order       = OrderField(blank=True, for_fields=['course'])

    def __str__(self):
        return '{}. {}'.format(self.order, self.title)

    class Meta:
        ordering = ['order']


class Content(models.Model):
    module      = models.ForeignKey(Module,
                                    related_name='contents',
                                    on_delete=models.CASCADE)

    content_type= models.ForeignKey(ContentType,
                                    on_delete=models.CASCADE,
                                    limit_choices_to={'model_in':('text', 'video', 'image', 'file')})

    object_id   = models.PositiveIntegerField()

    item        = GenericForeignKey('content_type', 'object_id')

    order = OrderField(blank=True, for_fields=['module'])

    class Meta:
        ordering = ['order']


class ItemBase(models.Model):
    """
    An abstract model that provides common fields for all content models
    (text, file, image, video)
    """
    owner       = models.ForeignKey(User,
                                    # Generate related_name for each child model automatically.
                                    related_name='%(class)s_related',
                                    on_delete=models.CASCADE)
    title       = models.CharField(max_length=200)
    created     = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

class Text(ItemBase):
    content = models.TextField()

class File(ItemBase):
    file = models.FileField(upload_to='files')

class Image(ItemBase):
    file = models.FileField(upload_to='images')

class Video(ItemBase):
    url = models.URLField()