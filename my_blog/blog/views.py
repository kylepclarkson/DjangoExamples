from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post


def post_list(request):
    """ Get all published posts. """
    object_list = Post.published.all()
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
        'posts': posts
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

