from django.db import models

# Create your models here.


class Author(models.Model):
    """ Authors that have contributed to research articles. """

    last_name           = models.CharField(max_length=80)
    first_name          = models.CharField(max_length=80)
    url_link            = models.URLField(max_length=200)

    def __str__(self):
        return f'{str(self.first_name)} {str(self.last_name)}'


class Publication(models.Model):
    """ A publication (differs from article as it is published.)  """

    title =             models.CharField(max_length=200)
    description =       models.CharField(max_length=500)
    year_published =    models.CharField(max_length=5)
    authors =           models.ManyToManyField(Author)
    file =              models.FileField(blank=True, null=True,
                                         upload_to='research/%Y/')

class Article(models.Model):
    pass





