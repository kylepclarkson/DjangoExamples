from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.contrib.postgres.search import SearchVector

from taggit.models import Tag

from .forms import SearchForm
from .models import Post

class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'

def post_list(request, tag_slug=None):
    """
    Get all published posts.
    :param request:
    :param tag_slug: Filter lists by tags from tag_slug.
    :return:
    """
    object_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    # Display 3 posts per page.
    paginator = Paginator(object_list, 3)
    # The current page the user is on.
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # Deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # Page is out of range, deliver last.
        posts = paginator.page(paginator.num_pages)

    context = {
        'page': page,
        'posts': posts,
        'tag': tag,
    }

    return render(request,
                   'blog/post/list.html',
                   context)


def post_detail(request, year, month, day, post):
    """ Get specific post (slug is based on publish and slug fields.) """
    post = get_object_or_404(Post,
                             slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)

    context = {
        'post': post
    }
    return render(request,
                  'blog/post/detail.html',
                  context)


def post_search(request):
    """ Get search from form, find results using query, and return. """
    form = SearchForm()
    query = None
    results = []
    # Check if form has been submitted
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Post.published.annotate(
                search=SearchVector('title', 'body'),
            ).filter(search=query)

    context = {
        'form': form,
        'query': query,
        'results': results
    }

    return render(request,
                  'blog/post/search.html',
                  context)