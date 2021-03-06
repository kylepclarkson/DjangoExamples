from django.db import models
from django.utils import timezone

import datetime


class Question(models.Model):

    question_text   = models.CharField(max_length=200)
    pub_date        = models.DateTimeField('date published')

    def was_published_recently(self):
        """ Return True of question was posted within the last 24 hours. """
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1) and self.pub_date <= timezone.now()
    # Override function fields for display in admin page.
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question        = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text     = models.CharField(max_length=200)
    votes           = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text






