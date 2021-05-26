from django.db import models
from django.contrib.auth.models import User


class Lead(models.Model):

    owner = models.ForeignKey(User, related_name="leads", on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200,)
    email = models.EmailField(max_length=200, unique=True,)
    message = models.CharField(max_length=500, blank=True,)
    created_at = models.DateField(auto_now_add=True)
    

