from django.db import models
from django.urls import reverse
import uuid # For unique book instances.

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

class BookInstance(models.Model):
    """ A specific instance of a book. """
    # A unique id for this book instance.
    id =    models.UUIDField(primary_key=True,
                             default=uuid.uuid4,
                             help_text='Unique ID for this instance of a book.')

    book =  models.ForeignKey('Book',
                              on_delete=models.SET_NULL,
                              null=True)
    # Details of specific book release.
    imprint = models.CharField(max_length=200)
    # The date in which this book instance is due to be returned.
    due_back = models.DateField(null=True, blank=True)

    LOAD_STATUS = (
        ('m', 'Maintenance'), ('o', 'On loan'), ('a', 'Available'), ('r', 'Reserved')
    )
    # The status of this book instance.
    status  = models.CharField(
        max_length=1,
        choices=LOAD_STATUS,
        blank=True,
        default='m',
        help_text='Book availability.'
    )

    class Meta:
        ordering = ['due_back']

    def __str__(self):
        return f'{self.id} ({self.book.title})'

class Author(models.Model):
    """ A model representing the author of a book. """

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        """ Returns the url to access an author instance. """
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'




