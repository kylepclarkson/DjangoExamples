from django.shortcuts import render
from django.views.generic import ListView
from django.http import JsonResponse

from .models import Quiz
from questions.models import Question, Answer
from results.models import Result


class QuizListView(ListView):
    model = Quiz
    template_name = 'quizes/main.html'


def quiz_view(request, pk):
    """ Return a specific quiz using its pk. """
    quiz = Quiz.objects.get(pk=pk)

    return render(request, 'quizes/quiz.html', {'obj': quiz})


def quiz_data_view(request, pk):
    """ Returns questions/answers and time for quiz. """
    quiz = Quiz.objects.get(pk=pk)

    # a list of dictionaries.
    # each list entry is a dict where the key is the question and the value a list of answers to the question.
    questions = []
    for q in quiz.get_questions():
        answers = []
        for a in q.get_answers():
            answers.append(a.text)
        questions.append({str(q): answers})

    return JsonResponse({
        'data': questions,
        'time': quiz.time
    })


def save_quiz_view(request, pk):

    if request.is_ajax():
        data = request.POST
        questions = []
        # convert http dict to python dict
        data_ = dict(data)
        # remove csrf token
        data_.pop('csrfmiddlewaretoken')

        for k in data_.keys():
            # key's are the 'text' of each question.
            question = Question.objects.get(text=k)
            questions.append(question)

        user = request.user
        quiz = Quiz.objects.get(pk=pk)

        score = 0
        multiplier = 100 / quiz.number_of_questions
        # a list of dict objects. Each entry of the list with have a question's text as key
        # with a dict as its value, if answered. The inner dict will contain the
        # correct answer and what answer was selected. If not answered, value will be a string.
        results = []
        correct_answer = None

        for q in questions:
            # get the answer selected from this question
            ans_selected = request.POST.get(q.text)

            if ans_selected != "":
                question_answers = Answer.objects.filter(question=q)
                # for each answer, check if it is correct. Append correct answer to results.
                for a in question_answers:
                    if ans_selected == a.text:
                        if a.correct:
                            score += 1
                            correct_answer = a.text

                results.append({
                    str(q): {
                        'correct_answer': correct_answer,
                        'answered': ans_selected
                    }
                })
            else:
                # no answered was given.
                results.append({str(q): 'not answered'})

        score_ = score * multiplier
        Result.objects.create(quiz=quiz, user=user, score=score_)
        passed = False

        if score_ >= quiz.required_score_to_pass:
            passed = True

        return JsonResponse({
            'passed': passed,
            'score': score_,
            'results': results,
        })

