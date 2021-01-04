from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.views import generic
from django.utils import timezone

import datetime
from .models import Question, Choice

# Create your views here.

# === Commented out to replace custom views with generic views. ===
# def index(request):
#     """ Display 5 newest questions. """
#     questions   = Question.objects.order_by('-pub_date')[:5]
#     context = {
#         'questions': questions,
#     }
#     return render(request, 'polls/index.html', context=context)
#
# def detail(request, question_id):
#     """ Display details of question. Raise 404 error if question id dne. """
#
#     try:
#         question = Question.objects.get(pk=question_id)
#     except:
#         raise Http404("This question does not exist!")
#     return render(request, 'polls/detail.html', context={'question': question})
#
#
# def results(request, question_id):
#     """ Display results for specified question. """
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html', {'question': question})

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'questions'

    def get_queryset(self):
        """ Return five most recent questions. """
        return Question.objects.filter(
            pub_date__lte=timezone.now(),    # Dates less than the current time.
        ).order_by('-pub_date')[:5]


class DetailView(generic.DeleteView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """ Exclude questions that are not yet published. """
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    """ Get user's choice. Increment its count, then redirect. """

    question = get_object_or_404(Question, pk=question_id)

    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You did not select a choice!"
        })

    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


