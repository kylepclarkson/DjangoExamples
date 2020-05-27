from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

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

    def __str__(self):
        return self.title


class Content(models.Model):
    module      = models.ForeignKey(Module,
                                    related_name='contents',
                                    on_delete=models.CASCADE)
    content_type= models.ForeignKey(ContentType,
                                    on_delete=models.CASCADE)
    object_id   = models.ForeignKey(ContentType,
                                    on_delete=models.CASCADE)
    item        = GenericForeignKey('content_type', 'object_id')

