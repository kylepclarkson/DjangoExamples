from django.shortcuts import render, redirect

from .models import Post, Like
from .forms import PostModelForm, CommentModelForm
from profiles.models import Profile


def post_comment_create_list_view(request):
    """ Handles """
    qs = Post.objects.all()
    profile = Profile.objects.get(user=request.user)

    post_form = PostModelForm()
    comment_form = CommentModelForm()

    # a post was created via the form
    post_added = False

    # name specified in html
    if 'submit_post_form' in request.POST:
        post_form = PostModelForm(request.POST, request.FILES)  # pass request files for image.
        if post_form.is_valid():
            # save form. Set author of update as request user.
            instance = post_form.save(commit=False)
            instance.author = profile
            instance.save()
            post_added = True
            post_form = PostModelForm()

    if 'submit_comment_form' in request.POST:
        comment_form = CommentModelForm(request.POST)
        if comment_form.is_valid():
            instance = comment_form.save(commit=False)
            instance.user = profile
            instance.post = Post.objects.get(id=request.POST.get('post_id'))
            instance.save()
            comment_form = CommentModelForm()


    context = {
        'qs': qs,
        'profile': profile,
        'post_form': post_form,
        'comment_form': comment_form,
        'post_added': post_added,
    }

    return render(request, 'posts/main.html', context)


def like_unlike_post(request):
    user = request.user

    if request.method == 'POST':
        # the post that was liked/unliked.
        post_id = request.POST.get('post_id')
        post_obj = Post.objects.get(id=post_id)
        profile = Profile.objects.get(user=user)

        if profile in post_obj.liked.all():
            # we want to unlike the post.
            post_obj.liked.remove(profile)
        else:
            # we want to like the post.
            post_obj.liked.add(profile)

        # update existing like, or create new like.
        like, created = Like.objects.get_or_create(user=profile, post_id=post_id)

        if not created:
            if like.value == 'like':
                like.value = 'unlike'
            else:
                like.value = 'like'
        else:
            like.value = 'like'

        post_obj.save()
        like.save()

    return redirect('posts:main-post-view')

