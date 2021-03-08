from django.urls import path
from . import views

app_name = 'quizes'

urlpatterns = [
    path('', views.QuizListView.as_view(), name='main-view'),
    path('<pk>/', views.quiz_view, name='quiz-view'),
]