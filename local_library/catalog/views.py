from django.shortcuts import render
from django.views import generic

from .models import *

class BookListView(generic.ListView):
    # get all records of Book model
    model = Book

def index(request):
    """ The home page of the site. """
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    num_instances_available = \
        BookInstance.objects.filter(status__exact='a').count()

    num_authors = Author.objects.all().count()

    # save values in context dict.
    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

