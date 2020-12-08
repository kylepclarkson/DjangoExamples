from django.db import models
from django.urls import reverse

# Create your models here.

class Genre(models.Model):
    """ The Genre of a book. """
    name = models.CharField(max_length=200, help_text="Enter a book genre")

    def __str__(self):
        return self.name

class Book(models.Model):

    title = models.CharField(max_length=200)

    author =    models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    summary =   models.TextField(max_length=1000,
                                 help_text='Enter a brief description of the book.')
    isbn =      models.CharField('ISBN', max_length=13, unique=True,
                                 help_text='13 characters that uniquely identify the book')
    genre =     models.ManyToManyField(Genre, help_text='Select a genre for this book')

    def __str__(self):
        return self.title + " " + self.isbn

    def get_absolute_url(self):
        """ Returns the url to access a detail record of this book. """
        return reverse('book-detail', args=[str(self.id)])

# TODO define remaining class models. 
