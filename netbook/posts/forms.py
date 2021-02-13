from django import forms

from .models import Post, Comment


class PostModelForm(forms.ModelForm):
    # Specify content textarea will consist only of 3 rows
    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}))

    class Meta:
        model = Post
        fields = ('content', 'image', )


class CommentModelForm(forms.ModelForm):
    # set placeholder value for form field, set body label to empty.
    body = forms.CharField(label='',
                           widget=forms.TextInput(attrs={'placeholder': 'Add a comment'}))

    class Meta:
        model = Comment
        fields = ('body',)
