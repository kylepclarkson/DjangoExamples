from django.shortcuts import render
from django.views.generic import (ListView, DetailView, CreateView)
from .models import Post        # Import Post class.

def home(request):
    # past data to render request.
    context = {
        'title':'HomePage',
        'posts': Post.objects.all()
    }
    # Render home.html
    return render(request, "blog/home.html", context=context)

"""
    Using class-based view instead of function-based view. 
"""

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html' # looks for templates <app>/<model>_<viewtype>.html
    # Specify name (key) of object.
    context_object_name = 'posts'
    # Order posts
    order = ['-date_posted']

class PostDetailView(DetailView):
    model = Post


class PostCreateView(CreateView):
    model = Post
    # Set fields of post
    fields = ['title', 'content']

    def form_valid(self, form):
        ''' Override method to set author. '''
        form.instance.author = self.request.user
        return super().form_valid(form)


def about(request):
    return render(request, 'blog/about.html',context={'title':'about'})
