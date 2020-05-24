from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView)
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
    ordering = ['-date_posted']
    # Paginate posts (limit posts per page)
    paginate_by = 5

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html' # looks for templates <app>/<model>_<viewtype>.html
    # Specify name (key) of object.
    context_object_name = 'posts'
    # Order posts
    ordering = ['-date_posted']
    # Paginate posts (limit posts per page)
    paginate_by = 5

    def get_queryset(self):
        """ Get posts by username. """
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
    # LoginRequiredMixin - requires to be login.
    model = Post
    # Set fields of post
    fields = ['title', 'content']

    def form_valid(self, form):
        ''' Override method to set author. '''
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    # LoginRequiredMixin - requires to be login.
    model = Post
    # Set fields of post
    fields = ['title', 'content']

    def form_valid(self, form):
        ''' Override method to set author. '''
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        """ Test if user can update post. """
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    # The url if delete is successful.
    success_url = '/'

    def test_func(self):
        """ Test if user can update post. """
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False


def about(request):
    return render(request, 'blog/about.html',context={'title':'about'})
