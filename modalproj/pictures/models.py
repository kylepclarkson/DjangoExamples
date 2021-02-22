from django.db import models


class Picture(models.Model):

    item = models.ImageField(upload_to='images/')
    info = models.CharField(max_length=200)

    def __str__(self):
        return f'{str(self.pk)}-{self.info}'