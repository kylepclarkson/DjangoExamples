from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import Post, Category
from .forms import PostForm, EditForm

# def home(request):
#     return render(request, 'home.html', context={})

# Class-based view
class HomeView(ListView):

    model = Post
    template_name = 'home.html'
    ordering = ['-id']

class ArticleDetailView(DetailView):

    model = Post
    template_name = 'article_detail.html'

class AddPostView(CreateView):

    model = Post
    form_class = PostForm

    template_name = 'add_post.html'
    # specify fields from model to put on page. Set PostForm.
    # fields = '__all__'
    # fields = ['title', 'body']

class AddCategoryView(CreateView):
    model = Category
    template_name = 'add_category.html'
    fields = '__all__'

class UpdatePostView(UpdateView):

    model = Post
    form_class = EditForm

    template_name = 'update_post.html'

class DeletePostView(DeleteView):

    model = Post
    template_name = 'delete_post.html'
    success_url = reverse_lazy('home')


'''
Function based view. 
Name 'categories' must match
path('category/<str:categories>/',CategoryView, name='category')
'''
def CategoryView(request, categories):
    # Get all posts belonging to category.
    # Replace '-' with ' ' (slugify) (#TODO see how to do better.)
    categories = categories.replace('-', ' ')
    category_posts = Post.objects.filter(categoires=categories)

    return render(request, 'categories.html', context={'categories':categories.title(),
                                                'category_posts':category_posts})

