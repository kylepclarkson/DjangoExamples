from django.contrib import admin

from .models import Article, Author, Publication
# Register your models here.

admin.site.register(Article)
admin.site.register(Publication)
admin.site.register(Author)
