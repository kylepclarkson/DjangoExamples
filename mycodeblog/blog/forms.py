from django import forms

from .models import Post

class PostForm(forms.ModelForm):
    ''' A custom form for creating blog posts. '''
    class Meta:
        model = Post
        fields = ['title', 'title_tag', 'author', 'body']

        # Widgets for styling form fields
        widgets = {
            # bootstrap form classes
            'title': forms.TextInput(attrs={'class':'form-control',
                                            'placeholder':'Post Title'}),
            'title_tag': forms.TextInput(attrs={'class':'form-control',
                                                'placeholder': 'Post Tag'}),
            'author': forms.Select(attrs={'class':'form-control'}),
            'body': forms.Textarea(attrs={'class':'form-control'}),
        }
