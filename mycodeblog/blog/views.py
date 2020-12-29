from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import Post, Category
from .forms import PostForm, EditForm

# def home(request):
#     return render(request, 'home.html', context={})

# Class-based view
class HomeView(ListView):
    # Get all post ordered newest first.
    model = Post
    template_name = 'home.html'
    ordering = ['-id']

    def get_context_data(self, *args, **kwargs):
        ''' Set context. '''
        # Get all category names.
        category_menu = Category.objects.all()

        context = super(HomeView, self).get_context_data(*args, **kwargs)
        context['category_menu'] = category_menu
        return context


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
    category_posts = Post.objects.filter(category=categories)

    return render(request, 'categories.html', context={'categories':categories.title(),
                                                'category_posts':category_posts})


def CategoryListView(request):
    categories_menu_list = Category.objects.all()

    return render(request, 'categories_list.html', {'categories_menu_list': categories_menu_list})

# 3 steps: create view, create template, create url