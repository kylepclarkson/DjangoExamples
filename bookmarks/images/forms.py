from django import forms
from django.core.files.base import ContentFile
from django.utils.text import slugify
from urllib import request

from .models import Image

class ImageCreationForm(forms.ModelForm):

    class Meta:
        model = Image
        fields = ('title', 'url', 'description')

        # Override url field of default widget. Users will use js tool to add url.
        widgets = {
            'url': forms.HiddenInput
        }

    def clean_url(self):
        # Ensure url is of jpeg image.
        url = self.cleaned_data['url']
        valid_extensions = ['jpg', 'jpeg']
        extension = url.rsplit('.',1)[1].lower()

        if extension not in valid_extensions:
            raise forms.ValidationError('The given URL does not match image extensions.')
        return url

    '''
        Override save function to first save the image to drive, then the database.
    '''
    def save(self, force_input=False, force_update=False, commit=True):

        image = super().save(commit=False)
        image_url = self.cleaned_data['url']
        name = slugify(image.title)
        extension = image_url.rsplit('.', 1)[1].lower()
        image_name = f'{name}.{extension}'

        # download image
        response = request.urlopen(image_url)
        # Save downloaded image to image object.
        image.image.save(image_name,
                         ContentFile(response.read()),
                         save=False)

        if commit:
            # Save image to database.
            image.save()
        return image