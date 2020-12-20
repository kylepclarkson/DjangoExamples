from django import forms

class CommentForm(forms.Form):
    author      = forms.CharField(
        max_length = 100,    # matches length of author in blog.models
        widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your name'
        })
    )

    body        = forms.CharField(widget=forms.Textarea(
        attrs= {
            'class': 'form-control',
            'placeholder': 'Leave a comment!'
        }
    ))