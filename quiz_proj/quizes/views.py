from django.shortcuts import render
from django.views.generic import ListView

from .models import Quiz


class QuizListView(ListView):
    model = Quiz
    template_name = 'quizes/main.html'


def quiz_view(request, pk):
    """ Return a specific quiz using its pk. """
    quiz = Quiz.objects.get(pk=pk)

    return render(request, 'quizes/quiz.html', {'obj': quiz})
