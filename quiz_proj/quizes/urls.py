from django.urls import path
from . import views

app_name = 'quizes'

urlpatterns = [
    path('', views.QuizListView.as_view(), name='main-view'),
    path('<pk>/', views.quiz_view, name='quiz-view'),
    path('<pk>/data/', views.quiz_data_view, name='quiz-data-view'),
    path('<pk>/save/', views.save_quiz_view, name='save-view'),
]

