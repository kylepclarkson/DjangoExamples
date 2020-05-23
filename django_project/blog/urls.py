from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView
from . import views

# See blog\view.py for matching parameters.
urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    # Find post corresponding to its primary key.
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    # url for creating new post
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('about/', views.about, name="blog-about"),
]

