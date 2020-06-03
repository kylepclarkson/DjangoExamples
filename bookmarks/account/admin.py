from django.contrib import admin

from .models import Profile

# Register your models here.

# Register Profile model (can be accessed using admin.)
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'photo']