from django.shortcuts import render

from blog.models import Post, Comment
from .forms import CommentForm

def blog_index(request):
    ''' Get app blog posts, sorted by newest to oldest. '''
    # '-' sign, sort by oldest first.
    posts = Post.objects.all().order_by('-created_on')

    context = {
        'posts': posts,
    }

    return render(request, 'blog_index.html', context)

def blog_category(request, category):
    ''' Get all blog posts with category "category" '''
    posts = Post.objects.filter(
        categories__name__contains=category
    ).order_by(
        '-created_on'
    )

    context  = {
        'category': category,
        'posts': posts
    }

    return render(request, 'blog_category.html', context)

def blog_detail(request, pk):
    ''' Get blog post with comments. Add form for submitting comment to blog post. '''

    post = Post.objects.get(pk=pk)
    comments = Comment.objects.filter(post=post)

    # Form for submitting comments.
    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment(
                author = form.cleaned_data['author'],
                body = form.cleaned_data['body'],
                post = post
            )
            comment.save()

    context = {
        'post': post,
        'comments': comments,
        'form': form,
    }

    return render(request, 'blog_detail.html', context)


