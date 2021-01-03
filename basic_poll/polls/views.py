from django.shortcuts import render
from django.http import HttpResponse, Http404

import datetime
from .models import Question

# Create your views here.

def index(request):
    """ Display 5 newest questions. """
    questions   = Question.objects.order_by('-pub_date')[:5]
    context = {
        'questions': questions,
    }
    return render(request, 'polls/index.html', context=context)

def detail(request, question_id):
    """ Display details of question. Raise 404 error if question id dne. """

    try:
        question = Question.objects.get(pk=question_id)
    except:
        raise Http404("This question does not exist!")
    return render(request, 'polls/detail.html', context={'question': question})


def results(request, question_id):
    return HttpResponse(f"This is the results of question {question_id}")


def vote(request, question_id):
    return HttpResponse(f"This is voting on question: {question_id}")



