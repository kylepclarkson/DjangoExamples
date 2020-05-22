from django.shortcuts import render

posts = [
    {
        'author': 'Danny Slave',
        'title': "Blog post 1",
        'content': 'My first blog post is here',
        'date_posted': 'May 22, 2020'
    },
    {
        'author': 'Arin Slave',
        'title': "Blog post 2",
        'content': 'My first blog post is here',
        'date_posted': 'May 22, 2020'
    }

]

def home(request):
    # past data to render request.
    context = {
        'posts':posts
    }
    # Render home.html
    return render(request, 'blog/home.html', context=context)

def about(request):
    return render(request, 'blog/about.html')
