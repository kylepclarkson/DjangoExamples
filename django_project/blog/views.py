from django.shortcuts import render
from .models import Post        # Import Post class.

def home(request):
    # past data to render request.
    context = {
        'title':'HomePage',
        'posts': Post.objects.all()
    }
    # Render home.html
    return render(request, 'blog/home.html', context=context)

def about(request):
    return render(request, 'blog/about.html',context={'title':'about'})
