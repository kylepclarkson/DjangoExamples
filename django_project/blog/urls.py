from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView,
)
from . import views

# See blog\view.py for matching parameters.
urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    # Find posts corresponding to username
    path('users/<str:username>', UserPostListView.as_view(), name='user-posts'),
    # Find post corresponding to its primary key.
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    # url for creating new post
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    # PostUpdate
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    # PostDelete
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('about/', views.about, name="blog-about"),
]

