from django.shortcuts import render, redirect

from .models import Post, Like
from profiles.models import Profile


def post_comment_create_list_view(request):
    """ Handles """
    qs = Post.objects.all()
    profile = Profile.objects.get(user=request.user)

    context = {
        'qs': qs,
        'profile': profile
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

