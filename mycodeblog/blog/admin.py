from django.contrib import admin

from .models import Post, Category

# Register Post model with admin site.
admin.site.register(Post)
admin.site.register(Category)
