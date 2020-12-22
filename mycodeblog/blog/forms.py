from django import forms

from .models import Post, Category

# ''' Hard code Selection. Use model instead. '''
# choices = [('coding', 'Coding'),
#            ('sports','Sports'),
#            ('travel', 'Travel')]
'''
TODO - Make choices dynamic by creating FK relationship. 
https://stackoverflow.com/questions/3419997/creating-a-dynamic-choice-field
'''
def get_choices():
    choices = Category.objects.all().values_list('name','name')
    choice_list = []
    for item in choices:
        choice_list.append(item)
    return choice_list

class PostForm(forms.ModelForm):
    ''' A custom form for creating blog posts. '''
    class Meta:
        model = Post
        fields = ['title', 'title_tag', 'author', 'category', 'body']

        # Widgets for styling form fields
        widgets = {
            # bootstrap form classes
            'title':    forms.TextInput(attrs={'class':'form-control',
                                            'placeholder':'Post Title'}),
            'title_tag': forms.TextInput(attrs={'class':'form-control',
                                                'placeholder': 'Post Tag'}),
            'author':   forms.Select(attrs={'class':'form-control'}),
            # 'category': forms.Select(choices=choices, attrs={'class': 'form-control'}),
            'category': forms.Select(choices=get_choices(), attrs={'class': 'form-control'}),
            'body':     forms.Textarea(attrs={'class':'form-control'}),
        }

class EditForm(forms.ModelForm):
    ''' A custom form for creating blog posts. '''
    class Meta:
        model = Post
        fields = ['title', 'title_tag', 'body']

        # Widgets for styling form fields
        widgets = {
            # bootstrap form classes
            'title': forms.TextInput(attrs={'class':'form-control',
                                            'placeholder':'Post Title'}),
            'title_tag': forms.TextInput(attrs={'class':'form-control',
                                                'placeholder': 'Post Tag'}),
            'body': forms.Textarea(attrs={'class':'form-control'}),
        }
